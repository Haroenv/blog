---
layout: post
title: Make a WinForm sharp
date: 2016-05-24 11:00
tags: [windows,c#,.net]
---

You might have noticed that if you're making a WinForm application on a higher resolution display that it looks quite blurry.

<figure>
  <img src="/assets/winform-blurry.png" alt="a blurry WinForm">
  <figcaption>A blurry WinForm</figcaption>
</figure>

The reason of this is because by default the application won't take the dpi scaling in account and scale the pixels it expect to the physical pixels. To fix this, you have to go to `Program.cs`, which is in the same folder as the one you created your WinForm project in. By default it looks like this:

```csharp
[STAThread]
static void Main() {
    Application.EnableVisualStyles();
    Application.SetCompatibleTextRenderingDefault(false);
    Application.Run(new Form1());
}
```

We'll change that to this:

```csharp
[STAThread]
static void Main() {
    if (Environment.OSVersion.Version.Major >= 6) SetProcessDPIAware();
    Application.EnableVisualStyles();
    Application.SetCompatibleTextRenderingDefault(false);
    Application.Run(new Form1());
}

[System.Runtime.InteropServices.DllImport("user32.dll")]
private static extern bool SetProcessDPIAware();
```

And then we get (on supported platforms, everything more than Vista) a proper pixel scaling of our form!

<figure>
  <img src="/assets/winform-fixed.png" alt="a sharp WinForm">
  <figcaption>A sharp WinForm</figcaption>
</figure>
