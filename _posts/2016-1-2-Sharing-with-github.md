---
title: Sharing With GitHub
layout: post
date: 2016-1-2 16:30
---
Building a simple link/image/site sharing service with github is pretty easy. My own version is visible at [s.haroen.me](https://s.haroen.me).

This requires knowledge of:

* git
* github pages
* private repositories

## What it actually is

It's a github pages repository, so it's built on [jekyll](https://jekyllrb.org) which is set as private. Because the generated sites are still public with private repositories, this is the perfect place to store images you don't want someone stumbling upon, but still want to share them.

This could by extension also be some joke site you quickly made. Examples of that are [s.haroen.me/ex](https://s.haroen.me/ex) for a quick reference of exam dates, [s.haroen.me/click](https://s.haroen.me/click) for quickly sharing a gif, a font [s.haroen.me/BLOKKNeue-Regular.ttf](https://s.haroen.me/BLOKKNeue-Regular.ttf) or jokes like [s.haroen.me/👌](https://s.haroen.me/👌).

## How it works

Make a new private repository with only a `gh-pages` branch (tip: if you're a [student](https://education.github.com/pack), you get 5 free private repositories from GitHub). The structure of that could look like this:

```
/
  index.html
  click/
    index.html
    style.css
    click.gif
  ex/
    index.html
    2016-januari.html
    2016-januari.pdf
  👌/
    index.html
```

## Link shortening

Using this method you can also make your own shortlinks of the form `s.haroen.me/shortlink`, like [s.haroen.me/db](https://s.haroen.me/db). The content of the file [`/db/index.html`](https://s.haroen.me/db) is this:

{% highlight html %}
<!DOCTYPE HTML>
<meta charset='UTF-8' />
<meta http-equiv='refresh' content='1' url='https://github.com/Haroenv/notes-1eoict/blob/master/Databanken/samenvatting.md' />
<script>
  window.location.href = 'https://github.com/Haroenv/notes-1eoict/blob/master/Databanken/samenvatting.md'
</script>
<title>Page Redirection</title>
If you are not redirected automatically, follow the <a href='https://github.com/Haroenv/notes-1eoict/blob/master/Databanken/samenvatting.md' />link.</a>
{% endhighlight %}

This uses three different ways to redirect:

* the `http-equiv='refresh'` meta-tag
* `window.location.href` in javascript
* a link

This will work on basically every browser. A major advantage of this method is that the browser will have to load this page, and only when it's parsed, it will go to the site you want to go to. To fix that issue, you'll have to do this server-side. Unfortunately github pages doesn't offer you a way to mess with the server-side, so this is your only option.

## subdomain

I personally find `s.haroen.me` more pleasing to read than `haroen.me/s`. You can achieve this by setting a `CNAME` file in the root of your repository with the contents `s.haroen.me`.

The next thing you need to do is add a `CNAME` record to your DNS provider like this:

```
s 10800 IN CNAME Haroenv.github.io.
```

This will make your site availaible at both `s.haroen.me/ex` as `haroen.me/s/ex`