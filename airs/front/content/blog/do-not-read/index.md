---
slug: do-not-read/
title: Do Not Read This Post
date: 2019-04-29
subtitle: What if this post were a malicious link?
category: attacks
tags: social-engineering, hacking, security, business
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330869/blog/do-not-read/cover_getmyo.webp
alt: 'Yellow police line tape on Unsplash: https://unsplash.com/photos/jM6Y2nhsAtk'
description: In this post, we'll look into the behavior trends
  of developers when including security in their codes,
  and how it can affect your company.
keywords: Social Engineering, Malware, Behavior, Security, Developer,
  Coding, Ethical Hacking, Pentesting
author: Julian Arango
writer: jarango
name: Julian Arango
about1: Behavioral strategist
about2: Data scientist in training.
source: https://unsplash.com/photos/jM6Y2nhsAtk
---

Why the f\*ck did you click on this post?

Chances are, you were attracted to the title, paradoxically suggesting
not to do something. But, here you are. We are glad you did not follow
that direction, but we deliberately crafted that title to attract your
attention, to guide your behavior. We behave in ways plenty of times
motivated by surprising factors. That single click you made a few
seconds ago is an example.

As a company, we have wondered for years how we can harness what science
already knows about human motivation in what we aim to provide to our
customers, not only from the attackers' perspective but also from the
"good guys" shoes. We know that information security is more than just
focusing on software and IT infrastructure: it is about how we behave.

What we know as **social engineering** is essentially the science of
persuasion put into practice, with presumably dark intentions. A bunch
of globally renowned organizations has succumbed to these types of
attacks, especially by [phishing](../phishing/) and impersonation, with
significant financial and reputational losses. According to
[Verizon](https://www.phishingbox.com/assets/files/Page_Editor_Files/rp_DBIR_2016_Report_en_xg.pdf),
which periodically publishes the Data Breach Investigation Report
(DBIR), in 2015, **95 out of 100** of advanced and targeted attacks
involved spear-phishing scams through emails with malicious attachments.
Many people still make a decision an attacker wants to be made triggered
by a well-crafted email that arrives at their inbox. A behavior
(persuasion) guiding another behavior (download an infected file).
Although important, we acknowledge that social engineering became boring
for many people in our field (but we wonder why), so, in this post, we
want to shift to other behaviors, other types of risks.

Problematic behaviors cataloged as human errors are interesting enough
because they seem irrational. They are those actions or omissions that
could have a great deal of impact within companies. Ongoing research
conducted by
[Ideas42](http://www.ideas42.org/blog/project/human-behavior-cybersecurity/),
a US non-profit, social-purpose organization, has found (by speaking to
cybersecurity experts) that **70-80%** of the costs attributed to
cybersecurity attacks are rooted in human error. We can think of those
times when we choose [*insanely weak*](../credential-stuffing/)
[passwords](../requiem-password/), of computer sessions we unnecessarily
leave open waiting for someone to dive in, of doing nothing about timely
found security vulnerabilities, of providing sensitive information to
some party without much thought, etc. Some of these are out of `Fluid
Attacks'` scope nowadays. Some others are our very reason to exist;
let’s talk about these.

<div class="imgblock">

![on Unsplash https://unsplash.com/photos/BzIC8ioj7Ms](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330868/blog/do-not-read/rest_g5a9bj.webp)

<div class="title">

Figure 1. Most people "rest" on intentions and fail to jump into action.

</div>

</div>

Let’s take secure coding. How many developers indeed engage in secure
coding? Ideas42 has found a
[figure](https://www.eweek.com/security/app-security-worries-cisos-but-most-fail-to-adopt-secure-development)
worth taking a look at. Nearly **14.000 CISOs** and other security
professionals were surveyed by ISC2. **72%** of them indicated that
"application vulnerabilities were a top concern". Still, only **24%** of
security practitioners say their companies always scan for bugs during
the code development process, and another **46%** sometimes look for
bugs during development. This could be seen by a psychologist as a clear
example of the intention-action gap. (Another example: The majority of
us agree that saving for the future is very important; yet, just a few
of us are saving enough for retirement.) Ideas42 has identified [secure
coding](http://www.ideas42.org/wp-content/uploads/2016/08/Deep-Thought-A-Cybersecurity-Story.pdf)
as one behavioral challenge that might be a potential lever to make
cybersecurity more robust. They provide behavioral insights to take into
account and tactics (design concepts) to reduce barriers to secure
coding. A summary is here:

<div class="tc">

**Table 1. Developers behaviors**

</div>

|                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p> **Behavioral Insights —how do developers behave**                                                                                                                                                                                                                                                  </p> | <p>                                                                                                                                                                                                                                                                                                                                                                                                                                        </p> |
| <p> **Tunneling:** Developers prioritize functional deliverables at the expense of security.                                                                                                                                                                                                           </p> | <p> Developers do their job using heuristics that overlook security concerns.                                                                                                                                                                                                                                                                                                                                                              </p> |
| <p> The explanation comes from the psychology of scarcity. People tend to focus on what is most pressing under scarcity (money, time, social connections, etc.). In the case of software developers, functionality trumps security aspects most of the time (and this is not necessarily undesirable). </p> | <p> Heuristics are mental shortcuts from a behavioral perspective. This has an evolutionary explanation: Our brains, most of the time, look for the path of least resistance to save energy. Developers use heuristics because coding is effortful, and they learn "tricks" to code easily for functionality and/or performance. What is the likely trade-off? Security. But heuristics can also be used in security, as we will see next. </p> |

Some of the *design concepts* Ideas42 suggests to make cybersecurity
more robust referring to the safe coding behaviors are almost exactly
what we at `Fluid Attacks` want to provide to our customers:

1. **Provide/create more bandwidth:** By *bandwidth*, behavioral
    scientists refer to cognitive capacity. Off-loading cognitive
    attention on secure coding from developers is a way to provide more
    robustness to security, by allocating full attention to safe coding.
    Do you know our [Continuous Hacking
    service](../../services/continuous-hacking/)? We are bandwidth for
    you\! We make it easier for your development team to focus first on
    functionality and performance without forgetting about security.
    Additionally, we provide bandwidth to IT security administrators and
    project managers through our [Attack Surface
    Manager](https://app.fluidattacks.com/). You don’t have to invest
    important cognitive resources to deal with weakness tracking,
    remediation and reporting.

2. **Provide tools to augment heuristics:** Developers can also rely on
    heuristics for secure coding. Have you visited our
    [**Criteria**](https://docs.fluidattacks.com/criteria/)? It is
    completely **free**\! Your company can leverage what we have built
    over the years, making infusing security on your code and IT
    infrastructure a lot easier.

3. **Bring costs into the present:** In a nutshell, we tend to be
    present-biased (weighing more value on immediate rewards compared to
    future rewards, even when the latter are objectively bigger) and
    loss-averse (we prefer to avoid losses than seeking gains).
    Developers may value delivering functionality quickly more than
    delivering, additionally, secure coding at low cost (time-effort),
    even when the potential loss in the future (by not considering safe
    coding) is enormous. You could consider what Ideas42 suggests: put
    incentives upfront, for example, performance-based pay. We
    acknowledge this is not easy, but it is worth considering and
    analyze how feasible it is.

These clever people at Ideas42 also came up with another ten behavioral
challenges related to cybersecurity. We invite you to take a look at the
report they published a couple of months ago.

We hope you have enjoyed a not-so-well-known perspective on information
security (behavior), and we look forward to discussing more of this. One
of our former employees, now a behavioral strategist, recently shared
with us some ideas and perspectives that led to this post. We were
impressed by how behavioral science is spreading fast, as he told us,
and we also came across this study from Ideas42 in which we find common
grounds in what we already do that influences behavior for the benefit
of our customers.

We will try to bring more of these behavior-related topics in future
posts, and we want to hear from you\!

- What human errors do you think are the most relevant to address in
  the workplace (i.e., more dangerous or pervasive)?

- How could a company nudge users or even IT guys to do what they
  should do?

- Are you a software developer? Tell us about how you infuse security
  while coding\! Do you have a strategy for that? Do you have a peer
  that takes care of it? Do you rely on us for this? (We hope you
  do\!)
