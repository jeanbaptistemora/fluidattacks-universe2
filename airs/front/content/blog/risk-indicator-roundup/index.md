---
slug: risk-indicator-roundup/
title: Risk Indicator Roundup
date: 2019-05-15
subtitle: A matter of taste
category: philosophy
tags: business, ethical-hacking, risk
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331066/blog/risk-indicator-roundup/cover_azhwyk.webp
alt: 'Choices. Photo by Nathan Dumlao on Unsplash:
  https://unsplash.com/photos/pMW4jzELQCw'
description: Here we compare risk indicators used in quantitative finance,
  giving their pros and cons. Most of them we have discussed earlier,
  but here we introduce the ALE.
keywords: Risk, Probability, Choice, Measure, Quantify, Indicator,
  Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/pMW4jzELQCw
---

What is the best risk indicator? Bottom line: there is no "best", only
different approaches to the same thing. Ultimately, it’s up to you. Here
we will show the pros and cons of each risk indicator so you can make an
informed decision.

## VaR

[Recall](../para-bellum/) that Value at Risk (`VaR`) measures the
worst-case scenario in an uncertain return by telling us the endpoint
beyond which our losses will likely not go, up to a certain degree of
confidence, in a definite period of time. Thus a daily 1% `VaR` of $10
million means the probability that you will lose more than $10 million
is 1%, which is the same as saying that you are 99% confident that the
losses will not exceed $10 million.

Pros:

- Gives a good idea of how much to save in order to avoid bankruptcy
  in most (95%) cases.

- Is a well-established standard, used by most banks and a requirement
  per international banking regulations.

Cons:

- Says nothing about what might happen beyond the threshold.

- Is a single number, therefore, its expressiveness is rather narrow.
  It says nothing about what happens elsewhere with the distribution
  of returns.

## tVaR

While the `VaR` gives a worst-case scenario with a certain confidence,
what if that confidence is broken, i.e., the `VaR` is breached? What can
we expect? That’s precisely the *tail* value at risk tries to answer. By
using the [expected value](../great-expectations/) of a [conditional
probability](../updating-belief/#mathematical-interlude), it gives us,
in a single number, what would be expected if a worst-case scenario
occurs.

There is no better way than this plot by
[Nematrian](http://www.nematrian.com/TailValueAtRisk) to summarize both
`VaR` and `tVaR`.

<div class="imgblock">

![(t)VaR illustration](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330968/blog/para-bellum/tvar_fg6jpf.webp)

<div class="title">

Figure 1. (t)VaR illustration

</div>

</div>

Pros:

- Prepares you for the worst of the worst.

- Single number, easy to compare or monitor over time.

Cons:

- Not easy to compute (involves an integral).

- Results can be overly pessimistic, thus impeding you from seeing the
  other side of the coin.

## ALE

This is a relatively new one. Remember we discussed Return on Control
(`ROC`) to decide whether investing in a given defense is worth the
hassle?

<div class="imgblock">

![Return on control](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330936/blog/monetizing-vulnerabilities/roc_qfbvd2.webp)

<div class="title">

Figure 2. Return on control

</div>

</div>

The change in loss was obtained from two simulated scenarios: one with
the control and another without it. Both were obtained by "averaging
out", i.e. finding the [expected value](../great-expectations/) of a
simulated distribution for the loss.

The Annualized Loss Expectancy (`ALE`) is related to such a computation
in that it is also obtained from a couple of expected, estimated values.
These estimated values are the expected number of ocurrences of an event
in a year (the Annualized Rate of Occurrence, `ARO`), and the expected
loss for a single ocurrence (Single Loss Expectancy, `SLE`). Thus, total
= reps x single. Too many acronyms for too little content:

<div class="imgblock">

![Acronyms joke](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331065/blog/risk-indicator-roundup/wenus_anm8lr.webp)

<div class="title">

Figure 3. You don’t want to ask Chandler about his Annual Net Usage Statistics!

</div>

</div>

Experts can estimate the ARO. Suppose it is known that a data breach
will most likely occur at least once in 10 years. The `ARO` for such an
event is 1/10 = 0.1 events per year. The `SLE` is to be estimated by
your own experts. How much would such a breach cost you? Say, $100
million. Then the loss expected in every one of those years is 0.1x100 =
$10 million. However, this rate will be fixed for each of the next ten
years. It is static and unlikely to be true since risks and threats
change daily.

Pros:

- Simple computation.

- Single number, thus easy to compare.

Cons:

- You’re stuck with the one year period.

- Not very "realistic".

## LEC

The loss exceedance curve is a decidedly different one, and one of our
favorites at that. We have already discussed it at length in our
[introduction to quantitative risk](../quantifying-risk), our general
[Monte Carlo simulation article](../monetizing-vulnerabilities), and
gave an example of implementing in [Quantitative
Python](../quantitative-python). In a nutshell, it’s a graph that tells
you the probability of losing a given amount or more of money, for any
amount in a range. It’s like having all possible values-at-risk for all
confidence levels. We believe the graph speaks for itself.

<div class="imgblock">

![Loss Exceedance Curve](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330935/blog/monetizing-vulnerabilities/simple-lec_troyzh.webp)

<div class="title">

Figure 4. Loss Exceedance Curve from [Hubbard et
al.](https://www.howtomeasureanything.com/cybersecurity/)

</div>

</div>

Pros:

- All the information you could want about losses in a single plot.

- Since it’s a visual tool it’s helpful when you’re considering a
  range of risks you’re willing to take, especially when it’s combined
  with residual risk and risk tolerance curves.

Cons:

- Harder to compare since it’s not a single number.

- Harder to obtain, since it involves simulations.

---
Overall, single number risk indicators (`ALE`, `VaR` and `tVaR`) are
good for making quick comparisons and monitoring them over time. In
contrast, the `LEC` might allow you to make a more fine-grained decision
regarding how much risk you are willing to take vs. how much you would
have to lose in many different scenarios, all in a single chart.

For ease of use, we’d say `ALE` is the winner. However, we wouldn’t
expect its predictions to be the most accurate of the lot. Also, its
time period (one year) might be too much for the fast-paced market we
currently live in. If you have to choose one single-number indicator, we
would recommend using `VaR`, wich international banking regulations
([Basel II](https://www.investopedia.com/terms/b/baselii.asp)) use,
since the `tVaR` might be a tad too extreme.

In the end, it’s your choice. Or there might not be any choice to make
at all. Who says you cannot use them all at once? If done well, they
should not be contradictory, but complimentary. Find out all you can
about your investment, use all the tools at hand, and then make the best
decision possible in terms of risk vs gain.
