---
slug: cost-cybercrime-ii/
title: Evolution of Cybercrime Costs (II)
date: 2020-02-19
subtitle: Uber cuts $120 million after discovering ad fraud...
category: attacks
tags: security, risk, vulnerability, business, policies, economics
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330837/blog/cost-cybercrime-ii/cover_vnfqpv.webp
alt: Photo by Jp Valery on Unsplash
description: Here we conclude our review of 'Measuring the cost of cybercrime'
  by focusing, among other things, on ad fraud,
  which appears to be a bit underrated.
keywords: Security, Risk, Vulnerability, Business, Policies, Economics,
  Ethical Hacking, Pentesting, WEIS
author: Julian Arango
writer: jarango
name: Julian Arango
about1: Behavioral strategist
about2: Data scientist in training.
source: https://unsplash.com/photos/9BatP4ovW2I
---

In a previous blog post, we discussed some of the findings of Anderson
et al. (2019) regarding the changes in cybercrime costs, more
prominently in the United States and the United Kingdom. We specifically
wrote about online card and banking fraud, as well as ransomware and
cryptocurrencies. We introduced these topics by referring to what had
changed in the last seven years when a first paper from the same authors
was presented at the Workshop on the Economics of Information Security
`(WEIS)` in 2012. We will conclude with other topics detailed in the
study. Check the first part of this blog post
[here](../cost-cybercrime-i/).

We will discuss marketing-related cyber crimes like ad fraud, and
Business Email Compromise `(BEC)` primarily. We found ad fraud figures
astonishing. Fortunately, awareness is growing as businesses are
starting to realize they have probably lost plenty of money without
knowing it. The second topic caught our eyes as it appears to be on the
rise. Although not related, we remembered Amazon’s CEO, Jeff Bezos, as
the hack he suffered was specific and directed to him. Let’s begin.

## Online advertising fraud (ad fraud)

We consider ad fraud to be underrated. This fraud happens when
advertisers' digital-ads budgets are stolen: sold ads that were never
seen by humans. These frauds could be categorized within
impression-fraud (paid fake impressions), click fraud (paid fake
clicks), and traffic laundering (fake traffic).

Partially, the problem emerges because there’s no authentication to
verify that users are actually viewing the ads the advertiser is paying
for. A way criminals use to profit from this is by creating browser
“viewing” ads automatically (especially video ads). How? By
compromising computers through malware installed to perform this.

It is estimated that for every ad fraud revenue dollar, the advertiser
spends between $2 and $5 to serve those ads. One well-documented example
in the cited paper tells the story of two ad campaigns with losses of
$36m. There were 1.900 servers and 850.000 `IP` addresses under control
of criminals to scale such frauds. Still, these were not part of a
botnet (the criminals paid for those resources).

The scholars argue that conflicts of interest exist between advertisers
and ad networks. Those conflicts impose barriers to better measuring the
impact of these cybercrimes. The researchers also estimate global losses
to be a couple of billions worldwide every year.

<div class="imgblock">

![Fake](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330837/blog/cost-cybercrime-ii/fake_ifrq2y.webp)

<div class="title">

Figure 1. Image by [Gordon Johnson](https://pixabay.com/users/gdj-1086657/)
from [Pixabay](https://pixabay.com/vectors/real-fake-typography-type-text-3166209/)

</div>

</div>

An outstanding example depicts the size and impact of these frauds. Uber
made a significant reduction in its digital marketing budget: **120
million out of 150 million dollars were cut with no performance
impact**, after discovering ad fraud. You can listen to this story
[here](https://www.alistdaily.com/lifestyle/kevin-frisch-uber-ad-fraud/),
told by Kevin Frish, former head of performance marketing and `CRM` for
Uber, interviewed by Alan Hart. Read along with us: ONE HUNDRED AND
TWENTY MILLION DOLLARS.

## Fraud on discount-like coupons and loyalty programs

We also consider that this type of fraud is underrated. Think about a
simple scenario: a company has a discount scheme through coupons, as
part of their marketing strategy to attract underserved market segments.
A criminal could gain access to the company’s systems and create
non-authorized coupons that can be sold in the black market (e.g., the
dark web) for a fraction of its value. Anderson and colleagues suggest a
hypothetical and straightforward scenario: a criminal could sell 2.000
coupons with a monetary value of $50. If all these coupons were used,
losses for the victim company would add up to $100.000. Only in the US,
losses from these frauds are estimated between $300m and $600m per year.

Similarly, loyalty programs have also suffered financial losses from
attackers. According to the cited paper, this fraud is growing. From
2016 to 2017, for instance, a publication reported a rise in attacks on
these rewards/points accounts of 9 percentage points. Another paper
estimated losses in these programs adding up to $235m. Furthermore,
other costs have been identified. A survey found that 17% of victims of
loyalty program fraud would stop doing business with the company, and
37% would tell others about the vulnerability of the program. How much
profit can be lost due to these soon-to-left consumers?

## Business Email Compromise (BEC)

Also known as “man-in-the-email attack” or “CEO scam,” this kind of
fraud seems like a phishing attack but has several unique elements.
First, performing the attack focuses on someone with the power to make
wire transfers, like a financial manager. Second, the attack supplants a
CEO or someone with authority and, third, using this impersonation, a
request to make a wire transfer to a supposed valid account —controlled
by the criminal— is made.

<div class="imgblock">

![plot](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330836/blog/cost-cybercrime-ii/plot_xk0lbb.webp)

<div class="title">

Figure 2. Adapted from FBI’s IC3 as cited in [Anderson et al.
(2019)](https://weis2019.econinfosec.org/wp-content/uploads/sites/6/2019/05/WEIS_2019_paper_25.pdf)

</div>

</div>

`BEC` has been growing over the years, as can be seen in Figure 2. Note
that complaints have grown almost linearly, while estimates of financial
losses have grown exponentially.

The effectiveness of this fraud is rooted in human psychology. Similar
to typical phishing, “\[attackers\] prey on the victim’s instinct to
respond quickly to a request from a person of authority within the
company” (Anderson et al., 2019, p. 15). This is also known as the
*messenger effect*, widely cited in the behavioral science literature.

## Other interesting topics covered in the study

The scholars go further, pointing to other frauds and their costs to
businesses and society. Moreover, they extend their analyses on
cybercrime costs by discussing what infrastructure criminals use to
create such damages, mainly botnets. In the paper, the scholars also
review other relevant research that they call victimization studies.
These are nation-representative surveys where people self-report whether
they have been victims of cybercrime. This perspective is valuable as it
allows researchers and policymakers to contrast different sources of
insight to better come up with strategies against cybercrime. We invite
you to take a look at the paper if this topic interests you. Click
[here](https://weis2019.econinfosec.org/wp-content/uploads/sites/6/2019/05/WEIS_2019_paper_25.pdf)
to download it.

## As a whole, society loses

From the figures these scholars put together, it’s clear that the costs
of cybercrime on society are relevant. Cybersecurity is not an isolated
topic for just a bunch of organizations. Quite the opposite:
cybersecurity is essential to society, as we now rely heavily on
information technology which offers many benefits in these modern times.

At `Fluid Attacks`, we’re committed to improving the safety of
organizations by putting some pressure on their mission-critical
systems. We do this by hacking those systems with a mix of automated
tools and the expertise of a group of highly skilled security engineers.
Check our [hacking services](../../services/continuous-hacking/) and our
[solutions](../../solutions/) (there is one product you can access and
use `FREE` of charge). Our distinctiveness lies in the approaches we
offer to organizations, comprised of [continuous
hacking](../../services/continuous-hacking/) and [one-shot
hacking](../../services/one-shot-hacking/). We detect weaknesses faster,
featuring a rich characterization, and we also make it easier for
clients to fix those defects through our ASM and Asserts.

Did you enjoy reading this post? We love to hear from our readers and
customers. [Do get in touch with us\!](../../contact-us/)

## References

1. Anderson, R., Barton, C., Böhme, R., Clayton, R., Gañán, C., Grasso,
    R., Levi M., Moore, T. & Vasek, M. (2019). [Measuring the changing
    cost of
    cybercrime](https://weis2019.econinfosec.org/wp-content/uploads/sites/6/2019/05/WEIS_2019_paper_25.pdf).
    Proceedings of the 17th Workshop of the Economics of Information
    Security (WEIS). Boston, MA.
