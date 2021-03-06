---
layout: post
title: Any gems on Github Pages
date: 2016-03-02 13:24
tags: [jekyll, github, travis]
---

You might've noticed that installing [gems](https://rubygems.org) that aren't allowed by Github isn't working. Luckily enough, [travis](https://travis-ci.org) offers a solution by building the site with jekyll, with the extra gems installed, and then pushing that to `gh-pages`. First step is to work in the `master` branch for your development.

You install your needed `gems` by using a Gemfile. You do this by running `bundle init` and then in your `Gemfile`, you add the needed gems. Mine looks like this:

```ruby
source 'https://rubygems.org'

gem 'jekyll'
gem 'octopress-autoprefixer'
```

Running `bundle install` on your local machine will install the needed `gems` locally too.

Then you add your project to travis, and add the following `.travis.yml` in your repository:

```yaml
language: ruby
rvm:
  - 2.0.0
branches:
    only:
        - master
env:
    global:
        - secure: ...
        - GH_OWNER=...
        - GH_PROJECT_NAME=...
        - GH_EMAIL=...
        - GH_USER=...
        - GH_MESSAGE=...
install:
    - bundle install
script:
    - jekyll build
after_success:
    # Any command that using GH_OAUTH_TOKEN must pipe the output to /dev/null to not expose your oauth token
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then git submodule add -b gh-pages https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME} site > /dev/null 2>&1
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then cd site
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then if git checkout gh-pages; then git checkout -b gh-pages; fi
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then git rm -r .
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then cp -R ../_site/* .
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then cp ../_site/.* .
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then git add -f .
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then git config user.email "${GH_EMAIL}"
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then git config user.name "${GH_USER}"
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then git commit -am "${GH_MESSAGE}"
    # Any command that using GH_OAUTH_TOKEN must pipe the output to /dev/null to not expose your oauth token
    - if [[ $TRAVIS_PULL_REQUEST == 'false' ]]; then git push https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME} HEAD:gh-pages > /dev/null 2>&1
```

Where you fill in the `env` variables with the values you want, and the `secure: ...` with your encrypted github OAuth token. You get your token on <https://github.com/settings/tokens> with `repo` access. Then you'll use the travis commandline tool `gem install travis`, and in the repository you'll use this gemfile, you run:

```
travis encrypt GH_OAUTH_TOKEN=...
```

This method is in use for [haroenv/bus](https://github.com/haroenv/bus) (live: [haroen.me/bus](https://haroen.me/bus)).

If you have any questions, ping me on twitter [@haroenv](https://twitter.com/haroenv).
