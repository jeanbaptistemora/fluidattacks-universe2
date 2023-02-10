---
slug: tiber-eu-framework/
title: Have You Heard About the TIBER-EU?
date: 2022-05-09
subtitle: An exemplary initiative to evaluate and protect systems
category: philosophy
tags: cybersecurity, red-team, blue-team, security-testing, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1652118259/blog/tiber-eu-framework/cover_tiber_eu_framework.webp
alt: Photo by Immo Wegmann on Unsplash
description: In this post, you will learn about TIBER-EU, an initiative of the European Central Bank that assesses European entities' cyber resilience.
keywords: TIBER EU, Framework, Test, Europe, Red Team, Threat Intelligence, Cyber Resilience, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/Ym2mFGr4GWI
---

[Back in 1988](https://www.ecb.europa.eu/ecb/history/html/index.en.html),
some European countries decided to create an economic union
that would allow the free movement of capital between them
and would have a shared authority
and a single monetary policy.
Years later,
they defined and adopted a common currency,
the euro,
which emerged along with the [euro area](https://en.wikipedia.org/wiki/Eurozone),
which now includes 19 of the 27 member states of the European Union (EU).
Today,
the institution governing that currency is the European Central Bank (ECB).
It is about an initiative related to cybersecurity
within this organization
that we will discuss in this blog post.

[Apart from](https://www.ecb.europa.eu/ecb/html/index.en.html)
helping to maintain prices stable in the euro area,
the ECB makes significant efforts
to contribute to the security of European banking.
[Since 2014](https://www.ecb.europa.eu/ecb/educational/explainers/tell-me-more/html/anniversary.en.html),
they have been monitoring
the soundness and resilience of banks in the area,
requiring them to make adjustments
whenever any irregularities appear.
In the digital context,
the ECB is firmly seeking to protect users' money from cyber threats
and acts preventively with the financial community.
Specifically,
they test their entities' security and cyber resilience.
[As they say](https://www.ecb.europa.eu/paym/cyber-resilience/html/index.en.html),
"Cyber resilience refers to the ability
to protect electronic data and systems from cyber attacks,
as well as to resume business operations quickly
in case of a successful attack."
They test it with the help of [ethical hackers](../what-is-ethical-hacking/).
These procedures are based on the [TIBER-EU](https://www.ecb.europa.eu/paym/cyber-resilience/tiber-eu/html/index.en.html).

## What is the TIBER-EU and how does it work?

The TIBER-EU (Threat Intelligence-based Ethical Red Teaming)
is a common framework
developed by the EU national central banks and the ECB,
published in 2018.
It guides authorities,
entities
and threat intelligence (TI)
and [red teaming](../../solutions/red-teaming/) (RT) providers
in controlled cyberattacks
and in improving the entities' cyber resilience.
Following the approach of a red team,
such as `Fluid Attacks`,
their tests seek to mimic malicious attackers' tactics,
techniques and procedures.
They intend to [simulate real attacks](../../solutions/attack-simulation/)
on their entities' systems,
especially on their critical operations,
to determine their weaknesses and strengths
and thus drive their growth in their cybersecurity maturity level.
(This reminds us of the [OWASP SAMM](https://fluidattacks.docsend.com/view/4k524b3gviwqubri),
which you can employ,
for instance,
to assess the maturity
of your [security tests](../../solutions/security-testing/).)

Several teams are involved in the TIBER-EU tests.
On the side of the entity
(generally from the financial sector)
to be evaluated are the blue and white teams.
The former is the one that is unaware
that it's going to be the target of simulated attacks
aimed at assessing its prevention,
detection and response capabilities.
The latter is a narrow group of people
that knows about the procedure and contributes to its execution.
On the other hand,
there are TI and RT providers.
The first company analyzes the spectrum of potential threats
and conducts a reconnaissance of the entity.
The second company is in charge of [ethical hacking](../../solutions/ethical-hacking/)
or well-meaning attacks against the entity's systems
and their critical operations.
Lastly,
there is the TIBER cyber team.
This group belongs to the authority
and is responsible for the supervision of the test
to ensure compliance with the framework's requirements.

<cta-banner
  buttontxt="Read more"
  link="/solutions/red-teaming/"
  title="Get started with Fluid Attacks' Red Teaming solution right now"
/>

The TIBER-EU also manages requirements for TI and RT providers.
The entity to be tested must verify they are met
before working with these companies.
These are [selection standards](https://www.ecb.europa.eu/pub/pdf/other/ecb.1808tiber_eu_framework.en.pdf)
we will talk about in a future post.
For the time being,
let's gain some insight into the [testing procedure](https://www.ecb.europa.eu/pub/pdf/other/ecb.tiber_eu_framework.en.pdf).
The authorities in European nations,
in discussion with the entities under their responsibility,
determine in which cases and when to carry it out.
To be recognized as a TIBER-EU test,
this process must be performed by independent external providers
and not by the entities' internal teams.
The framework stipulates that
this test must be divided into three phases:
preparation, testing and closure.

<div class="imgblock">

![TIBER-EU Process](https://res.cloudinary.com/fluid-attacks/image/upload/v1652118200/blog/tiber-eu-framework/tiber_eu_process.webp)

<div class="title">

Image taken from [ecb.europa.eu](https://www.ecb.europa.eu/pub/pdf/other/ecb.tiber_eu_framework.en.pdf).

</div>

</div>

Before the preparation phase,
TIBER-EU offers an optional one:
the **generic threat landscape phase**.
This step is to conduct "a generic assessment
of the national financial sector threat landscape."
It involves mapping the entity's role
and identifying current high-end threat actors for the sector
along with their methods against this kind of entity.
In the **preparation phase**,
the teams responsible for the test are defined
along with the scope of the test.
The authority validates the above,
and the entity hires the TI and RT providers.

In the **testing phase**,
the TI company elaborates a "Targeted Threat Intelligence Report,"
presenting threat scenarios
and relevant information about the entity.
(The generic threat landscape from the optional phase would serve
as the basis for this stage.)
The RT company uses all this to develop attack scenarios
and execute controlled attacks
against "specified critical live production systems,
people and processes that underpin the entity's critical functions."

In the **closure phase**,
the RT provider offers a "Red Team Test Report"
with details of the employed methods,
as well as the findings and evidence from the test.
On a case-by-case basis,
this report may include recommendations for the tested entity
to improve in areas such as policies,
operations, controls or awareness.
Key stakeholders review and discuss the test
and the issues discovered.
Then the entity,
which receives detailed technical evidence
on its weaknesses or vulnerabilities,
agrees to and completes a "Remediation Plan."

For everyone involved,
it should be clear that TIBER-EU tests carry risks.
For example,
testing can result in data loss,
alteration and disclosure,
system downtime and damage,
and denial-of-service cases.
This is why the TIBER-EU framework is strict
and prioritizes the establishment of solid risk management controls
to be employed throughout the process.
The framework states that for testing to be secure,
the roles and responsibilities of all stakeholders
must be adequately defined and understood.
In addition,
in line with what we mentioned earlier,
and which we will discuss later,
TI and RT vendors must comply with specific requirements.
It is expected "to ensure that
only the best and most qualified personnel
conduct such sensitive tests on critical functions."

Something fundamental
that this sophisticated and robust initiative does
is to contribute "To provide an appropriate level of assurance
that key financial services assets and systems are protected
against technically competent,
resourced and persistent adversary attacks."
European authorities rely on TI and RT providers' methodologies
to assess their entities' security and reduce risks.
Why is it that so many organizations are still engrossed
in relying solely on less-than-accurate automated scanning tools?
We've said it before:
To stay one step ahead of the malicious hacker,
you need someone who thinks like them.
You require ethical hackers.
Would you like to count on the assistance of `Fluid Attacks'` ethical hackers?
[Contact us!](../../contact-us/)
