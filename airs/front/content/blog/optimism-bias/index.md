---
slug: optimism-bias/
title: '"No, We Won''t Get Hacked!"'
date: 2020-10-07
subtitle: And, "of course, I can always protect my company."
category: philosophy
tags: cybersecurity, mistake, risk, business, company, hacking
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330962/blog/optimism-bias/cover_or7kk2.webp
alt: Photo by Charles Deluvio on Unsplash
description: In cybersecurity, optimism bias and overconfidence can have
  pervasive consequences. I discuss them in this post.
keywords: Cybersecurity, Mistake, Risk, Optimism, Bias, Overconfidence,
  Ethical Hacking, Pentesting
author: Julian Arango
writer: jarango
name: Julian Arango
about1: Behavioral strategist
about2: Data scientist in training.
source: https://unsplash.com/photos/9BXL-Vn22Do
---

*How likely is your organization to suffer a hack or a data breach in
the next 12 months? How confident are you in containing all attacks on
your organization?* Your answers to these questions are probably
associated with how cybersecurity operations are performed at your
company. Psychological research has shown how complex 'judgment
formation' is. Mainly, **beliefs about future events** one can
experience and **perceptions about how skilled** one is depend on many
factors; I will not delve into those details. Instead, I will focus on
two strong tendencies on those judgments: first, a bias for optimism,
and second, overconfidence. I will discuss what the implications of
these two concepts for cybersecurity operations are.

## Optimism bias and overconfidence

*Optimism bias* is the tendency to overestimate the likelihood of
positive events in our lives and, conversely, to underestimate the
probability of adverse events. Perhaps the most common instance of this
bias in a business domain is what we see in **project management**. We
usually underestimate how long a project will take to complete;
likewise, we tend to underestimate the resources required. In another
realm, newlyweds say almost always that their divorce is nearly
impossible. Yet, the proportion of divorces across the world is around
50%. Optimism bias is not a failure of our brain or our physiology.
Quite the opposite: it has been hypothesized that this skewed judgment
has evolutionary roots; that is, it played a fundamental role in our
survival as species. The problem is that, nowadays, this deviation might
play against us. You can read more in a very insightful article Tali
Sharot wrote a few years ago
([Sharot, 2011](https://www.sciencedirect.com/science/article/pii/S0960982211011912)).

On the other hand, we have *overconfidence*, a related and probably more
pernicious tendency. If you work in cybersecurity, ask yourself: would
you rate your cybersecurity skills better than average? Furthermore, if
you’re a manager, do you think your management skills are above the
average manager? One of the most famous studies in overconfidence
measured how a group of car drivers rated their driving skills and
driving safety
([Svenson, 1981](https://www.gwern.net/docs/psychology/1981-svenson.pdf)).
The author found that at least 69% of participants ranked themselves
better than the median driver; at least 77% rated themselves as safer
than the median driver. Of course, this is statistical nonsense. The
American Automobile Association (AAA) ran a study in 2017 which included
a driving confidence measure; here’s an excerpt:

> "…​U.S. drivers report high confidence in their own driving abilities.
> Despite the fact that more than 90 percent of crashes are the result
> of human error, three-quarters (73 percent) of U.S. drivers consider
> themselves better-than-average drivers. Men, in particular, are
> confident in their driving skills with 8 in 10 considering their
> driving skills better than average."
> ([AAA, 2018](https://newsroom.aaa.com/2018/01/americans-willing-ride-fully-self-driving-cars/))

Are you a better driver than the average driver? I bet you won’t answer
"yes" so quickly after reading the previous lines. In other contexts,
this has been studied too. Some research pieces have suggested
"overconfidence as an explanation for wars, strikes, litigation,
entrepreneurial failures, and stock market bubbles" (see [Moore &
Healy, 2008](https://www.asc.ohio-state.edu/economics/healy/papers/Moore_Healy-TroubleWithOverconfidence.pdf)).

<div class="imgblock">

![Security](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330960/blog/optimism-bias/security_e9c03q.webp)

<div class="title">

Figure 1. Photo by [Ben
Williams](https://unsplash.com/@d_one?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on [Unsplash](https://unsplash.com/s/photos/animal-security?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

</div>

</div>

## And the implications for cybersecurity?

In cybersecurity, these two traits can lead to undesired behaviors. *"We
won’t get hacked… that won’t happen here"* might be an important
vulnerability a company should look to fix. One person or company should
never be so sure about the reach of cyber threats. Stopping thinking
about additional ways a threat could be materialized is not a good
strategy, given the surprising ways cybercriminals manage to cause
trouble. On the other hand, thinking that your internal cybersecurity
team is *always* capable of repelling any attack is dangerous. Ask
yourself, what’s your point of reference? To whom you compare your
skills and processes?

Consider some of the figures put together at Hosting Tribunal
([here](https://hostingtribunal.com/blog/hacking-statistics/#gref) and
[here](https://hostingtribunal.com/blog/cybersecurity-statistics/)):

- 444,259 ransomware attacks took place worldwide in 2018.

- More than 6,000 online criminal marketplaces sell ransomware
  products and services.

- 90% of CIOs admit to wasting millions on inadequate cybersecurity.

- 65% of the top 100 banks in the US failed web security testing.

- Data breaches are identified in 191 days on average.

- There were more than 53,000 cybersecurity incidents in 2018.

If people tend to exhibit a bias towards optimism, and if people think
they have better skills than others on average, it is not difficult to
start wondering whether our stands on cybersecurity might be a bit
flawed. *Is it possible that my company is more exposed than previously
thought?* *Should I revisit the confidence in what I can really do now
to protect my company?* Those are healthy reflections we all should make
if we are responsible for cybersecurity at any level. Why? Integrating
information to know our level of risk exposure and our skills is
difficult. We have limited information about cybersecurity risks, and we
tend to accept data from known actors (e.g., competitors). But what
about more distant threats that maybe we don’t know about, or that we
think we know about but perhaps it’s just wishful thinking?

One of the sources of optimism bias lies in another psychological
phenomenon: the availability heuristic. Think about the last time you
knew about a data breach within your organization. If it is hard to come
up with an example in your mind, chances are you would think it is not
very likely that your company would suffer such an event in the future.
Here, your past experiences and knowledge are, in part, responsible for
the bias.

Now, think about how confident your team is about detecting all
vulnerabilities in your applications and infrastructure. It might be
true that you have never been hacked…​ or that you haven’t been aware of
it. Many companies report no breach even if known vulnerabilities are
found long after being injected. Another thing to consider is: how many
violations have been successful in other organizations without being
revealed to the public? That’s an instance of an interesting problem:
*knowing what you don’t know*. Again, a healthy skepticism helps here.

## What can you do?

You can adopt a healthy skepticism and let outsiders test your systems
to find potential weaknesses. Also, be open: like a real scientist is
open to finding his/her theory wrong after running experiments.
Implement a process by which you can continuously know whether your
systems are vulnerable. Go further and make that process automatically
*break the build* when an application doesn’t meet the defined security
standards. And close that cycle triggering the fixes required, as soon
as possible, to keep the business up and running. You can have all of
that with [Continuous Hacking](../../services/continuous-hacking/) and
coordinating your team and stakeholders with an Attack Surface Manager.

We hope you have enjoyed this post, and we look forward to hearing from
you. [Do get in touch with us\!](../../contact-us/)
