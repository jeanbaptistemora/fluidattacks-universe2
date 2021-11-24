---
slug: seek-chaos/
title: Seek for Chaos and Dive Into It
date: 2019-05-06
subtitle: The Antifragile philosophy
category: philosophy
tags: business, security, risk, experiment
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331094/blog/seek-chaos/cover_bvvxp3.webp
alt: 'multicolor abstract paint on Unsplash: https://unsplash.com/photos/YQrUzrsRNes'
description: In this article, we examine how the Antifragility concept
  can inform design decisions, change the mindset of cybersecurity teams,
  and affect your business.
keywords: Security, Fragile, Robust, Antifragile, Risk, Chaos,
  Ethical Hacking, Pentesting
author: Julian Arango
writer: jarango
name: Julian Arango
about1: Behavioral strategist
about2: Data scientist in training.
source: https://unsplash.com/photos/YQrUzrsRNes
---

Imagine a medium-sized sealed carton box, with two or three glasses
inside. If you kick the box (like kicking a soccer ball), the glasses
will surely break. The glasses are fragile. Now, think of the same box,
but with two or three standard steel hammers. Nothing will happen to
those hammers after kicking the box. The hammers are robust in this
context.

In cybersecurity, there are plenty of instances in which artifacts or
entities are fragile given some inputs (we will call them stressors).
For example, some default password designs are fragile. It is cheap to
find lists of these and it is not so challenging to perform a
brute-force attack. At some point, that stressor will break at least one
security layer. On the other hand, adding more security layers to
authentication (i.e., two-factor authentication) prevents systems to be
hacked so easily; these are robust (although how robust is depends on
the type of stressor). The typical paradigm of information security has
been to go from fragile designs and processes to robust ones as
previously unthinkable events appear. Think of how networking protocols
have evolved or how `IT` infrastructure is becoming more script-oriented
or transitioning into infrastructure as a code.

A couple of years ago, a new related concept appeared: *antifragility*.
This term is developed in the book *Antifragile by Nassim Taleb*. A
controversial figure, Taleb is a professor of Risk Engineering at New
York University. Beyond robustness, he points to actions and entities
that, rather than protect, gain from randomness, disorder, and
uncertainty. He called this antifragile. Lifting weights and
administering vaccines are antifragile actions: people become stronger
from this stressors. Lifting weights break muscle fibers. Vaccines are
small illnesses injected. These make your body to grow stronger muscles
and develop resistance against viruses, respectively. Antifragility is
becoming better from struggles. If you google a bit, you might find that
a Hydra, the mythological monster, is an antifragile entity.

Shane Parrish, who runs Farnam Street blog, has provided more examples
related to this concept using a triad: `FRAGILE` - `ROBUST` -
`ANTIFRAGILE`. Here are two cases:

<div class="tc">

**Table 1. An excerpt of The Central Triad: three types of exposure. Source:\
<https://fs.blog/2014/04/antifragile-a-definition/>**

</div>

|                                   |                                                                                   |                                                                           |                                                |
| --------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------- |
| <p> **Case**                 </p> | <p> **FRAGILE**                                                              </p> | <p> **ROBUST**                                                       </p> | <p> **ANTIFRAGILE**                       </p> |
| <p> Errors                   </p> | <p> Hates mistakes                                                           </p> | <p> Mistakes are just information                                    </p> | <p> Loves mistakes (since they are small) </p> |
| <p> Dichotomy event-exposure </p> | <p> Studying events, measuring their risks, statistical properties of events </p> | <p> Studying exposure to events, statistical properties of exposures </p> | <p> Modifying exposure to events          </p> |

How can we foster antifragility in our cybersecurity efforts? We will
discuss two ways: first, by creating “troubles” and inject them into
operations. Second, by experimenting, tinkering and exposing ourselves
and systems to small risks.

## Netflix’s Simian Army

<div class="imgblock">

!["Monkey in a cave"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331093/blog/seek-chaos/monkey_unzaj3.webp)

<div class="title">

Figure 1. A monkey shouting on a cave”; perhaps he is about to cause some chaos!

</div>

</div>

The worst nightmare for a company like `Netflix` is downtime. In 2008,
the company decided to migrate to a cloud infrastructure after facing a
massive database incident. Complete migration took eight years (read
[here](https://media.netflix.com/en/company-blog/completing-the-netflix-cloud-migration)
about it). In the process, back in 2010, the company launched `Chaos
Monkey`, a tool to cause their cloud servers to be offline by random.
They cannot afford, for instance, outages of their `IaaS` provider.

### The Netflix Simian Army

> “By running Chaos Monkey in the middle of a business day, in a
> carefully monitored environment with engineers standing by to address
> any problems, we can still learn the lessons about the weaknesses of
> our system, and build automatic recovery mechanisms to deal with them.
> So next time an instance fails at 3 am on a Sunday, we won’t even
> notice.”

By being exposed to these outages, `Netflix` assesses how proper the
countermeasures are to keep services running. If they are not, they
devise improvements to avoid these outages when they happen for real.

> “By pseudo-randomly rebooting their own hosts, they could suss out any
> weaknesses and validate that their automated remediation worked
> correctly,”

wrote [Gremlin](https://www.gremlin.com/chaos-monkey/), a *“chaos
engineering”* company. `Netflix` didn’t stop there. They build a `Simian
Army`: more tools to inject other *“troubles”* into their platform. One
of these is `Chaos Gorilla` which simulates an outage of an entire
availability zone.

This mindset is in line with the cases shown in `table 1`. `Netflix` was
not waiting for mistakes to happen; they created them. Furthermore,
those *"mistakes"* were diverse; they were creating different exposures
to their platform. The journey has not been perfect, and some outages
took place, especially at the early days of the migration (read about a
Christmas outage
[here](https://medium.com/netflix-techblog/a-closer-look-at-the-christmas-eve-outage-d7b409a529ee)).
However, Netflix has achieved a remarkable resiliency, even with
underlying infrastructure failing (see
[here](https://www.networkworld.com/article/3178076/why-netflix-didnt-sink-when-amazon-s3-went-down.html)
a report on Amazon S3 outage), making those earlier outages something
tiny.

I don’t know about you, dear reader, but I’ve never experienced a
`Netflix` outage since July 2013, when I became a customer.

## Experimentation, tinkering and small risks

<div class="imgblock">

![Richard
Feynman](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331094/blog/seek-chaos/feynman_vbcjy0.webp)

<div class="title">

Figure 2. Richard Feynman

</div>

</div>

> “The test of all knowledge is experiment. Experiment is the sole judge
> of scientific ‘truth’.” - Richard Feynman

In my work, I rely on behavioral insights most of the time to think
about behavior change. Many people I have worked with believe Behavioral
Science is the origin of proper experimentation, but they are wrong. It
is precisely the opposite: good experimentation has been essential in
creating what Behavioral Science is today. Likewise, good
experimentation is a door-opener for novel ideas, different approaches
in doing things regardless of discipline. Some people think innovations
come from a bunch of new methodologies and frameworks (e.g., design
thinking), but I would argue that innovations are created more from an
exploration mindset and curiosity than anything else. The glue of these
two elements is running experiments. By exploring and being curious, we
discover how the world works; we start creating hypotheses. By doing
experimentation, we test those hypotheses and continue to build
knowledge upon empirical results.

In a sense, becoming antifragile means that you would have to crave for
some chaos. You would have to seek for variability, and you would have
to embrace and face uncertainty. This would lead you to learn to live in
harsh circumstances if they arrive. To become antifragile is to become a
constant learner with diverse inputs. In this way, a company could be
always a step further and be better prepared for the uncertain future.
That’s exactly what experiments are for: to learn what works and what
doesn’t.

I acknowledge that the corporate world has reasons not to invest or
support this mindset. One of these is the cost. Investing in
experiments, with a no clear outcome isn’t encouraging. However, in the
words of Parrish, that’s playing the short-term game, which is
dangerous. Another reason is how to handle results from unsuccessful
experiments. People in firms fear they would seem ridiculous in the face
of unfavorable results. But, here’s the thing: how much money companies
are not capturing by not experimenting? It might be they are just
following the herd. We should reframe our thinking into asking how much
are we missing (or losing) by not experimenting, rather than keeping
telling ourselves that an experiment is expensive.

> “You have to be willing to look like an idiot in the short term to
> look like a genius in the long term” - Shane Parrish —Farnam Street
> blog

John List and Uri Gneezy (both experimental economists), in their book
The Why Axis, suggest that businesses that do not experiment are losing
money. Furthermore, they claim that executives of these
non-experiment-oriented corporations will become endangered species
(`p. 213`).

An organization I admire is The Behavioral Insights Team (`BIT`). This
company works designing and running experiments since 2010. Almost every
project is a well-designed experiment. They aim to find cheaper and
scalable solutions to improve efficiency and efficacy of services from
governments and public institutions towards citizens. They combine novel
approaches including behavioral science, adequate randomized control
trials, and data analyses. From their work (and learning), they were
able to launch `BI Ventures`, their product development army. They have
been looking for *"mistakes"* and experimenting with different
*“exposures”* to help governments stepping away from fragility. In
their journey, `BIT` itself has become a great example of an antifragile
company. See how `BIT` has been featured:

- The Economist ([Policymakers around the world are embracing
  behavioral
  science)](https://www.economist.com/international/2017/05/18/policymakers-around-the-world-are-embracing-behavioural-science)

- The Guardian ([The rise of nudge – the unit helping politicians to
  fathom human behaviour; The ‘nudge unit’: the experts that became a
  prime UK
  export](https://www.theguardian.com/public-leaders-network/2015/jul/23/rise-nudge-unit-politicians-human-behaviour)).

## Becoming antifragile: Fluid Attacks can help

Want to start becoming antifragile in your cybersecurity efforts? We can
help. Check out our services. We inject a mix of *“troubles”* into your
applications and `IT` infrastructure:

- [Continuous hacking](../../services/continuous-hacking). Think of it
  as a constant source of stressors.

- [One-shot hacking](../../services/one-shot-hacking/). This is like a
  one-shot stressor focused on your most valuable information assets
  (or on the target you want).

We are able to create some monkeys and even gorillas to shake your `IT`
assets, making offensive testing your best line of protection. That way,
you can learn how to better prepare for potential incidents and outthink
attackers\! And don’t worry: we do it in a controlled way.

We also invite you to take a look at our Attack Surface Manager, a
platform to keep track of weaknesses. Think of it as a platform that
helps you to learn how to become antifragile in cybersecurity.
