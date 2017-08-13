---
layout: post
title: Nearing the end
date: 2017-05-01 12:00
tags: [algolia,internship,yarn,]
---
Sorry that I have not been updating that regularly, it must have slipped my mind a lot (since I had to update the data of this post at least three times already). Let's just go for a summary of things I've done in the missing period: 

# Yarn

The detail page is proving a big success with regularly about 70 000 daily searches (up from 4 000 in January and 40 000 in February), which has been because of some improvements made recently. I've worked together with [Daniel](https://github.com/Daniel15) to make file listings and added versions because [Konstantin](https://github.com/bestander) suggested it. 

Interestingly when Konstantin [tweeted](https://twitter.com/bestander_nz/status/858030031343374336) about the addition of versions, there were even 107 000 searches that day. Glad it was pretty simple to add. 

I also did some contributions to the [indexer](https://github.com/algolia/npm-search) for Yarn, [one](https://github.com/algolia/npm-search/pull/38) for adding the versions, and [another](https://github.com/algolia/npm-search/pull/40) for adding a way to redo the bootstrap weekly. There is also one for [cleanup](https://github.com/algolia/npm-search/pull/39), plus a few hotfixes.

I also experimented with SEO in a few ways. The first is a generic Algolia sitemap generator, which you can find on [GitHub](https://github.com/algolia/algolia-sitemap) or [Yarn](https://yarnpkg.com/zh-Hans/package/algolia-sitemap). It uses the [browse](https://www.algolia.com/doc/api-client/javascript/advanced/#backup--export-an-index) feature of Algolia, then creates a sitemap using a function to create links -- with support for several languages -- and aggregates all of the created sitemaps in a [sitemap index](https://support.google.com/webmasters/answer/75712?hl=en). 

I applied this experiment to Yarn, giving it all the detail pages. I used my package to have a [script](https://github.com/yarnpkg/website/blob/master/scripts/sitemaps.js) that runs when the site is being created, and takes about a minute. After submitting this sitemap to Google, all pages are marked as "existing", but not yet indexed. 

{% include
	image.html
	img='sitemap.png'
	alt='470k pages in sitemaps' 
%}

Regarding that, I made some changes that make the rendering work *slightly* better in some conditions, by adding polyfills when needed and prerendering when needed. Unfortunately Google doesn't work with prerendering, so it doesn't look as nice as it could yet, but we'll find a solution. 

{% include
	image.html
	img='google-before.png'
	alt='before optimisations' 
%}

{% include
	image.html
	img='google-after.png'
	alt='after optimisations' 
%}

As you can see, Googlebot is still being annoying, but at least the "how users would see your page" has improved. 

All commits since last update are [here](https://github.com/yarnpkg/website/commits?author=Haroenv&since=2017-04-07T22:00:00Z&until=2017-05-01T22:00:00Z)

# React InstantSearch

The last thing I've done is regarding to someone building a # mention component. In the end there was a bug in our `connectAutoComplete` implementation. It assumed that we were in a multi-index context, but that isn't always the case. You can read all about it in [#71](https://github.com/algolia/react-instantsearch/issues/71), [#74](https://github.com/algolia/react-instantsearch/issues/74) and [#75](https://github.com/algolia/react-instantsearch/issues/75). In the end this was the result: 

{% include
	image.html
	img='autocomplete.gif'
	alt='hashtag suggestion with Algolia and React Instantsearch.' 
%}

You can find all my other pull requests to React InstantSearch [here](https://github.com/algolia/react-instantsearch/pulls?utf8=✓&q=is%3Apr%20author%3AHaroenv%20)

{% include
	image.html
	img='ris-prs.png'
	alt='Pull requests to React InstantSearch' 
%}

# InstantSearch.js

This might have been a bit longer ago already (around April 6th), but InstantSearch.js is busy with the v2 release, where I've been a part of. Mostly in meetings and thinking together about APIs, but also in code ([#2107](https://github.com/algolia/instantsearch.js/pull/2107)). 

InstantSearch.js now also has connectors like React InstantSearch, and the plan is to at some point (probably v3) to unify them completely and publish the connectors as a dependency for both (and probably all) InstantSearch projects, but that's _future music_ for now. 

# Other

There's a lot of other projects I've done smaller work on, among others making [create-next-app](https://github.com/segmentio/create-next-app) work properly with Yarn, improvements in our documentation and dashboard. Here's a non-exhaustive overview:

{% include
	image.html
	img='cra-prs.png'
	alt='Pull requests to Create Next App' 
%}

{% include
	image.html
	img='doc-prs.png'
	alt='Pull requests to Documentation' 
%}

{% include
	image.html
	img='web-prs.png'
	alt='Pull requests to Algolia Dashboard' 
%}

I also reviewed a lot of pull requests in this period: 

{% include
	image.html
	img='reviews.png'
	alt='Pull requests reviewed by me' 
%}
