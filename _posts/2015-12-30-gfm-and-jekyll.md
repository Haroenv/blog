---
layout: post
title: GFM and Jekyll
date: 2015-12-30 13:36
tags: [jekyll, github]
redirect-from:
  - /2015/12/30/GFM-and-Jekyll.html
---

UPDATE 2/2/2016: GitHub switched to Jekyll 3.0 for `gh-pages`. This means you can now use this in your `_config.yml`

They now use `rouge` and `kramdown` by default. *Old* highlighting still works, but backticked codefencing seems to be the new preferred way. Unfortunately I've noticed that this doesn't work for me.

Now, instead of

{% highlight html %}
<pre><code>...</code></pre>
{% endhighlight %}

code is embedded in

{% highlight html %}
<figure class="highlight">
  <pre><code class="language-yaml" data-lang="yaml">...
  </code></pre>
</figure>
{% endhighlight %}

Make sure that your styling for `figure.highlight`, doesn't change the alignment.

Source: <https://github.com/blog/2100-github-pages-now-faster-and-simpler-with-jekyll-3-0>

---


In short words: don't do it.

Although Jekyll is supposed to make writing blogs easier and more straight-forward (which it mostly does), but code highlighting will make your head scratch a bit.

I tried using

{% highlight liquid %}
```css
.selector {
  display: none;
}
```
{% endhighlight %}

And putting

{% highlight yaml %}
kramdown:
  input: GFM
{% endhighlight %}

But that put my fenced codeblocks simply in a `code` tag. This doesn't help with highlighting, so I wasn't happy.

The real solution is to not try to use GFM and do it with [rouge](http://rouge.jneen.net) or [pygments](http://pygments.org). For that to work locally you need to make sure you've got that gem installed (`gem install rouge`), and then in your `_config.yml` put:

{% highlight yaml %}
highlighter: pygments
{% endhighlight %}

After that you can highlight your code blocks with the rouge filter:

{% highlight liquid %}
{% raw %}
{% highlight yaml %}
kramdown:
  input: GFM
{% endhighlight %}
{% endraw %}
{% endhighlight %}

Additionally, this will only add the proper classes to the `<pre><code>...</code></pre>`-block. You'll need to add a stylesheet yourself, like for example [this one](https://github.com/richleland/pygments-css) from Pygments compiled by @richleland.

You can add some other gems like `jekyll-mentions` to get github `@-mentions` in your blog.

{% highlight yaml %}
gems:
  - 'jekyll-mentions'
{% endhighlight %}
