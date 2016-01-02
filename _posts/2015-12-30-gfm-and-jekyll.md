---
layout: post
title: GFM and Jekyll
date: 2015-12-30 13:36
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

Additionally, this will only add the proper classes to the `<pre><code>`-block. You'll need to add a stylesheet yourself, like for example [this one](https://github.com/richleland/pygments-css) from Pygments compiled by @richleland.

You can add some other gems like `jekyll-mentions` to get github `@-mentions` in your blog.

{% highlight yaml %}
gems:
  - 'jekyll-mentions'
{% endhighlight %}