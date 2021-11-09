---
slug: big-code/
title: Big Code
date: 2019-08-02
subtitle: Learning from open source
category: machine-learning
tags: machine-learning, vulnerability, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330671/blog/big-code/cover_gbuzvj.webp
alt: Git. Photo by Yancy Min on Unsplash, https://unsplash.com/photos/842ofHC6MaI/
description: Here we'll see how DeepCode works. It has a lot of potential
  for identifying bugs in your code by learning from
  the abundant sources available in Github.
keywords: Machine Learning, Vulnerability, Open Source, Deep Learning, Lint,
  Bug, DeepCode, Github, Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/842ofHC6MaI/
---

In our [Machine Learning (`ML`) for secure code
series](../tags/machine-learning) the *mantra* has always been the same:
to figure out how to leverage the power of `ML` to detect security
vulnerabilities in source code, regardless of the
[technique](../crash-course-machine-learning), be it [deep
learning](../deep-hacking), [graph mining](../exploit-code-graph),
[natural language processing](../natural-code), or [anomaly
detection](../anomaly-serial-killer-doll).

In this article we present a new player in the field,
[DeepCode](https://www.deepcode.ai/), a system that has exactly this
purpose, combining `ML` with data flow analysis, namely in the form of
taint analysis.

Taint analysis can come in dynamic and static forms and can be performed
at the source and binary levels, but either way, the goal is the same.
Start by looking at where input comes from and is controlled by the
user, for example, a web app search field. These are named *sources* in
this context. Then, continue to follow the thread to where it gets used
by the system in a security-critical fashion, as in using that info to
query a database, to continue with the previous example. These points
are called *sinks*.

<div class="imgblock">

![Taint analysis diagram](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330670/blog/big-code/taint-analysis_fz03sg.webp)

<div class="title">

Figure 1. Taint analysis diagram via [Coseinc](https://www.csa.iisc.ac.in/~vg/teaching/E0-256/slides/TaintAnalysis.pdf).

</div>

</div>

Along the way in the case of a secure application, data should encounter
significant input sanitization or validation. These are called
*sanitizers* in the taint analysis context. However, frequently this
does not happen, and thus vulnerabilities arise.

Traditional taint analysis tools, however, usually present high false
positive rates, as is the case with
[Bandit](https://github.com/openstack/bandit) and
[Pyt](https://github.com/python-security/pyt) (see some critique
[here](https://smarketshq.com/avoiding-injection-with-taint-analysis-1e55429e207b)).

`DeepCode’s` purpose is to remove minor difficulties these taint
analysis tools may have. `DeepCode` does this by learning from the vast
quantity of freely-available, high-quality code in open repositories
such as [Github](https://github.com/), a circumstance then dubbed "Big
Code". The tool is easy and free to use. This provides the added
advantage of also learning from the user’s code, the suggestions made by
the tool, and the user’s feedback (accepting suggestions, *how* to fix
them, etc).

Another problem with taint analysis is that sources, sinks, and
sanitizers need to be specified by hand, which is extremely impractical
for large-scale projects. This is another area where `ML` helps
`DeepCode`, but how is that done?

`DeepCode` has been called [Grammarly](https://app.grammarly.com/) for
code. It claims to be 90% accurate, and that it understands the *intent*
behind the code. It also claims to find twice as many issues as other
tools, even some critical ones (`XSS`, `SQL` injection and path
traversal, etc.) which is something typical static analysis tools do
not. Moreover, it claims to be easy to use, requiring no configuration.

The tool is friendly. You need only point it to your repository and give
the appropriate permissions, and then it will show a dashboard with the
issues found. Here is one for [Eclipse Che Cloud
IDE](https://github.com/eclipse/che):

<div class="imgblock">

![Dashboard for Eclipse Che](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330670/blog/big-code/che-dashboard_chqwbk.webp)

<div class="title">

Figure 2. Security issues dashboard for Eclipse Che, adapted from [DeepCode
demo](https://www.deepcode.ai/app/gh/eclipse/che/5be0e29f11fdef73ed4a3da5fe61e3cc0eb3e875/_/dashboard/).

</div>

</div>

Here we see three instances of a possible path traversal vulnerability.
In the full dashboard, we also see how they report an insecure `HTTPS`
channel, a Server Side Request Forgery (`SSRF`), a Cross Site Scripting
(`XSS`) vulnerability, and a header that leaks technical information
(`X-Powered-By`). And that’s only the issues tagged as "security". There
are also `API` misuse issues, v.g. using `Thread.run()` instead of
`Thread.start()`, general bugs or defects, and now they even throw lint
tools results, which deal with formatting and presentation issues. Oh,
yes, and every issue comes with a possible fix you might implement right
away.

Quite nice, from the point of view of contributing a new vulnerability
report to a project, with no false positives. However when the aim is to
find *all* vulnerabilities, one cannot help but raise the question: is
that all? Are these *all* the security vulnerabilities in a project with
more than [300,000](https://api.codetabs.com/v1/loc?github=eclipse/che)
lines of code?

Let us take one of the many Vulnerable by Design (`VbD`) applications we
use for training purposes in our [challenges
site](https://autonomicmind.com/challenges/sites-ranking-vbd/), and see
how many vulnerabilities come up by running `DeepCode` on them. By the
way, they currently support `Javascript`, `TypeScript` and `Java`,
besides the original `Python`. That leaves us with two apps to try: the
[Damn Vulnerable `NodeJS` Application](https://github.com/appsecco/dvna)
(`DVNA`) and [Damn Small Vulnerable
Web](https://github.com/stamparm/DSVW) (`DSVW`), since most `VbD` apps
are built with `PHP`.

I forked both of these on `Github`, signed up for a `DeepCode` account,
and let it run. For `DSVW`, which is a single `Python` file under 100
lines of code, but still ridden with vulnerabilities, `DeepCode` reports
zero issues. Perhaps it does not work as well on such tiny projects.

<div class="imgblock">

![Dashboard for DSVW](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330669/blog/big-code/dsvw-dashboard_nhzja3.webp)

<div class="title">

Figure 3. Zero issues in DSVW.

</div>

</div>

This is, to say the least, disappointing, since that `DSVW` has no less
than 26 different *kinds* of vulnerabilities, as per its `README`. In
[Writeups](https://gitlab.com/fluidattacks/writeups/tree/master/vbd/dsvw/),
three of those have been manually explored and exploited.

Maybe it’s a problem with having so few lines of code, maybe it’s a
`Python` thing, so let’s try the other one: `DVNA`, built with `NodeJS`
with the specific purpose of demonstrating the [`OWASP` Top 10
vulnerabilities](https://www.owasp.org/index.php/Top_10-2017_Top_10).

This time around, `DeepCode` found 9 issues. Of those, take out the 3
which come from `ESLint`, and let’s consider the other 6; 2 are `API`
misuses, which are basically "use arrows instead of functions" and 4 are
security vulnerabilities, and pretty serious ones at that:

- Code Injection via `eval` function in calculator module. Not the
  same one as in the authors' security guide. Also not yet reported in
  [Writeups](https://gitlab.com/fluidattacks/writeups/tree/master/vbd/dvna/)
  This should be researched further.

- `SQL` injection. As per [security
  guide](https://appsecco.com/books/dvna-developers-security-guide/solution/a1-injection.html)
  and
  [Writeups](https://gitlab.com/fluidattacks/writeups/blob/master/vbd/dvna/0564-sql-injection/jicardona.feature).

- Open Redirect. Also in [the security
  guide](https://appsecco.com/books/dvna-developers-security-guide/solution/ax-unvalidated-redirects-and-forwards.html)
  and
  [Writeups](https://gitlab.com/fluidattacks/writeups/blob/master/vbd/dvna/0601-unvalidated-redirects/simongomez95.feature).

- Technical information leakage via the `X-Powered-By` header, as in
  `Che`.

So, altogether, 3 noteworthy security vulnerabilities, in a `NodeJS`
application with more than 7,500 lines of code. In
[Writeups](https://gitlab.com/fluidattacks/writeups), at least 29
different vulnerabilities have been reported in `DVNA`. You can see a
[report](https://gitlab.com/fluidattacks/writeups/blob/master/vbd/dvna/results-toe.md)
on manual testing vs the `LGTM` [code-as-data](../oracle-code) tool in
there, too, where it is quite clear that tool misses most of the
vulnerabilities as well.

Now for a more realistic test, let’s try running `DeepCode` on some of
our own repos, namely, Integrates, our platform for vulnerability
centralization and management and
[asserts](https://fluidattacks.gitlab.io/asserts/), our vulnerability
automation framework. Both are
[open-source](https://gitlab.com/fluidattacks), written in `Python`, and
actively developed. As before, the vast majority of issues found by
`DeepCode` are of the `lint` and `API` usage kind.

<div class="imgblock">

![Integrates Dashboard](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330669/blog/big-code/integrates_rlof4p.webp)

<div class="title">

Figure 4. Integrates Dashboard

</div>

</div>

In `Integrates` we see a possible command injection in the spreadsheet
report generation function. However, this input is not controllable by
the user, so this does not pose a real threat at the moment:

**Command Injection in Integrates?.**

<div class="imgblock">

![Command Injection in Integrates?](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330669/blog/big-code/reports.py_nubki3.webp)

</div>

However, the suggestion to sanitize the input via `subprocess.call()` is
not bad. Who knows if `Integrates` will later have user-configurable
passwords for reports, or a *different* vulnerability enables an
attacker to change this parameter.

The other security issue is in the `PDF` report generation, this time
identified as `Path traversal`. Again, probably difficult to exploit,
but should be sanitized anyway.

<div class="imgblock">

![Asserts
Dashboard](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330669/blog/big-code/asserts_vtzc8h.webp)

</div>

In [`Asserts`](https://fluidattacks.gitlab.io/asserts/), however, the 15
issues found by `DeepCode` are less worrisome, for two reasons:

- [`Asserts`](https://fluidattacks.gitlab.io/asserts/) is not a
  client-server application, but an `API` that runs locally.

- Most of the 15 issues are several instances of `SSRF`, when
  [`Asserts`](https://fluidattacks.gitlab.io/asserts/) makes `HTTP`
  requests via [Requests](https://2.python-requests.org/en/master/),
  generally to client’s `ToEs` as one would in a browser.

Of course, all the issues detected by `DeepCode` will be taken care of.

---
Once again, this confirms our other *mantra* we have held in this
[Machine Learning (`ML`) series](../tags/machine-learning) and also
[elsewhere](../replaced-machines/) [on
our](../../about-us/differentiators/#method)
[website](../importance-pentesting/). While automated tools, even
`ML`-powered ones, may have the potential to do what a human could not
do in terms of repetitions and scalability, as of yet, they do not have
the malice or creativity which humans have in finding critical and
interesting security vulnerabilities.

# References

1. V. Raychev. 2018. [DeepCode releases the first practical anomaly bug
    detector](https://medium.com/deepcode-ai/deepcode-releases-the-first-practical-anomaly-bug-detector-32bebc8cdf57).

2. V. Chibotaru. 2019. Meet the tool that automatically infers security
    vulnerabilities in Python code.
    [Hackernoon](https://tinyurl.com/y6tpoxzj)
