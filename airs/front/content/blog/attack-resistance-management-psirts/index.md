---
slug: attack-resistance-management-psirts/
title: Outstanding Product Security
date: 2022-09-22
subtitle: How Attack Resistance Management can help PSIRTs
category: philosophy
tags: cybersecurity, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1663883952/blog/attack-resistance-management-psirts/cover_psirt.webp
alt: Photo by Marek Piwnicki on Unsplash
description: This post describes how Attack Resistance Management can help enhance the operational maturity of PSIRTs in vulnerability discovery, triage and remediation.
keywords: Attack Resistance Management, What Is Psirt, Product Security Incident Response Team, Ethical Hackers, Vulnerability Discovery, Vulnerability Triage, Vulnerability Remediation, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/zetUhDVYejc
---

Software solutions vendors need their technology
to be secure for their users.
Period.
When it's found not to be secure,
they have to activate a reliable process
that will allow them to fix the issues.
More specifically,
in this process,
their Product Security Incident Response Team (PSIRT)
has to handle the reports,
triage them,
orchestrate remediation
and address stakeholders through security advisories.
On paper,
this seems as straightforward as its end purpose.
However,
PSIRTs face several challenges
that affect their prompt action.
We will highlight these challenges
and how Attack Resistance Management (ARM),
a continuous process to map the attack surface,
assess manually its resistance to attacks
and increase it,
can help.

## What is PSIRT?

For the sake of clarity,
let's kick off this blog post
by stating what [PSIRTs](https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1)
are.
As the name suggests,
PSIRTs are teams created in organizations to respond to,
and sometimes find,
threats and flaws in their **products**.
Thus,
their role is different from that of Computer Incident Response Teams (CSIRTs).
The latter initiate actions
to assess security in their organization's **systems**
and fix the issues they detect.

With the sponsorship of executive leadership,
PSIRTs create policies
on how to manage vulnerabilities reported in their products
by inside or outside sources.
This legitimization enables the team to orchestrate actions
to require constant vulnerability remediation
and engage the communications,
sales,
support and legal teams
in the efforts of security assurance.

## What is Attack Resistance Management?

Also for the sake of clarity,
let's define Attack Resistance Management.
We're talking about a solution
that addresses the shortcomings in the cybersecurity of organizations
in regard to knowledge
about the entirety of their digital assets
and attack surface,
security testing frequency,
accuracy to perform such tests
and skill of the dev and sec teams.

Accordingly,
ARM involves the continuous performance of manual security tests
of the entire attack surface
to determine its risk exposure
and resistance to attacks.
Throughout this process,
remediation is made as soon as possible
with the technical support of [ethical hackers](../what-is-ethical-hacking/),
and the organizations' staff members
continuously improve their secure development practices.

## How ARM benefits PSIRTs in vulnerability discovery

The very basic [level of operational maturity](https://www.first.org/standards/frameworks/psirts/psirt_maturity_document)
of a PSIRT
requires it to set the channels
and the manner
in which it will receive reports
of vulnerabilities in its organization's products.
(We've talked about this more extensively [here](../iso-iec-29147/).)
Make no mistake: **reports do come in**.
How many and from what sources?
The answer to both can be "So many!"
Also,
these reports could be talking about a vulnerability
in one or several previous product versions.
It might even have been already fixed
by the time the PSIRT receives the report.
To top it all off,
if report sources do not use a standard,
machine-readable format to communicate vulnerabilities
(e.g., [OASIS SARIF](../oasis-sarif/)),
the team has to spend more time analyzing the cases.

Having no ARM implemented can make for a chaotic scenario
in which the progress of the PSIRT in vulnerability discovery is slowed down.
When ARM is in the house,
it boosts the team's operational maturity.
In this area,
this maturity is reflected in the following:

- The entire attack surface of the organization's products
  (e.g., web, cloud-based and mobile apps, IoT devices, email servers)
  is known
  and monitored constantly as the software evolves.

- Vulnerabilities are sought after constantly
  and proactively from the start of the software development lifecycle (SDLC),
  instead of in a reactive fashion.
  That is,
  the organization does not have to wait for outside researchers,
  PSIRTs, etc.,
  to find them.
  This constant security testing allows for opportunities
  to play out "what if" scenarios.

- Third-party
  and open-source software is constantly inventoried
  in a software bill of materials (SBOM)
  and monitored for security advisories.

- Vulnerability history
  (e.g., location, author, report date, status)
  is recorded in its entirety.

- Enough information is available
  to generate reports
  to measure the success of the team
  with metrics such as discovered vulnerabilities
  (and corresponding risk exposure)
  and response time.

The result is
that PSIRTs implementing ARM are able to determine more quickly
whether the vulnerabilities reported by outside sources
had already been identified.
If so,
these teams can easily look up
when the vulnerabilities were created
and what versions of the technology they affect.
Also,
it's easier for them to find out
whether the affected systems
and versions have been patched.

<cta-banner
  buttontxt="Read more"
  link="/solutions/vulnerability-management/"
  title="Get started with Fluid Attacks' Vulnerability Management solution
  right now"
/>

## How ARM benefits PSIRTs in vulnerability triage

A further challenge for PSIRTs is to triage vulnerabilities.
This involves determining the validity of the report.
At the basic level,
these teams need to establish what is considered a vulnerability,
how vulnerabilities should be prioritized
and how capable their staff is of understanding the way the issue works.

Without ARM,
it is way more difficult to know
whether the reported issues can be reproduced in the vendor's environment.
Moreover,
a (possibly) lower technical expertise,
or use of automated tools only,
makes it challenging
to accurately define
whether the report is not a false positive and,
if proven not to be,
what level of risk the vulnerability represents.
Besides,
as attack simulations are not constantly performed,
meaning teams spend less time triaging and analyzing vulnerabilities,
prioritization standards are learned more slowly.

Optimal ARM guarantees PSIRTs the following in regard to triage and analysis:

- Highly certified ethical hackers probe the system for complex vulnerabilities
  and design exploits.
  Thus,
  these professionals' technical expertise allows
  for a more accurate qualification of vulnerabilities
  and their impact
  (e.g., corresponding risk exposure),
  as well as a faithful reproduction of them.

- In line with the previous,
  ethical hackers provide knowledge
  to improve the vulnerability qualification criteria.

- The constant,
  comprehensive security testing keeps the triage process oiled up,
  thus allowing time to gain knowledge about prioritization.

In short,
ARM enables PSIRTs to more accurately validate,
understand and reproduce vulnerabilities,
thus achieving a more advanced maturity level.

## How ARM benefits PSIRTs in vulnerability remediation

At a basic level,
PSIRTs have to determine how to deal,
if at all,
with the risk accompanying confirmed vulnerabilities
in their organizations' products.
Remediation is harder
when there is no ARM in place,
as a proactive manual search for vulnerabilities
and a strong remediation culture may not be established.
Moreover,
the staff's lack of expertise
and no assistance from qualified hackers can result
in a more challenging
and error-prone remediation process.

These are some ways in which ARM can enhance the maturity of PSIRTs
in regard to remediation:

- Ethical hackers support the process
  with recommendations and guidance.

- The team can orchestrate remediation early in the SDLC
  (i.e., prior to product release),
  and by doing so constantly
  they can achieve a strong remediation culture.

- The constant,
  comprehensive reports
  of remediated risk exposure represented by vulnerabilities
  can help the organization learn
  how strong is their commitment towards security
  and whether it is providing a fix
  within the specified service-level agreement timeframes,
  among other success metrics.

At an advanced maturity level,
through constant support of world-class ethical hackers over ARM,
PSIRTs can quickly and effectively remediate vulnerabilities,
early and throughout the entire SDLC.
Furthermore,
they can readily access relevant data
to inform stakeholders
how the security of the products is evolving.

## Attack Resistance Management with Fluid Attacks

`Fluid Attacks` offers [Attack Resistance Management](../../platform/arm/)
as part of its [Continuous Hacking](../../services/continuous-hacking/)
solution.
In it,
`Fluid Attacks'` ethical hackers
test the security of client organizations' products
continuously throughout the SDLC.
Clients manage each of their products' attack surface
on `Fluid Attacks'` Attack Resistance Management platform
([ARM](https://app.fluidattacks.com/)),
where the security testing results are readily available,
showing exhaustive details,
history
and evidence of the vulnerabilities that are found.
Through this platform,
PSIRTs can assign the remediation of vulnerabilities to their staff
and access helpful metrics
on how well they're reducing risk exposure in their products.
This platform also offers support options
that connect PSIRTs with hackers
who can help remediation with further details.
And all that is just a bit of what the ARM offers.

Are you interested in securing your product
with the best solution?
[Contact us](../../contact-us/).
If you just want to explore `Fluid Attacks'` ARM,
get the [21-day free trial](https://app.fluidattacks.com/SignUp)
of Continuous Hacking Machine Plan
and see the results of automated security tests
performed to assess your product,
along with many of the functions described above.
