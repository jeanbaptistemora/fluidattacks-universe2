---
slug: cyber-insurance-ransomware/
title: Ransomware and Cyber Insurance
date: 2021-07-29
subtitle: Why is security always excessive until it's not enough?
category: attacks
tags: cybersecurity, company, trends, risk, vulnerability, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1627561560/blog/cyber-insurance-ransomware/cover-cyber-insurance-ransomware_lflmzi.webp
alt: Photo by Chris Curryon on Unsplash
description: This post will deepen in the relation between cyber insurance
  and ransomware popularized by the Royal United Services Institute
  last report.
keywords: Ransomware, Attack, Vulnerability, Insurance, Cybersecurity,
  Ethical Hacking, Cyber, Pentesting
author: Felipe Zárate
writer: fzarate
name: Felipe Zárate
about1: Cybersecurity Editor
source: https://unsplash.com/photos/ybxugA_CWoM
---

On June 28, the Royal United Services Institute (RUSI) published [a
report](https://rusi.org/explore-our-research/publications/occasional-papers/cyber-insurance-and-cyber-security-challenge)
explaining why cyber insurance spurs ransomware attacks. After its
publication, several blogs emerged summarizing or detailing the problem
(I recommend
[ZDNet](https://www.zdnet.com/article/ransomware-has-become-an-existential-threat-that-means-cyber-insurance-is-about-to-change/)
,
[PCrisk](https://www.pcrisk.com/internet-threat-news/21233-is-cyber-insurance-making-it-harder-to-defend-against-ransomware),
[TechTimes](https://www.techtimes.com/articles/261595/20210617/ransomware-attacks-pressure-insurance-companies-limit-coverage-cybercrimes.htm)
and [Security
Intelligence](https://securityintelligence.com/news/whats-behind-rising-ransomware-costs/)
articles). This blog post is not intended to summarize the RUSI report.
Instead, it will use it to describe and explain the relationship between
cybersecurity insurance and the rise of ransomware.

Let’s start by setting out the figures. We will use, primarily, the
FBI’s [2020 Internet Crime
Report](https://www.ic3.gov/Media/PDF/AnnualReport/2020_IC3Report.pdf),
of which we already made a [blog post](../fbi-2020-report/). According
to this report, in the United States alone, "2,474 complaints identified
as ransomware with adjusted losses of over $29.1 million" were received.
This amount was estimated with a considerable margin of error since the
final number does not include dozens of factors that could considerably
increase the monetary loss. It does not take into account, for example,
the economic loss that involves the extra investment of time, equipment,
or additional salaries to those who must decrypt the files (or the
insurance payment, if any). It also does not consider cases not reported
to the FBI; a widespread practice since companies might prefer to pay
for ransomware before it is known that their security system was
breached.

If we consider the monetary loss of ransomware over the last three
years, it is easy to see the exacerbated increase (see Figure 1). From
paying **$3,621,857** in **2018**, it went on to pay **$29,157,405** in
**2020**. This means a **705% increase** in the **total loss** due to
ransomware in three years. Why have ransomware price demands skyrocket
that way?

<div class="imgblock">

![ransomware-complaint-loss-comparison](https://res.cloudinary.com/fluid-attacks/image/upload/v1627562361/blog/cyber-insurance-ransomware/ransomware-complaint-loss-comparison_btczd1.webp)

<div class="title">

Figure 1. Crime types by victim loss by [FBI’s 2020 Internet Crime
Report](https://www.ic3.gov/Media/PDF/AnnualReport/2020_IC3Report.pdf).

</div>

</div>

## Ransomware and payments: a vicious cycle

Cybercriminals know that ransomware is a **profitable activity** because
there is always someone willing to pay. In this regard,
[Threatpost](https://threatpost.com/cyber-insurance-ransomware-payments/166580/)
published that 41 percent of claims made to cyber insurance corresponded
to ransomware attacks during 2020. According to
[Bloomberg](https://www.bloomberg.com/news/articles/2021-05-20/cna-financial-paid-40-million-in-ransom-after-march-cyberattack),
the cyber insurance company CNA paid $40M at the end of March in
response to a ransomware attack. With a single attack, cybercriminals
get millions of dollars. That’s a lot more than most midsize businesses
would earn in a year. [Jennifer
Granholm](https://www.nbcnews.com/now/video/can-cyber-insurance-keep-up-with-the-growing-number-of-ransomware-attacks-116154437896),
Secretary from the Department of Energy of the USA, said about it:
"Paying ransomware only exacerbates and accelerates this problem. You
are encouraging the bad actors when that happens."

However, if the ransomware is not paid, how can a victim decrypt their
files? Indeed, Andre Nogueira, CEO of [JBS](../jbs-revil-cyberattack/),
and Joseph Blount, CEO of [Colonial
Pipeline](../pipeline-ransomware-darkside/), posed this same question.
In the end, both decided that the most immediate solution was to pay the
sum requested by the attackers. And these are not isolated cases. Five
years ago, [IBM did a
study](https://www.healthcareitnews.com/news/ransomware-70-businesses-attacked-pay-ibm-study-finds)
in which it concluded that 70% of businesses attacked by ransomware
paid, a figure that by 2020 only decreased by 2%, according to
[Statista](https://www.statista.com/statistics/701282/ransomware-experience-of-companies/).

Of course, all of this results in a vicious circle that can be completed
in two steps. First, cybercriminals encrypt information and demand money
to unlock it. Second, insurance pays those demands to release the
information. Recently, however, cybercriminals noticed a way to demand
money in addition to asking for the decryption of information:
blackmail. Cybercriminals realized that [they are successful
in](https://www.zdnet.com/article/ransomware-theres-been-a-big-rise-in-double-extortion-attacks-as-gangs-try-out-new-tricks/)
asking for money to prevent them from leaking and publishing that
information. Criminals play with companies' operations, their reputation
and, more worryingly, with legal issues. Therefore, companies that work
with sensitive information are often the most affected in this regard.
Hence, organizations working in the education sector or government
entities (which manage a lot of sensitive data) have been two of the top
targets of ransomware during 2021, according to the [Cloudwards
portal](https://www.cloudwards.net/ransomware-statistics/).

## The list goes on and on

Added to all these series of unfortunate events, with the arrival of
cryptocurrencies, criminals solved the problem they had with laundering
money. In an interview with the ZDNet’s senior reporter, Danny Palmer,
the Chief Digital Officer of Mars Incorporated, [Sandeep
Dadlani](https://www.zdnet.com/article/ransomware-has-become-an-existential-threat-that-means-cyber-insurance-is-about-to-change/)
argued that criminals didn’t know how to withdraw the money they charged
without raising suspicions. Now that the system is decentralized, it is
not possible to see where that money is going. The involvement of cyber
insurance companies had aggravated the problem. Before, a criminal could
only demand what a person could afford for decrypting their data. There
was no point in charging more. Now, they go for the big companies
because they know that behind them is an insurance company backing them
financially. This same point is made by the [RUSI
report](https://static.rusi.org/263_ei_ransomware_final_0_0.pdf):
"\[…​\] when an organisation has a cyber insurance policy, it might
be able to claim the ransom back, which may encourage payment."

The problem is accentuated to the extent that it would be cheaper to pay
the ransom than to regain the trust of customers and investors. If data
were to be leaked, the company’s reputation would be severely damaged.
Suppose the monetary and reputational convenience of paying the ransom
is added to the urgency of certain organizations to resume their
services. In that case, you get a cocktail that should be taken quickly
and almost without hesitation. [Security
Intelligence](https://securityintelligence.com/news/whats-behind-rising-ransomware-costs/)
already pointed it out: "agencies that are responsible for upholding a
nation’s critical infrastructure \[…​\] can’t afford to suffer a
prolonged disruption." This happens with companies in the health,
transport, or food sector. It was the case of, for example, [Colonial
Pipeline](../pipeline-ransomware-darkside/) and
[JBS](../jbs-revil-cyberattack/).

## Not today

We come back to the question we had already asked. If we all know that
paying for ransomware is financing these criminal groups, what should we
do? [Joshua
Motta](https://www.nbcnews.com/now/video/can-cyber-insurance-keep-up-with-the-growing-number-of-ransomware-attacks-116154437896),
CEO of [Coalition](https://www.coalitioninc.com/), a USA cyber insurance
company, gives us some insights that his own company always puts into
practice. They demand compliance with specific prevention criteria by
the companies that request their services. "In order to qualify for
insurance, you shouldn’t be doing the types of things that are going to
make you a target of a criminal actor," says the CEO. To do so, the
insurance company itself trains its potential clients to strengthen
their prevention practices. This may seem weird for an insurance
company. It is not common for car insurance, for example, to teach how
to drive to their potential customers before agreeing to concluding the
deal.

<div class="imgblock">

![Counter Ransomware](https://res.cloudinary.com/fluid-attacks/image/upload/v1627562360/blog/cyber-insurance-ransomware/counter-ransomware_wkr8b1.webp)

<div class="title">

Figure 2. “Summary of Areas of Potential Action to Counter
the Ransomware Threat” in [RUSI report](https://static.rusi.org/263_ei_ransomware_final_0_0.pdf).

</div>

</div>

We at `Fluid Attacks` believe this is the right path to take. Enough of
keep thinking that [*my company will not be
attacked\!*](../optimism-bias/) The best way to stop cyberattackers is
not to give them the option to attack. In other words, we must be
prepared. **Prevent ransomware attacks is the best way to avoid them**.
We must not leave so many things to chance: on the contrary, we must
integrate a robust security system from the outset of our software
development. The infrastructure must be constantly and continuously
tested. Stopping ransomware is everyone’s responsibility. Avoid crying
over spilled milk; instead, prepare yourself never to spill it.

We hope you have enjoyed this post!\
At `Fluid Attacks`, we look forward to hearing from you.\
[Contact us](../../contact-us/)!
