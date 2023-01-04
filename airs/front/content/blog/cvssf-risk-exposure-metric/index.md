---
slug: cvssf-risk-exposure-metric/
title: What Your Risk Management's Missing
date: 2022-11-16
subtitle: Why measure cybersecurity risk with our CVSSF metric?
category: philosophy
tags: cybersecurity, risk, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1668626573/blog/cvssf-risk-exposure-metric/cover_cvssf.webp
alt: Photo by Maxim Hopman on Unsplash
description: We present some of the flaws of the traditional measure of cybersecurity risk and introduce CVSSF, the risk-exposure-based metric with which we overcome them.
keywords: Cvss, Cvssf, Risk Exposure, Risk Management, Cybersecurity Risk Management, Cybersecurity Success, Security Status, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/HBkuFoJuwDI
---

Cybersecurity incidents are on the rise,
evidencing the fault in the traditional approach
that guides how to prioritize risk management.
Thus,
organizations worldwide are in urgent need of alternatives
that yield useful information
to help them make better decisions in cybersecurity.
To contribute to solving this problem,
we propose our CVSSF metric.
This is a risk-exposure-based value
that enables organizations
to improve the prioritization of vulnerabilities in remediation.
And mainly,
it gives them a more accurate measure of their security status.
In this blog post,
we will talk about the motivations for this metric
and evidence of its worthiness.

## Flaws of the traditional measure of cybersecurity risk

The cyber threats to organizations worldwide continue to grow.
The [number of devices connected to the Internet](../what-trends-to-expect-for-2023/)
is getting higher.
Thus,
organizations' attack surfaces
(i.e., points of exposure of IT systems to untrusted sources)
are bigger,
along with chances to get breached.
The [exploitation of single critical vulnerabilities](../cybersecurity-trends-2022/)
in third-party software
threatens to severely disrupt supply chains.
Attackers keep compromising [a great number of records](https://www.itgovernance.co.uk/blog/data-breaches-and-cyber-attacks-quarterly-review-q3-2022).
And all this comes
as the average cost of a data breach keeps breaking records.

The threats above are things
that every organization has to deal with
in their way to create value for their clients.
In short,
**aiming for success is a risky business**.
Indeed,
managing risk is arguably the most important issue to resolve in cybersecurity.
Accordingly,
standards and frameworks by renowned sources
(e.g., [NIST's](../nist-supply-chain-risk/),
[ISO's](../iso-iec-27002-2022/))
give firms a pretty good idea of controls to mitigate risk.
However,
the sheer amount of successful cyberattacks suggests
that the way firms are prioritizing risk mitigation is not working.

What is the faulty approach to cybersecurity risk management?
Well,
most firms use scores and risk maps from known standards.
This traditional approach,
of course,
takes into account that vulnerabilities differ
in the degrees to which they would affect a system if exploited.

One measure is the Common Vulnerability Scoring System ([CVSS](https://www.first.org/cvss/specification-document))
score,
widely used for communicating the characteristics
and severity of vulnerabilities.
Basically,
it quantifies the vulnerability's exploitability, scope and impact.
That is the base score,
which is further adjusted by temporal and environmental variables.
The result is a severity value between 0.0 and 10.0.
Most importantly,
this range is broken down into a qualitative severity rating scale,
where 0.0 = none;
0.1 - 3.9 = low;
4.0 - 6.9 = medium;
7.0 - 8.9 = high,
and 9.0 - 10.0 = critical.

Vulnerability scanning products generally provide the CVSS scores
of detected vulnerabilities.
This information is supposed to help organizations
reduce uncertainty in regard to what their security status is
and what to remediate first.

Generally,
what comes to mind is the aggregation of vulnerabilities
by adding up the quantitative CVSS scores.
This poses a difficulty.
We could have ten vulnerabilities with a score of 1.0 each,
and they would not represent the same risk as one of 10.0.
Likewise,
success in remediating those ten vulnerabilities
should not be seen as valuable as that in fixing that one critical flaw.
This raises the following possibility.

<div class="imgblock">

![CVSSF risk management - Fluid Attacks](https://res.cloudinary.com/fluid-attacks/image/upload/v1668627114/blog/cvssf-risk-exposure-metric/cvssf-risk-management-fluid-attacks.webp)

<div class="title">

Ten CVSS 1.0 vulnerabilities do not equal one CVSS 10.0 vulnerability.

</div>

</div>

Let's say instead we add up the number of vulnerabilities
by their qualitative CVSS scores.
Then,
we could keep a tally of,
say,
low, medium, high and critical severity vulnerabilities
which we would try to address separately.
This approach would yield
a complicated view of the security status of the system,
as it would not be unified.
This could be tolerated.
But a basic flaw is
that the segmentation of CVSS scores into qualitative levels is arbitrary.
For example,
a vulnerability is considered critical
only if it has been given a score of at least 9.0,
so one that is given a score of 8.9 is "just" a high severity one.
It is that difference of 0.1 that would mean the prioritization of the former,
while they could be threatening the system to a fairly similar degree of risk.

## Fluid Attacks' risk-exposure-based metric

At Fluid Attacks,
we recognize the limitations of the traditional approach.
We propose a new metric to contribute to measure risk more accurately,
providing information about the security status of the system
with which organizations can improve their prioritization
in the remediation of vulnerabilities.

Our proposal is a simple algorithm to find out the risk exposure
(i.e., the extent to which a system is vulnerable to successful cyberattacks).
We call it the CVSSF metric,
as it takes the CVSS base score
and adjusts it to show the exponential nature of severity.
"F" stands for "à la Fluid Attacks."
The formula is the following:

<div class="imgblock">

![CVSSF risk formula - Fluid Attacks](https://res.cloudinary.com/fluid-attacks/image/upload/v1668629343/blog/cvssf-risk-exposure-metric/cvssf-risk-formula-fluid-attacks.webp)

</div>

In this formula,
the constant P means "proportionality."
It determines
how many vulnerabilities of a given CVSS base score equal one vulnerability
of one more CVSS base score unit.
This can be determined by each organization.
But what have our pen testers observed?
They have reached a consensus to give P a value of 4.
You can understand this as follows:
"Four vulnerabilities of a CVSS base score of 9.0 equal one of 10.0."
As for the constant R, it means "range,"
and restricts the values of the CVSSF
to ones that the organization feels comfortable using.
Again,
we recommend using 4.

<div class="imgblock">

![CVSSF risk formula with values - Fluid Attacks](https://res.cloudinary.com/fluid-attacks/image/upload/v1668629362/blog/cvssf-risk-exposure-metric/cvssf-risk-formula-with-values-fluid-attacks.webp)

</div>

Our adjustment by proportionality enables us
to provide visibility to the riskiest vulnerabilities to a system.
Using the illustration of the scale shown above as an example,
those ten vulnerabilities at the left side together equal a CVSSF of 0.2.
And the one vulnerability at the right has a CVSSF of 4,096.0.

## Benefits of the CVSSF

The riskiest vulnerabilities may not appear as frequently
as low or medium severity vulnerabilities,
so when they all are aggregated per the traditional approach,
the importance of the riskiest could be overshadowed.
When organizations use the CVSSF,
they can see their aggregated risk exposure rise more dramatically
than it otherwise would
if one high to critical vulnerability is reported in their systems.

Case on point: Our [2022 State of Attacks](https://try.fluidattacks.tech/state-of-attacks-2022/)
documented
that 98% of the vulnerabilities we detected in the systems of our clients
were of a low or medium CVSS severity.
**Yet it was the remaining 2%
that generated 76% of the reported risk exposure**.
They were exclusively high or critical CVSS severity vulnerabilities.

So,
organizations using the CVSSF can **promptly prioritize remediation**
of the vulnerabilities representing a higher risk exposure.
If successful,
this would cause the aggregated risk exposure to go down significantly.
Also,
their uncertainty about their security status can be greatly reduced,
as they have an **accurate aggregated value** at their disposal
on which they can **base their goals for cybersecurity success**,
and which they can **use for predictions of potential losses**.

## Fluid Attacks detects the risk exposure in your system

At Fluid Attacks,
we offer [Continuous Hacking](../../services/continuous-hacking/),
helping our clients learn the security status of their systems
throughout the software development lifecycle.
We do this by leveraging security testing early and continuously
using a combination of automation and the manual work of our ethical hackers.

We've found
that the implementation of our manual security testing
(e.g., [penetration testing](../../solutions/penetration-testing/))
is invaluable.
By October 2022,
our hackers reported about **80%** of the risk exposure
attributed to vulnerabilities in the systems of our clients.
If clients depended only on tools,
their risk management would be jeopardized.

Want us to assess your system?
We provide the CVSSF units of every detected security issue
on our [Attack Resistance Management (ARM) platform](../../product-overview/).
You can also see the aggregated risk exposure,
as well as its management,
over time,
and benchmark it against that of best performing organizations.
From the platform,
you can assign remediation to developers in your team,
ask our hackers for guidance
and request reattacks to verify the effectiveness of your remediation efforts.

Start your [21-day free trial](../../free-trial/)
of Continuous Hacking Machine Plan today.

> **Note:**
> For a summarized presentation of our CVSSF metric,
> download the [white paper](https://try.fluidattacks.tech/report/cvssf/).
