---
slug: oss-security/
title: Secure Just by Being in a Cave?
date: 2020-11-05
subtitle: Security of OSS — Fluid Attacks as a vivid example
category: philosophy
tags: security, cybersecurity, code, software, company, business
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330966/blog/oss-security/cover_ztzxzn.webp
alt: Photo by Karsten Winegeart on Unsplash
description: We want to remind you that hiding your applications' source code
  can often provide you only an illusion of security
  and that OSS is a worthwhile alternative.
keywords: Security, Cybersecurity, OSS, Open Source, Code, Software, Company,
  Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/2HlidfG6ihs
---

In two posts I published previously, I had already mentioned Open Source
Software
([**OSS**](https://en.wikipedia.org/wiki/Open-source_software)). In [the
first one](../vulns-triage-synopsys/), I remember quoting Gardner,
referring to the increasing use of **OSS** by development teams in
charge of building applications. In [the second
one](/blog/look-inside-oss/), which may serve as an introduction to this
post, I addressed some generalities about **OSS**, its differentiation
from proprietary software, and some of its benefits as a business
strategy. For this post, we’ve decided to give more room to the security
of **OSS** and briefly present our experience at `Fluid Attacks`.

About two months ago,
[Nivel4](https://blog.nivel4.com/noticias/filtracion-revela-el-codigo-fuente-de-tres-bancos-en-mexico/)
reported that the source codes of three Mexican banks' mobile
applications had been leaked and revealed on the web. Some people on the
networks commented that the cause of the leak was a misconfiguration,
and the banks immediately reported that there was no impact on the
security of the systems and customers' sensitive data. Was it true? I
believe that many people were suspicious of such security on the spot.
By the way, if there was nothing to lose by showing the code, why did
they keep it out of sight? These banks undoubtedly lost users'
confidence and reputation among competitors.

The applications of the three banks inadvertently became **OSS**. We
could say that their owners intended to maintain a security image by not
making public the code. However, hidden or open, the code’s security
will depend on how solid and qualified its elaboration has been.
Vulnerabilities or flaws can be found in both open and proprietary
software, but as
[Byfield](https://www.datamation.com/open-source/nine-reasons-for-using-open-source-software.html)
shared some years ago, "proprietary software vendors are notorious for
security by obscurity." They usually erroneously believe that keeping
their systems in the dark caves will make them more secure. Therefore,
in many cases, they perform a few security assessments and patch
vulnerabilities relatively slowly.

One of the most mentioned business benefits of **OSS** is, contrary to
many people’s intuition, security. When we talk about an **OSS** project
widely recognized on the web, we can say that many eyes are scrutinizing
it and many hands are testing it regularly. Consequently, the chances of
overlooking cybersecurity risks are much lower than when the project is
private. A large community with a wide variety of members can detect and
fix vulnerabilities in the code much faster than a small group of
developers belonging to a single company.

Nevertheless, I should note that many companies keep their code secret,
some of them at the same time pretty well secured, for no other reason
than to preserve as their own the idea that makes them unique against
their competitors. That’s comprehensible. However, some hide only their
"essential" portions of code and expose the rest on the web to benefit
from working in open communities. That’s what, according to
[Brikman](https://www.ycombinator.com/library/56-why-the-best-companies-and-developers-give-away-almost-everything-they-do),
for example, Google does with their "primary differentiator\[:\] their
search architecture." Meanwhile, many companies that share *all* the
code to the general public, generating confidence by the security they
provide, can receive [income through other
means](https://www.sciencedirect.com/science/article/abs/pii/S026840121100123X?via%3Dihub),
including [offering services](https://lwn.net/Articles/786068/) related
to their **OSS**. They have their ["secret
sauce"](https://www.ycombinator.com/library/56-why-the-best-companies-and-developers-give-away-almost-everything-they-do)
located elsewhere, and here’s where `Fluid Attacks` comes in.

## Fluid Attacks is safe, out of the cave

<div class="imgblock">

![Karsten](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330966/blog/oss-security/karsten_wowiqz.webp)

<div class="title">

Figure 1. Photo by [Winegeart](https://unsplash.com/@karsten116)
on [Unsplash](https://unsplash.com/photos/v_OICS4SdEA).

</div>

</div>

`Fluid Attacks` was born directly in the free and open-source software,
making use of it and keeping it in that condition. As
[Gomez](https://www.linkedin.com/in/mgomezarango/en-us), co-founder of
the company, said, they started working directly on Linux and were in
charge of networking, based on **OSS**, before becoming a red team in
2008, which has not stopped sharing its code. Code that is not
exclusively adhered to a pair of privileged minds on which it’ll always
depend to exist and operate. Whenever someone leaves `Fluid Attacks`,
someone else with similar skills and experience will take over because
the raw material with which we work will never cease to be shared.

Apart from the collaboration that we can receive from smart people of
our [community](https://docs.fluidattacks.com/) and not legally
affiliated with our company, almost all `Fluid Attacks'` members can and
are encouraged to review the code to propose new ideas for its
optimization (including security). Since `Fluid Attacks’s` inception,
we’ve taken advantage of **OSS** as an organization, and we’ve also
committed ourselves, on a reciprocal basis, to generate our contribution
to the overall cybersecurity community.

Could then someone ask us, aren’t you giving away work that has cost you
so much? Aren’t your competitors watching in detail, even copying, what
you use to serve your customers? Couldn’t keeping an **OSS** mean giving
away the necessary material to other groups of individuals to establish
new companies and more competition for you? And, perhaps more
importantly, **aren’t you highly vulnerable to malicious hackers'
attacks by exposing your code?**

In response to these questions, we can say that what we’ve built so far
has also been partly thanks to many people worldwide who have maintained
the **OSS** movement. We can also say that we feel comfortable making
knowledge public, gaining experience and reducing duplication of effort.
Additionally, we rely on our primary differentiator —which is not in the
code— to stand out from old and new competitors. As I said, our way of
making profits is not focused on offering a code but services from human
intelligence using that code. Finally, **revealing our code doesn’t make
us highly vulnerable to attacks**, as long as it has the necessary
security controls and its vulnerabilities are reduced to a minimum.

It’s imperative to note that the code we publicly display is not just
the same code we use in our clients' security benefits. It’s also the
code that serves to carry out our systems' and products' security
analyses on an ongoing basis ([Continuous
Hacking](../../services/continuous-hacking/)). We’re not giving the
community a batch of mediocre and half-baked lines of code. The material
we develop and fervently update at an accelerated pace is our analysts'
material day by day. At the same time, it’s the stuff that can be used
reliably by anyone in any corner of the planet to detect vulnerabilities
in IT systems.

At `Fluid Attacks`, we understand that having a hidden code is not
necessarily keeping it safe. We comprehend that security depends on the
code’s strength and quality, which preferably should be reviewed by many
people and continuously. So, we don’t hide the code. There’s no mystery
behind what it can do. What we keep hidden and safe is our company’s and
clients' sensitive data, using complex encryption processes, for
example. That’s what we help many companies to achieve (discovering
vulnerabilities and promoting better development practices) and what we
give to you as a recommendation here.

Inside or outside the cave, your security will depend on your armor,
weapons and skills. We can help you, and the community can help you
improve your security. Leave the cave voluntarily (do not wait to be
taken out like the banks). It’ll reflect confidence, strength and
transparency to your followers, clients or stakeholders. Later, you’ll
even be able to generate, facilitate contributions to the community.
Just [contact us\!](../../contact-us/)

P.S. Take a look at our code [here](https://gitlab.com/fluidattacks)\!
