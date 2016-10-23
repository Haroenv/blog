---
layout: post
title: Inline SVG in CSS
date: 2016-10-23 13:37
tags: [css]
---

From time to time you'll want to have a small svg as a background image for some icon. However regularly linking to it causes an extra request, and that's not always fun.

You can use a `utf-8` data URI though. Prefix your URI with:

```
data:image/svg+xml;utf8,
```

Which you can then use like this:

```css
.some-icon {
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewbox='100 100 100 100' width='100' height='100'><path fill='none' stroke='red' stroke-width='10' d='m43,35H5v60h60V57M45,5v10l10,10-30,30 20,20 30-30 10,10h10V5z'/></svg>");
}
```

Take in accoun that there's a bug in Firefox that doesn't allow `#` in data URIs. You can avoid this by using `rgb()` instead.
