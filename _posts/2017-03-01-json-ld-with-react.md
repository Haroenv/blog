---
title: JSON-ld with React
date: 2017-03-01T12:55:12Z
tags: react, linked-data, json-ld
---
It's not very hard to render json-ld with React, but since it's something that's not completely obvious; it looks like this: 

```jsx
const Element = ({data}) => (
  <script type="application/ld+json">
    {JSON.stringify({
      ...data
    })}
  </script>
)
```

If you would have naively done this, you would expect to escape the brackets, but it's easier if you render the `JSON.stringify` output for the content of the `script`.
