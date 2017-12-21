---
layout: post
title: JSON-LD with React
date: 2017-03-01T12:55:12Z
tags: [react, linked-data, json-ld]
---

It's not very hard to render json-ld with React, but since it's something that's not completely obvious; it looks like this:

```
const JsonLd = ({ data }) =>
  <script type="application/ld+json">
    {JSON.stringify(data)}
  </script>;
```

As [noted](#comment-3255424415) by Iain Collins, in some cases you'll need to set this as dangerous HTML like this:

```
{% raw %}const JsonLd = ({ data }) =>
  <script
    type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
  />;{% endraw %}
```

You can then use this component like this:

```
const data = {
  "@context": "http://json-ld.org/contexts/person.jsonld",
  "@id": "http://dbpedia.org/resource/John_Lennon",
  name: "John Lennon",
  born: "1940-10-09",
  spouse: "http://dbpedia.org/resource/Cynthia_Lennon"
};

const App = () =>
  <body>
    <h1>Hello World</h1>
    <p>Lorem ipsum dolor sit amet</p>
    <JsonLd data={data} />
  </body>;
```

If you would have naively done this, you would expect to escape the brackets (`\{`), but it's easier if you render the `JSON.stringify` output for the content of the `script`.
