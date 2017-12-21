---
layout: post
date: 2017-04-10 22:34
title: Other things
tags: [algolia,internship]
---

These last two weeks were different than the other ones, because Yarn now definitely became a lower priority for me. This is mostly because work on InstantSearch Core comes in a different gear now. So what does the proposed API look like for now?

1. make an algoliasearch client
2. make a new store
3. make a refinement
4. link them together
5. change the state of a refinement
6. listen to changes

So why is this actually needed? Why can't we just use the [helper](https://yarnpkg.com/en/package/algoliasearch-helper)? It all comes down to keeping state of a certain attribute together and easily changeable.

Our state "schema" is as follows. A plain object with two keys. A first one is the one we track in user space, and is the one that you change, that one is called `refinements`. It is subdivided per attribute name, as well as adding a `__raw` key for Algolia parameters that don't fit under certain attribute.

Each attribute can have multiple refinements, think things like `range`, `refinementList`, `toggle` ... which have one or multiple options.

The second key in the state is the `results` key. That one is only supposed to writable by an Algolia client, because it will always store the results of the latest refinement.

```js
import store from './store';

const state = {
  refinements: {
    // a certain attribute name
    price: {
      range: {
        min: 0,
        max: 10,
      },
    },
    // raw Algolia parameters
    __raw: {
      distinct: true,
    },
  },
  results: {
    // whatever Algolia returns
  },
};

if (store.getState() === state) {
  // yes, they're equal
}
```

More details are available on the [InstantSearch Core](https://github.com/algolia/instantsearch-core) GitHub repository, which is private for now, but will be public as soon as it's released. You can ask for sneak peeks if you really want to though 😜.

Two weeks ago Thursday there was an "offsite-but-not-really-offsite" with everyone of the engineering department where we reflected on Q1 and how things can be improved, especially now that we're growing so fast. Having great libraries is a start, but managing them is a wholly different issue. Handling support tickets, feature requests and bug reports for all parts of the company is something we all deal with. Of course it isn't as easy as saying "oh yes, we need more mailboxes" or whatever. A truy good solution is hard to find, but it does mainly come down to better internal communication.

The other passed Thursday it was a real offsite, where we went and did a "treasure hunt" in the Louvre, which was nice to get to know other people of the company you don't really talk to often.
