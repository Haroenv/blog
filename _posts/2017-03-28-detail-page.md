---
layout: post
date: 2017-03-28 23:00
title: Detail page
tags: [algolia,internship]
---

Great news! The detail page of Yarn has been accepted and deployed. You can now see detail pages of every package on Yarn (and thus also npm). There will be a more detailed blog post on all the things that this held in, and edgecases, but I don't want to spoil all of that yet.

This week I've written part of my bachelor thesis, mostly focusing on figuring out which chapters to pick and where I can later explicitly write lots about. You can find that — in LaTeX — at [Haroenv/bachelorproef](https://github.com/Haroenv/bachelorproef). Any critiques are always welcome, but just know that this is not more than a draft right now.

As you might know, most of the bugs are found just after deploying and just before something being merged. This is mostly because before merging, lots of people look at your code, read all lines and try to find things that can be improved. After being deployed lots is found as well, because it sometimes takes seeing something live before you notice something is wrong.

Most of my pull requests this week were to the Yarn website this week because of that, and also because I wanted to fix everything as much as possible to be able to get a clean deploy when the package detail was live.

{% include image.html img='yarn-prs-this-week.png' alt='8 opened pull requests to yarnpkg/website. 6 merged, one closed and one still open. fix(detail): make changing languages work Mar 28, fix(docs) turn off email protection when not needed Mar 27, feat(search): mark count location in download string Mar 27, fix(docsearch): custom styling Mar 26, fix(i18n): provide a default value for scripted langs Mar 25, feat(config): put keys in a separate file Mar 25, fix(ci) solano Mar 21, Detail page! Mar 20' caption='Pull requests to the Yarn website this week' %}

The deployment itself went pretty smoothly. The reason the pull request was open for a while was kinda double. Firstly because the Yarn website might not have been the highest priority at Facebook (which I understand, they have other websites to care about), secondly because [Daniel Lo Nigro](https://twitter.com/Daniel15) was on holiday before, [Christoph Pojer](https://twitter.com/cpojer) just got married and [Konstantin Raev](https://twitter.com/bestander_nz) was preparing a talk on Yarn. All things considered, it got merged fast still.

Thanks to everyone who helped, from the Facebook team for reviewing thoroughly, [Vincent](https://twitter.com/vvo), [Kevin](https://twitter.com/Kevin_Granger), [Jonas](https://twitter.com/JonasBadalic), [Alex](https://twitter.com/bobylito), [Maxime](https://twitter.com/maxiloc), [Léo]() and [Sylvain](https://twitter.com/sylvainutard) from Algolia for helping me when needed and reviewing my code.

Now that most of the work on the Yarn site is done, a blog post will come on the Algolia blog (and maybe on other places too), and I'll maybe talk at a meetup about it. If someone that reads this organises a meetup and wants to hear me talk about it, [shoot](https://twitter.com/intent/tweet?text=hey%20@haroenv,%20come%20talk%20at%20this%20meetup%20about%20Yarn!&related=haroenv&original_referer=https://haroen.me/algolia-blog/detail-page)!
