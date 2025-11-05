#!/usr/bin/env python3
"""
Convert GPX file to simplified elevation graph SVG and generate ride data JSON
"""
import xml.etree.ElementTree as ET
import math
import glob
import json
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in meters using Haversine formula"""
    R = 6371000  # Earth radius in meters

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def parse_gpx(filepath: str) -> Tuple[List[Tuple[float, float]], Dict]:
    """Parse GPX file and return elevation points and ride statistics"""
    tree = ET.parse(filepath)
    root = tree.getroot()

    # Define namespaces
    ns = {
        "gpx": "http://www.topografix.com/GPX/1/1",
        "gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
    }

    points = []
    raw_points = []  # Store for moving time calculation
    total_distance = 0.0
    prev_lat = None
    prev_lon = None

    # Statistics tracking
    heart_rates = []
    elevation_gain = 0.0
    prev_ele = None

    # Extract all track points
    for trkpt in root.findall(".//gpx:trkpt", ns):
        lat = float(trkpt.get("lat"))
        lon = float(trkpt.get("lon"))
        ele_elem = trkpt.find("gpx:ele", ns)
        time_elem = trkpt.find("gpx:time", ns)

        time = None
        if time_elem is not None:
            time_str = time_elem.text
            time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))

        if ele_elem is not None:
            elevation = float(ele_elem.text)

            # Track elevation gain
            if prev_ele is not None and elevation > prev_ele:
                elevation_gain += elevation - prev_ele
            prev_ele = elevation

            # Calculate cumulative distance
            if prev_lat is not None and prev_lon is not None:
                distance = haversine_distance(prev_lat, prev_lon, lat, lon)
                total_distance += distance

            points.append((total_distance / 1000, elevation))  # Convert to km
            raw_points.append(
                {
                    "lat": lat,
                    "lon": lon,
                    "ele": elevation,
                    "time": time,
                    "distance": total_distance,
                }
            )

            prev_lat = lat
            prev_lon = lon

        # Parse heart rate from extensions
        extensions = trkpt.find("gpx:extensions", ns)
        if extensions is not None:
            tpx = extensions.find("gpxtpx:TrackPointExtension", ns)
            if tpx is not None:
                hr_elem = tpx.find("gpxtpx:hr", ns)
                if hr_elem is not None:
                    heart_rates.append(int(hr_elem.text))

    # Calculate moving time (exclude stopped segments)
    moving_time_seconds = 0.0
    SPEED_THRESHOLD = 0.5  # m/s (1.8 km/h) - below this is considered stopped

    for i in range(1, len(raw_points)):
        if raw_points[i]["time"] and raw_points[i - 1]["time"]:
            time_diff = (
                raw_points[i]["time"] - raw_points[i - 1]["time"]
            ).total_seconds()
            distance_diff = raw_points[i]["distance"] - raw_points[i - 1]["distance"]

            # Only count time if moving (and reasonable time gap)
            if time_diff > 0 and time_diff < 300:  # Max 5 min between points
                speed = distance_diff / time_diff  # m/s
                if speed >= SPEED_THRESHOLD:
                    moving_time_seconds += time_diff

    # Calculate statistics
    stats = {
        "distance": round(total_distance / 1000),  # km
        "elevation": round(elevation_gain),  # m
        "moving_time_minutes": round(moving_time_seconds / 60),
        "calories": 0,
        "avg_heart_rate": 0,
        "max_heart_rate": 0,
    }

    # Calculate heart rate stats and calories
    if heart_rates and moving_time_seconds > 0:
        stats["avg_heart_rate"] = round(sum(heart_rates) / len(heart_rates))
        stats["max_heart_rate"] = max(heart_rates)

        # Cycling-specific calorie estimation
        # Combines distance, elevation, time and heart rate for more accurate results
        body_weight_kg = 75
        time_hours = moving_time_seconds / 3600
        distance_km = total_distance / 1000
        avg_hr = stats["avg_heart_rate"]
        elevation_m = elevation_gain

        # Base metabolic cost from distance and speed
        # Average power estimation: ~150-200W for moderate cycling
        avg_speed_kmh = distance_km / time_hours if time_hours > 0 else 0

        # Estimate power from speed (rough approximation)
        # Power (watts) ≈ 3.5 * speed_kmh + 0.5 * elevation_gain/time_hours
        estimated_power = 3.5 * avg_speed_kmh + (
            0.5 * elevation_m / time_hours if time_hours > 0 else 0
        )

        # Calories from power: Power(W) * time(h) * 3.6 (kJ to kcal conversion)
        # Plus 20% for cycling efficiency (~80% efficient, so divide by 0.8)
        power_calories = estimated_power * time_hours * 3.6 / 0.8

        # Heart rate adjustment factor (relative to moderate intensity ~130 bpm)
        hr_factor = avg_hr / 130

        # Final estimate with HR adjustment
        stats["calories"] = round(power_calories * hr_factor)

    return points, stats


def simplify_data(
    points: List[Tuple[float, float]], target_points: int = 500
) -> List[Tuple[float, float]]:
    """Simplify data by sampling evenly across the distance"""
    if len(points) <= target_points:
        return points

    simplified = []
    step = len(points) / target_points

    for i in range(target_points):
        idx = int(i * step)
        if idx < len(points):
            simplified.append(points[idx])

    # Always include the last point
    if points[-1] not in simplified:
        simplified.append(points[-1])

    return simplified


def create_svg(
    points: List[Tuple[float, float]],
    global_max_dist: float,
    global_min_ele: float,
    global_max_ele: float,
    total_distance: float,
    elevation_gain: int,
    width: int = 1200,
    height: int = 400,
) -> str:
    """Create SVG elevation graph with consistent global scale"""
    if not points:
        return ""

    # Add padding to prevent clipping
    padding = 4  # Enough for stroke-width/2 + circle radius
    graph_width = width - 2 * padding
    graph_height = height - 2 * padding

    # Scale functions using global bounds
    def scale_x(dist):
        return padding + (dist / global_max_dist) * graph_width

    def scale_y(ele):
        # Invert Y axis (SVG coordinates start from top)
        return (
            padding
            + graph_height
            - (ele - global_min_ele) / (global_max_ele - global_min_ele) * graph_height
        )

    # Build SVG path
    path_points = []
    for dist, ele in points:
        x = scale_x(dist)
        y = scale_y(ele)
        path_points.append(f"{x:.2f},{y:.2f}")

    path_d = "M " + " L ".join(path_points)

    # Create data array for JavaScript
    data_points = []
    for dist, ele in points:
        x = scale_x(dist)
        data_points.append(f"{{x:{x:.2f},dist:{dist:.1f},ele:{int(round(ele))}}}")

    data_array = "[" + ",".join(data_points) + "]"

    # Default text showing total distance and elevation gain
    default_text = f"{total_distance:.1f}km, {elevation_gain}m"

    # Generate SVG with embedded JavaScript
    svg = f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" class="elevation-graph">
  <defs>
    <style>
      .elevation-text {{
        font-size: 16px;
        fill: currentColor;
        opacity: 1;
        transition: opacity 0.2s;
        text-anchor: end;
      }}
    </style>
  </defs>
  <path d="{path_d}" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
  <text id="elevationText" class="elevation-text" x="{width - padding - 10}" y="{height - padding - 10}">{default_text}</text>
  <script>
    <![CDATA[
      (function() {{
        var currentScript = document.currentScript;
        var svg = currentScript.closest('svg');
        var text = svg.querySelector('#elevationText');
        var data = {data_array};
        var defaultText = '{default_text}';
        
        function updateText(e) {{
          var pt = svg.createSVGPoint();
          pt.x = e.clientX;
          pt.y = e.clientY;
          var svgP = pt.matrixTransform(svg.getScreenCTM().inverse());
          
          var closest = null;
          var minDist = Infinity;
          for (var i = 0; i < data.length; i++) {{
            var dist = Math.abs(data[i].x - svgP.x);
            if (dist < minDist) {{
              minDist = dist;
              closest = data[i];
            }}
          }}
          
          if (closest) {{
            text.textContent = closest.dist + 'km, ' + closest.ele + 'm';
          }}
        }}
        
        function resetText() {{
          text.textContent = defaultText;
        }}
        
        svg.addEventListener('pointermove', updateText);
        svg.addEventListener('pointerleave', resetText);
        
        svg.addEventListener('touchmove', function(e) {{
          e.preventDefault();
        }}, {{ passive: false }});
      }})();
    ]]>
  </script>
</svg>"""

    return svg


def main():
    # Configuration
    target_points = 500  # Number of points in simplified data

    # Find all GPX files in current directory
    gpx_files = sorted(glob.glob("*.gpx"))

    if not gpx_files:
        print("No GPX files found in current directory")
        return

    # Create output directory
    output_dir = Path("../../../_includes/img/diagonal")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(gpx_files)} GPX files")
    print(f"Output directory: {output_dir}")
    print()

    # First pass: parse all files and find global min/max values
    print("Calculating global scale...")
    all_points = []
    all_stats = []
    for gpx_file in gpx_files:
        points, stats = parse_gpx(gpx_file)
        all_points.append(points)
        all_stats.append(stats)

    # Find global bounds
    global_max_dist = max(points[-1][0] for points in all_points if points)
    global_min_ele = min(min(p[1] for p in points) for points in all_points if points)
    global_max_ele = max(max(p[1] for p in points) for points in all_points if points)

    print(f"  Max distance: {global_max_dist:.2f} km")
    print(f"  Elevation range: {global_min_ele:.1f}m - {global_max_ele:.1f}m")
    print()

    # Second pass: generate SVGs with consistent scale
    for i, (gpx_file, points, stats) in enumerate(
        zip(gpx_files, all_points, all_stats), start=1
    ):
        print(f"[{i}/{len(gpx_files)}] Processing: {gpx_file}")

        try:
            # Calculate total distance from original data
            total_distance = points[-1][0]
            print(f"  {len(points)} data points, distance: {total_distance:.2f} km")

            # Get elevation gain from stats
            elevation_gain = stats["elevation"]
            print(f"  Elevation gain: D+{elevation_gain}m")
            print(f"  Moving time: {stats['moving_time_minutes']} minutes")
            print(
                f"  Avg HR: {stats['avg_heart_rate']} bpm, Max HR: {stats['max_heart_rate']} bpm"
            )
            print(f"  Estimated calories: {stats['calories']} kcal")

            # Simplify
            simplified_points = simplify_data(points, target_points)
            print(f"  Simplified to {len(simplified_points)} points")

            # Generate SVG with global scale
            svg_output = output_dir / f"elevation-{i}.svg"
            svg_content = create_svg(
                simplified_points,
                global_max_dist,
                global_min_ele,
                global_max_ele,
                total_distance,
                elevation_gain,
            )
            with open(svg_output, "w") as f:
                f.write(svg_content)

            print(f"  Saved: {svg_output}")
            print()

        except Exception as e:
            print(f"  Error processing {gpx_file}: {e}")
            print()

    # Calculate totals and averages
    print("Calculating totals and averages...")

    total_distance = sum(s["distance"] for s in all_stats)
    total_elevation = sum(s["elevation"] for s in all_stats)
    total_minutes = sum(s["moving_time_minutes"] for s in all_stats)
    total_calories = sum(s["calories"] for s in all_stats)

    # Weighted average heart rate (by time)
    weighted_hr_sum = sum(
        s["avg_heart_rate"] * s["moving_time_minutes"] for s in all_stats
    )
    avg_heart_rate = round(weighted_hr_sum / total_minutes) if total_minutes > 0 else 0

    # Maximum heart rate across all rides
    max_heart_rate = max(s["max_heart_rate"] for s in all_stats)

    # Average speed
    avg_speed = (
        round(total_distance * 60 / total_minutes, 1) if total_minutes > 0 else 0
    )

    # Convert total minutes to hours and minutes
    hours = total_minutes // 60
    minutes = total_minutes % 60

    # Format numbers with space as thousand separator
    def format_number(num):
        return f"{num:,}".replace(",", " ")

    summary = {
        "days_cycling": len(all_stats),
        "total_distance": total_distance,
        "total_distance_formatted": format_number(total_distance),
        "total_elevation": total_elevation,
        "total_elevation_formatted": format_number(total_elevation),
        "total_moving_time_minutes": total_minutes,
        "total_moving_time_formatted": f"{hours}h {minutes}m",
        "average_speed": avg_speed,
        "average_heart_rate": avg_heart_rate,
        "max_heart_rate": max_heart_rate,
        "total_calories": total_calories,
        "total_calories_formatted": format_number(total_calories),
    }

    print(f"  Days: {summary['days_cycling']}")
    print(f"  Total distance: {summary['total_distance']} km")
    print(f"  Total elevation: {summary['total_elevation']} m")
    print(f"  Total moving time: {summary['total_moving_time_formatted']}")
    print(f"  Average speed: {summary['average_speed']} km/h")
    print(f"  Average HR: {summary['average_heart_rate']} bpm")
    print(f"  Max HR: {summary['max_heart_rate']} bpm")
    print(f"  Total calories: {summary['total_calories']} kcal")
    print()

    # Generate JSON data file with rides and summary
    print("Generating ride data JSON...")
    json_output = Path("../../../_data/diagonal.json")
    output_data = {
        "rides": all_stats,
        "summary": summary,
    }
    with open(json_output, "w") as f:
        json.dump(output_data, f, indent=2)
    print(f"Saved: {json_output}")
    print()

    print("Done!")


if __name__ == "__main__":
    main()
