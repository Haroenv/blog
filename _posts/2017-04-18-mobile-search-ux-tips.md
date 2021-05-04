---
layout: post
date: 2017-04-18 17:30
title: Mobile search UX tips
tags: [algolia,internship,ux,mobile,crosspost]
---

> I wrote a blog post on the Algolia blog: [Small but impactful search UX tips for mobile web](https://blog.algolia.com/mobile-search-ux-tips/)

---

As part of our annual tradition of giving a gift to the community, these past few weeks I was part of the team working to implement search inside of Yarn. During that time, I noticed some small quick-wins that could make our search boxes better, and today I’d like to share a few of them.

User experience is important at Algolia – both the developers who use our API and the end-users who use the products they build – and so we look a lot at how the tools we provide to developers can make it easy to create great UX.

One of our most recent projects, [react-instantsearch](https://community.algolia.com/instantsearch.js/react/), comes with many optimizations and we’ll highlight a few of them in this post.

### Submit UX

We use `<input type="search" />` because it allows us to take advantage of semantics for screen readers that tell the user it’s a search input, and it will also show a ? (magnifying glass icon) as the return button on Android. In Chrome and Safari this has more advantages, namely that it shows a search button on one side, and a clear button on the opposite side.

To get that functionality for everyone, react-instantsearch wraps the search box in a form, and includes two extra buttons: one with type reset to clear the input, and another with type submit that will be used if “search as you type” has been deactivated -we hide the latter with some css to avoid duplicating functionality.

<p data-height="265" data-theme-id="light" data-slug-hash="xqejjN" data-default-tab="js,result" data-user="Algolia" data-embed-version="2" data-pen-title="Default React InstantSearch layout" class="codepen">See the Pen <a href="https://codepen.io/Algolia/pen/xqejjN/">Default React InstantSearch layout</a> by Algoliamanager (<a href="https://codepen.io/Algolia">@Algolia</a>) on <a href="https://codepen.io">CodePen</a>.</p>

We only want to submit the form when a user types something, so we will put the “required” attribute on the input. That prevents a user from submitting an empty search. However the default result isn’t too beautiful:

<figure>
  <img src="https://blog-api.algolia.com/wp-content/uploads/2017/04/Screen-Shot-2017-04-05-at-15.25.49.png" alt="an input that has been submitted, but was required. It shows an error message 'Fill out this field'">
  <figcaption>A required input</figcaption>
</figure>

</div>

We can avoid this message showing up, but still avoid the submitting of the form, by adding the “novalidate” attribute to the form.

<p data-height="265" data-theme-id="light" data-slug-hash="PpgamQ" data-default-tab="html,result" data-user="Algolia" data-embed-version="2" data-pen-title="input type text vs input type search" class="codepen">See the Pen <a href="https://codepen.io/Algolia/pen/PpgamQ/">input type text vs input type search</a> by Algoliamanager (<a href="https://codepen.io/Algolia">@Algolia</a>) on <a href="https://codepen.io">CodePen</a>.</p>

### Button UX

Next, we can go further in improving the search box itself. On mobile, the submit button becomes more prominent, since it’s visible as the return key (on both iOS and Android). We would love to have something that has to do with search to be displayed there instead of return. On Android we already solved this, just by using input type=search, but iOS still shows “return”, because iOS requires the form to have an action. Search is available on the page we’re on, so we can leave the action attribute empty, and then it means the current page. This will cause the submit button to read “search” instead, and it will be translated to the language of the keyboard you’re using.

You can play around with the differences on all browsers in this codepen:

<p data-height="265" data-theme-id="light" data-slug-hash="LWvrOx" data-default-tab="html,result" data-user="Algolia" data-embed-version="2" data-pen-title="input type text vs input type search + forms" class="codepen">See the Pen <a href="https://codepen.io/Algolia/pen/LWvrOx/">input type text vs input type search + forms</a> by Algoliamanager (<a href="https://codepen.io/Algolia">@Algolia</a>) on <a href="https://codepen.io">CodePen</a>.</p>

### Don't forget to Blur

Don’t fret, we aren’t done with the search button yet. If you have a button that says search, you expect the search results to appear. Because we show the results in realtime, while you’re typing, we don’t need to calculate the results at this point, so pressing search now does nothing at all for users. We fix this by  
[blurring](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/blur) (which is the opposite of focusing) the search input. The keyboard will then be dismissed when you hit search, and you can see all of the results.

### No need for Autocorrect

Because Algolia [is typo-tolerant](https://yarnpkg.com/en/packages?q=alogliasearch), mobile-specific features like autocorrect become a bit obsolete. We don’t want to spend time undoing the suggestions by our browser to suggest other words, especially if you’re in a case like Yarn, where a lot of the packages have unique spelling that we don’t want to be corrected.

To disable autocorrect, you’ll need three attributes — `autocorrect=off`, `spellcheck=false`, and `autocapitalize=off` — the latter avoids starting a search with a capital letter all the time. With those improvements, a search on a mobile device will look like this:

<figure>
  <img src="https://cloud.githubusercontent.com/assets/6270048/23188400/dac82d2e-f88e-11e6-9d7e-b96c5437893f.gif" alt="image of an iPad that is focused on a search form. The return key says return and pressing it doesn't dismiss the keyboard">
  <figcaption>The situation before these improvements</figcaption>
</figure>

<figure>
  <img src="https://cloud.githubusercontent.com/assets/6270048/23188399/daad4b80-f88e-11e6-9895-df7d7443ad36.gif" alt="Image of an iPad with a search form, it's return key says 'search'">
  <figcaption>The situation after these improvements</figcaption>
</figure>

A last thing that has been added is the “role” added to the form. Since December of 2015 , with [html-aria#18](https://github.com/w3c/html-aria/issues/18), it’s valid html5 to add an additional role to a form, and in this case a search role makes a lot of sense. In screen readers that support it, the search input will be read as a search form with inputs, and that’s exactly what we want.

With all those things  implemented in [react-instantsearch](https://community.algolia.com/instantsearch.js/react/) in  
[instantsearch.js#1999](https://github.com/algolia/instantsearch.js/pull/1999) and [instantsearch.js#2046](https://github.com/algolia/instantsearch.js/pull/2046), we get a search form that looks like this:

<p data-height="390" data-theme-id="light" data-slug-hash="ZeZRRE" data-default-tab="html,result" data-user="Algolia" data-embed-version="2" data-pen-title="React InstantSearch SearchBox" class="codepen">See the Pen <a href="https://codepen.io/Algolia/pen/ZeZRRE/">React InstantSearch SearchBox</a> by Algoliamanager (<a href="https://codepen.io/Algolia">@Algolia</a>) on <a href="https://codepen.io">CodePen</a>.</p>

You can get a search box like this one by using react-instantsearch to make your search experience, or apply this knowledge yourself.

When making the search for Yarn a few other things came to my attention —I’d like to thank [James Kyle](http://thejameskyle.com) a lot, because he kept finding new things to give me feedback on. One of these is stylistic, and that is to always make sure your search input stands out from the background. You can do that by making sure it has a white (or light) background, a placeholder that’s not too light and not too dark. You should add an identifiable  icon (for example ?) to get extra clarity, and it’s also good practice to give a special border to active inputs. My colleague [Kevin Granger](https://github.com/shipow) made a really cool webapp that allows you to create all kinds of search boxes that follow these criteria at [http://shipow.github.io/searchbox](http://shipow.github.io/searchbox).

### OpenSearch

<figure>
  <img src="https://blog-api.algolia.com/wp-content/uploads/2017/04/ezgif-2-12bc36fde1.gif" alt="a browser with a focused URL bar, once 'yarn' is typed, and then a tab, followed by a keyword, then enter, the keywords get searched in">
  <figcaption>OpenSearch in action on the <a href="https://yarnpkg.com/en/packages">Yarn site</a></figcaption>
</figure>

Another thing I learned about while making search for Yarn is the [OpenSearch](http://opensearch.org) spec. It was developed by a9 (which is a subsidiary of Amazon) a long time ago, and deals with a lot of browser and search functionality. You can make your whole search available in the dropdown that comes up when you use “search in site”. Making your search available in the rss format that opensearch expects isn’t what Algolia is made for right now, but we can make browsers handle the “search in site” feature. To do that we have to add a `<link rel=search` to the `<head>` of every page. In that we add a `href="/opensearch.xml"` and `type="application/opensearchdescription+xml"`, a `title="name of your site"` is also added to show up in the UI of browsers correctly. The /opensearch.xml file should contain something like this:

```xml
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/" xmlns:moz="http://www.mozilla.org/2006/browser/search/">
  <ShortName>Yarn</ShortName>
  <Description>Package Search</Description>
  <Url type="text/html" method="get" template="https://www.yarnpkg.com/en/packages?q={searchTerms}" />
  <InputEncoding>UTF-8</InputEncoding>
  <Image height="32" width="32" type="image/x-icon">https://yarnpkg.com/favicon.ico</Image>
</OpenSearchDescription>
```

You can read more about the implementation of OpenSearch in [Chrome](http://dev.chromium.org/tab-to-search), [Firefox](https://developer.mozilla.org/en/Add-ons/Creating_OpenSearch_plugins_for_Firefox), [Safari](https://developer.apple.com/library/content/releasenotes/General/WhatsNewInSafari/Articles/Safari_8_0.html), [Internet Explorer](<https://msdn.microsoft.com/library/dn832639(v=vs.85).aspx>), [Yandex](https://yandex.com/support/browser/search-and-browse/search.xml) and [in general](http://www.opensearch.org).

### The Devil is in the Details

I enjoyed discovering these quick fixes that get a search experience from good to great, and hope they help you create beautiful search for your users. If you have any questions about the tips above, or have UX tips of your own, we’d love to discuss this more with you on the [Algolia forum](http://discourse.algolia.com).

<script async src="https://production-assets.codepen.io/assets/embed/ei.js"></script>
