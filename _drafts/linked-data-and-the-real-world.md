---
title: Linked data and the real world
layout: post
tags: [open data, linked data]
---

So I've worked at [open Summer of code](http://2016.summerofcode.be) for the month of July this year (2016) — something I can really encourage for every Belgian IT student by the way — focusing on linked data and its encouragement to legislators (delivering the new homepage of [vocab.datex.org](http://vocab.datex.org)). These are some of my considerations and questions I'd love to see answered in the future. As a disclaimer: all the following opinions are my own and in no way represent any official opinion.

The interesting thing about linked data[^1] is that it's useful for two major reasons. The first one is semantic interoperability, and the second one is _linkability_.

Semantic interoperability is maybe the concept I like most of all. Thanks to requiring an ontology (vocabulary) for each term the data become more logical without a lot of effort. Imagine %%

On the other hand we have the _linkability_. What I mean by this is the principles of [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) applied to the whole internet of things. This means that every identity, be it a `servicePoint`, a `accident` or a restaurant dish all have to have a unique identifier. However having a identifier isn't enough. This identifier needs to be a [URI](http://www.w3.org/Provider/Style/URI) — basically a url that doesn't change — and thus requires you to not only send the raw data, but requires at least a minimal page that gives some explanation for every term.

There is however a workaround for this. You can link your data inside the same page. Let's say you've got a dataset containing data about the accidents in a region[^2]. You can use [datex](http://vocab.datex.org) to create a single vocabulary. We'll host this JSON-ld feed at `https://verkeerscentrum.be/data.jsonld` to keep things simple and just a file.

<!--there are zero width spaces after each@ -->

```json
{
  "@context": {
    "@vocab": "http://vocab.datex.org/terms#"
  },
  "@graph": [
    {
      "@id": "https://verkeerscentrum.be/data.jsonld#123a1592ef2bac",
      "@type": "Situation",
      "Accident": {}
    },
    {}
  ]
}
```

[^1]: if you're not familiar with linked data, check out the JSON-ld and RDFa tutorials on [vocab.datex.org](http://vocab.datex.org).
[^2]: This is a real example. You can use [`datex2-linker`](https://github.com/osoc16/datex2-linker) to create a JSON-ld feed from their [`datex`](http://www.verkeerscentrum.be/uitwisseling/datex2full) feed.
