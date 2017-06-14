---
title: An update from Bois de Vincennes
date: 2017-02-18 15:50
layout: post
tags: [algolia,internship]
---
Time goes so fast when you're busy, already two weeks over. I've been working on two sides. On one hand I am getting into improving [react-instantearch](https://community.algolia.com/instantsearch.js/react/), and on the other I'm busy improving the search experience of [yarn](https://yarnpkg.com/search). 

Right now the website of yarn uses [instantsearch.js](https://community.algolia.com/instantsearch.js/) as a way of searching. That uses (p)react behind the scenes, but it isn't exposed to the user. Instead you search either using widgets, or changing things in the [helper](https://github.com/algolia/algoliasearch-helper-js) directly. Although this is very powerful and flexible, you can get the feeling you don't have much feeling with the widgets directly, and you can be making very complex to understand logic. 

As discussed before I joined, I moved the searchbar to be visible at all times, and switch to react-instantsearch. For that some tooling was set up ([#375](https://github.com/yarnpkg/website/pull/375)). Once that was merged I could start moving the searchbar and changing its logic. This was not an easy process, mostly because of the flexibility of instantsearch.js. In the end I'm proud of the result ([#383](https://github.com/yarnpkg/website/pull/383)) that took me most of the week and 92 commits. 

I've realised that it won't be easy to make a structure that's both abstracting away the logic of search actions, but still easy to understand and implement. React-instantsearch solves this by having two structures. One is [widgets](https://community.algolia.com/instantsearch.js/react/widgets/), and the other is [connectors](https://community.algolia.com/instantsearch.js/react/connectors). A widget has the limitation that it gives a user very little control of finer details or edgecases, a connector has a bigger disadvantage in my opinion. Because by default it doesn't assume anything about how you use it, you will have to reimplement the logic of the component. 

An ideal solution to me would be to only make connectors, but lots of them that can do a lot, and document them really well. These connectors can be reused regardless of framework, since all they do is a certain algolia refinement. Things like toggling a refinement, putting one or searching are the actions that should be done. Another thing that should be made is a redux-like datastore that has a state at all times that is the current results. 

As a separate project components that use those connectors can be made in various frameworks. 

In the instantsearch front I've started by improving things in documentation ([#1966](https://github.com/algolia/instantsearch.js/pull/1966), [#1974](https://github.com/algolia/instantsearch.js/pull/1974), [#1982](https://github.com/algolia/instantsearch.js/pull/1982)), fixed a bug in Safari ([#1970](https://github.com/algolia/instantsearch.js/pull/1970)), update the poweredBy component ([#1978](https://github.com/algolia/instantsearch.js/pull/1978) and made how to translate clearer in the [storybook](https://community.algolia.com/instantsearch.js/react/storybook/?knob-translate=%7B%22submit%22%3Anull%2C%22reset%22%3Anull%2C%22submitTitle%22%3A%22Submit%20your%20search%20query.%22%2C%22resetTitle%22%3A%22Clear%20your%20search%20query.%22%2C%22placeholder%22%3A%22Search%20your%20website.%22%7D&selectedKind=SearchBox&selectedStory=playground&full=0&down=1&left=1&panelRight=1&downPanel=kadirahq%2Fstorybook-addon-knobs) ([#1980](https://github.com/algolia/instantsearch.js/pull/1980)). A pull request that isn't merged yet is my "first real code contribution" to react-instantsearch. It allows to use custom components as the search and submit button content ([#1991](https://github.com/algolia/instantsearch.js/pull/1991)). 

I've also done some contributions to the documentation of other Algolia projects while reading through them. 
