---
title: 'Yarn: From Zero to 700,000 User Searches per Month'
date: 2017-11-09
layout: post
tags: [algolia,yarn,crosspost]
---

> A blog post me and [Vincent](https://twitter.com/vvoyer) wrote is up on the Algolia blog [here](https://blog.algolia.com/yarn-search-javascript-packages/).

---

Since December 2016, as part of our yearly community gift effort, Algolia has powered the [JavaScript packages search](https://yarnpkg.com/en/packages) of the Yarn website. This blog post explains how we collaborated with the Yarn team, what the challenges were building such a search interface, and how much this search is used today.

[Yarn](https://yarnpkg.com/en/) is a JavaScript package manager similar to [npm](http://npmjs.com/). In the beginning, there was no way to search for JavaScript packages on the Yarn website. Since we were heavy users of Yarn, in December 2016 we built a proof-of-concept search UI, and it was released on their website one month later ([Try it here!](https://yarnpkg.com/en/packages?q=react&p=1)). As of today, every month there are about 500,000 searches _(that's 2.3M API calls)_ being done on the Yarn JavaScript packages index on Algolia.

<figure>
  <img src="https://blog.algolia.com/wp-content/uploads/2017/11/image5-1.png" alt="1 - 1.5 million searches a month">
  <figcaption>number of user searches per month on the Yarn website</figcaption>
</figure>

## From a Slack discussion to PR and Merge. All in one month.

Search on the Yarn website started with the documentation. We wanted people to easily find information on how to use Yarn. As with 300 other programming community websites, we went for Algolia’s [DocSearch](https://github.com/algolia/docsearch) and this was merged in [yarnpkg/website#105](https://github.com/yarnpkg/website/pull/105). Then another Yarn contributor ([@thejameskyle](https://twitter.com/thejameskyle)) asked in [yarnpkg/website#194](https://github.com/yarnpkg/website/issues/194) if there should be package searching abilities, much like npm had.

This is where [Algolia](https://www.algolia.com/) came into play. We are a search engine, Yarn wants search and we are heavy users of Yarn, so we figured: let’s do this!

This is how it started on December 5th in our #2016-community-gift Slack channel:

* "Hey what could we build for the JavaScript community that would help them in their daily workflow?"
* "It’s not that easy to find relevant JavaScript packages when you need one"
* "I like Yarn a lot…"
* "Let’s build Yarn search!"

We wanted the community to feel empowered by a great new way to search for JavaScript packages. This was also an opportunity for us to work on something cool while benefiting the company. Three weeks later, on December 22th 2016, via [yarnpkg/website#322](https://github.com/yarnpkg/website/puls/322), we proposed our first package search solution. Ten days later it got merged, and instant-search for JavaScript packages was available on the Yarn website.

In early 2017, we met with the Yarn team for a one day in-person brainstorming in London. The goal was to think about evolutions of the search experience along with defining a package details page. Algolia proposed design views of what search could be and from that we drafted a [master plan](https://gist.github.com/vvo/c801fb8b653eda9fb17de60987476b5e).

## Features behind a great package search

### It shows results instantly ⚡️

<figure>
  <img src="https://blog.algolia.com/wp-content/uploads/2017/11/image2.gif" alt="Yarn search - instant results">
  <figcaption>^ This is not sped up. It is THAT fast (<a href="https://yarnpkg.com/en/packages?q=babel">try it</a>!). Yes, it still wows even us every time.</figcaption>
</figure>

Instead of showing a dropdown of results, we chose to replace the page completely with the search results. This requires more data to be available immediately, but gives more context on the decisions you make while searching for a fitting package. Having the search page be the main entry point will make sure that you don’t need to know exactly what you want before “committing” to a search.

### It displays a lot of metadata

After using npm search many times, we knew what was missing and what was superfluous from the search results and package detail pages. We brainstormed a bit and iteratively added a lot of useful metadata.

Here’s a comparison between the two search results pages (npm on the left, Yarn on the right):

<figure>
  <img src="https://blog.algolia.com/wp-content/uploads/2017/11/image4-1.png" alt="search showing downloads, GitHub stargazers, and more">
  <figcaption>Comparison between the npm search page on the left, Yarn search page on the right</figcaption>
</figure>

_npm search results on the left, Yarn search results on the right (click to enlarge)_

In the search results of Yarn we decided to directly display, for example, the number of downloads for every packages, the license, direct links to GitHub, and the owning organization.

This metadata helps the user to not have to open many package detail pages before getting the information they want.

### It has completely rethought package detail pages

For the package detail page, we took a similar approach. We started with the same base metadata as npm shows, but also took the opportunity to add a lot more. We decided to show changelogs (when available), GitHub stargazers, commit activity, deprecation messages, dependencies and file browsing.

Here’s what it looks like:

<figure>
  <img src="https://blog.algolia.com/wp-content/uploads/2017/11/image1-1.png" alt="detail showing changelogs, GitHub stargazers, and more">
  <figcaption>Comparison between the npm detail page on the left, Yarn detail page on the right</figcaption>
</figure>

We believe (and we had a lot of feedback about it) that all those additions are providing an enhanced experience that helps users when finding and comparing JavaScript packages.

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">TIL yarn has a responsive package details page<a href="https://t.co/w2QkQoDP9P">https://t.co/w2QkQoDP9P</a> <a href="https://t.co/wBnQ9biD85">pic.twitter.com/wBnQ9biD85</a></p>&mdash; John-David Dalton (@jdalton) <a href="https://twitter.com/jdalton/status/847590769078583297?ref_src=twsrc%5Etfw">March 30, 2017</a></blockquote>

This is an iterative process, and suggestions and feedback [are always welcome.](https://github.com/yarnpkg/website)

## Technical implementation and challenges

The first step to providing a search for JavaScript packages is to replicate and monitor changes from the npm registry into an Algolia index.

The code for this replication is all open source and available at [algolia/npm-search](https://github.com/algolia/npm-search). The most important API being used here is the [npm replication API](https://docs.npmjs.com/misc/registry).

The npm registry is exposed as a [CouchDB database](http://couchdb.apache.org/), which has a [replication protocol](http://docs.couchdb.org/en/master/replication/protocol.html) that can be used to either set up your own npm registry, or in our case a service (the Algolia index) that has the same data as the npm registry.

### Replicating the npm registry

Replication in CouchDB is a very simple but powerful system that assigns an “update sequence” (a number) to any changes made on a database. Then, to replicate a database and stay in sync, you only need to go from the update sequence 0 (zero) to the last update sequence, while also saving the last update sequence you replicated on your end. For example, right now, the last update sequence known on the npm registry is 5647452 (more than five million changes).

Early on we saw that going from 0 to 5647452 was very slow (multiple hours) and we wanted it to be faster. So, we made a replication system consisting of three phases:

The bootstrap. Instead of going over all update sequences, we save the current last sequence, then we list all JavaScript packages and replicate them by bulk to Algolia

1. The catch-up. Starting from our last known update sequence, we catch up to the new last update sequence of npm (maybe 5000 changes since bootstrap start, which is fast)
2. The watch. Once we are “up to date” then we just watch the npm repository for any new changes and we replicate them

For all of those phases, we use the [PouchDB](https://pouchdb.com/) module which we recommend because it has an awesome API to interact with CouchDB databases.

### Getting the necessary metadata

All the phases go through ​the same steps to get the required metadata for displaying. Some of the metadata is also retrieved on the frontend directly, like the GitHub ones (stargazers, commit activity).

Here are all our sources:

* npm registry, example for express: [http://registry.npmjs.org/express](http://registry.npmjs.org/express)
* npm download counts: the [npm downloads endpoint](https://github.com/npm/registry/blob/master/docs/download-counts.md)
* Packages’ dependents: the [dependents endpoint of npm](https://github.com/algolia/npm-search/blob/764ee8561819d4deeba7757acedc2d441da938e6/npm.js#L100-L118) (there’s no official documentation on that)
* Changelogs: a [clever](https://github.com/algolia/npm-search/blob/764ee8561819d4deeba7757acedc2d441da938e6/github.js#L18-L35) first resolved, first served list of calls to various ChAnGeloG files, like [History.md’s express changelog](https://raw.githubusercontent.com/expressjs/express/master/History.md)
* GitHub Stargazers<span style="font-weight: 400;">⭐️</span>, commit activity: we get them on the frontend directly from GitHub using the browser of the person doing a search. This way we benefit from a larger rate limit on GitHub <span style="font-weight: 400;">shared amongst all users.</span> This is also what npm search does for opened issues on their detail pages.
* Browse view: we get this from the [unpkg](https://unpkg.com) API, which gives us the files, folders and sizes for all published packages

### Query Rules to the rescue

There are a lot of Algolia features baked in our JavaScript packages search index; you can see the whole index settings [in our repo](https://github.com/algolia/npm-search/blob/master/config.js#L13-L54).

One of them that really helped us is [Query Rules](https://www.algolia.com/doc/guides/query-rules/query-rules-overview/). When you are searching for a package, there are two questions to answer: the package that you exactly typed, and the package that you probably typed. We found that other searches often don’t have what you typed exactly early in the results, even though it exists.

What we have as a solution is a query rule that applies when the user types the name of a package exactly or without special characters (to allow people affordance in how they type dashes).

<figure>
  <img src="https://blog.algolia.com/wp-content/uploads/2017/11/image3-2.png" alt="Algolia dashboard that shows a query rules to boost exact matches">
  <figcaption>Example query rule to boost exact matches</figcaption>
</figure>

This allows a query like `reactnative` to have as first result `react-native` which is very popular, and as second result `reactnative`, which is deprecated and not supposed to be used, but still exactly what the user typed and may be looking for.

For a package search, we can’t make any assumptions like “Maybe the user was looking for this package instead of what they typed”. Instead we want to always present them both the exact package match if any and then the popular ones.

## The future of Yarn search

A big part of our success was made possible because we opened the JavaScript package search to multiple websites and applications (which is another milestone for us!), namely:

* [Yarn](https://yarnpkg.com/en/) (65% of searches)
* [jsDelivr](https://www.jsdelivr.com/), the free Open Source CDN (10% of searches) [serving one billion downloads](https://blog.algolia.com/serving-one-billion-javascript-library-downloads/) per month of our libraries
* [Atom autocomplete module import](https://blog.algolia.com/atom-plugin-install-npm-module/)

We will soon open the JavaScript package search API to more websites and make it an official community project. The plan is to create a single page documentation for anyone to reuse this JavaScript search API in their applications. From editor plugins to community websites like [CodeSandbox](https://codesandbox.io/), we know the demand for an easy-to-use and instant package search is high.

Building on that we want to add new features like:

* Bundle size information like [siddharthkp/bundlesize](https://github.com/siddharthkp/bundlesize)
* Advanced filtering with tags
* Anything YOU would like to see, [let us know](https://github.com/algolia/npm-search/issues)

We did not stop at the search feature. I am proud to be a [frequent contributor](https://github.com/yarnpkg/website/graphs/contributors) to the Yarn website, helping on adding translations, reviewing or merging PRs and updating the Yarn cli documentation.

## Thanks

This project wouldn’t have been feasible without the help of everyone from the Yarn and Algolia teams. Since our first contact with the Yarn team, communication has always been great and allowed everyone to feel confident about shipping new features to the Yarn website.

We also want to thank very much the npm team for being responsive and advising us while we were building our replication mechanism.

We hope you enjoyed this article, see you soon for this year’s community gift 🎁!

_Thanks to [Vincent](https://twitter.com/vvoyer) and [Ivana](https://twitter.com/voiceofivana) for their help while writing this article._

<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 