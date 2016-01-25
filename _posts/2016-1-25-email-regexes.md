---
title: Email Regexes
layout: post
date: 2016-1-25 10:24
tags: programming
---

You might've come around trying to check an email address. The best strategy for this is to be as lenient as possible. You don't want people who have a "weird" email address to get blocked by your system to even enter their address.

Some (weird) possibilities you should consider:

* any unicode is allowed
* domain names can be ip addresses too
* any length of top level domain is allowed
* `@` is required

My solution only has one major flaw[^1], and that's that it won't allow domains without a tld or an ip address.

I check for `any character more than once` (`.+`), followed by a single `@`, followed by the domain which can be an ipv4 address, an ipv6 address or a domain with tld. this will check for `any character followed by a dot or a colon, followed by any character`, which will match `172.0.0.1`, `haroen.me`, `::1` or `2001:db8:85a3::8a2e:370:7334` (`.+(\.|:).+`)

```
/.+@.+(\.|:).+/
```

Some testing can be done [here](https://regex101.com/r/yT4zI2/2) at [regex101](https://regex101.com), a very useful tool to check regular expressions.

[^1]: okay, there could be more flaws, let me know if I forget something
