---
title: Canceling asynchronous operations nicely
date: 2017-12-21
layout: post
tags: [algolia,javascript,asynchronous,react]
---

# Introduction

Browser engines and Node.js have always been asynchronous. This is why we are able to have high concurrency of operations while each of the operations only has a single thread.

* elaborate a bit based on the talk

While the idea of asynchronous operations has always been part of the core of using JavaScript, it wasn't until recently that there has been a language feature to describe that a certain result isn't immediately available. Nowadays there are two _main_ ways to make sure an operation is not making the rest of the program wait: callbacks and Promises.

Making sure something happens asynchronously is one thing, but imagine the following case. You are writing a single page app which draws a nice picture based on what the camera sees. This picture is being drawn to the canvas, which might take 10ms or a few seconds depending on how big the source image i. Which is why this calculation is done asynchronous, with a Promise or a callback. If someone changes their page though and the image isn't visible anymore, we want to cancel that calculation, because it will consume resources for the users, while they've already decided that they don't want to see the picture, or whatever you already shown was enough for them.

Another example is when you're making network requests. When

* requests that depend on eachother,
* no need to complete older requests
* sometimes you need to complete older requests for cache
* adding a timeout

# callbacks

* whatever returned from the function will have a way to cancel it, like `setInterval`
* only used by repeating operations, not one-off long running operations
* usually has options for timeout (like XHR), but what do they _really_ mean?

# Promises

* Oops, we already return a Promise, we can wrap it so the promise is not the main return
* something else returned will have a way to cancel things
* but what about when using `async` functions, they return a simple Promise

# fetch

* original github issues
* has no timeout
* timeout seen as part of userland
* timeout vs deadline
* making Promises be abortable by default
* TC39 annoyingness

# AbortController

* What can you do if you stay in userland
* separation of something that will abort things and things that can be aborted
* `fetch` first implementer
* other web APIs also support it

Externally you make "something" which can abort other things (i.e. control them), an `AbortController`. This controller has a signal it can pass around to everything it needs to control, and a method called `abort`, to send an event to all signals that it would like those operations to cancel. Each of the signals is an {todo: what's the name} EventEmitter, which you might recognise from working with DOM events.

Similarly to those, you can also subscribe to an event with `addEventListener('abort', callback)` or `onabort(callback)`. Inside the function which accepts an AbortSignal, you will subscribe to the `abort` event sent by the controller. Once that's been fired, you do whatever you can/need to actually abort the operations you're doing.

# imperative vs declarative

* nice that you can abort remotely
*

# React

```jsx
<Fetch
  url="http://google.com/"
  method="POST"
  headers={{
    'Accept-Encoding': 'application/json',
  }}
  render={({ data, error }) => <div>{JSON.stringify({ data, error })}</div>}
/>
```

* so we add a signal prop?

```jsx
<Fetch
  url="http://google.com/"
  method="POST"
  headers={{
    'Accept-Encoding': 'application/json',
  }}
  signal={abortSignal}
  render={({ data, error }) => <div>{JSON.stringify({ data, error })}</div>}
/>
```

# solution?

* allow `abort` prop to be set to true
* is that even good
* what about refresh in higher level comps

# Read more

If you want to read more about the ideas in this post, there are a few posts and informational documents by others that influenced me while researching about this topic:

* [concurrent operations jsconf bp]()
* [Mozilla Dev Network on AbortController]()
* [google blog AbortController]()
* [bramus post AbortController]()
* [render prop mjackson]()
