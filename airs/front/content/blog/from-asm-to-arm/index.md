---
slug: from-asm-to-arm/
title: From ASM to ARM
date: 2022-11-16
subtitle: We adhere to the attack resistance management concept
category: philosophy
tags: cybersecurity, company, security-testing, hacking, trend
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1668649683/blog/from-asm-to-arm/cover_from_asm_to_arm.webp
alt: Photo by Alexander Nikitenko on Unsplash
description: This blog post explains the "attack surface management" and "attack resistance management" concepts and our transition from one to the other.
keywords: Attack Surface, Attack Surface Management, Asm, Attack Resistance Management, Arm, Vulnerability Management, Exposure Management, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/H6obC_biCSk
---

Attack Surface Manager was the name of Fluid Attacks' platform
only a while ago.
In recent years,
the "**attack surface management**" (ASM) concept has become popular
among cybersecurity providers.
However,
we recently realized that
what this concept usually encompasses is not *entirely* in line
with what we offer in the company.
It actually falls short.
What a variety of companies currently intend to provide in the market with ASM
is far from what we're aiming for.
Our contribution to cybersecurity is more profound.
That's why we decided to adhere to a newer concept:
"**attack resistance management**" (ARM).
ARM allows us to generate a more precise differentiation
and avoid misunderstandings.
It better embraces what we do and what we offer.
Hence we modified the name of our platform.
In this post,
we help you to have a clearer understanding of the ASM and ARM concepts
and our transition from one to the other.

## Attack surface management

**Attack surface** usually refers to all an organization's IT assets
that an attacker could identify,
have access to,
exploit and affect in some way.
Regardless of whether many of them are not seen as vulnerable,
they potentially are.
Therefore,
viewing the attack surface as absolutely every digital asset
in relation to the organization
is preferable.
Some of these assets are internal and some are external.
That is,
some are within the organization's facilities and network
(e.g., computers and other devices used by employees)
and others are public or internet-facing assets
(e.g., public apps and websites).

The **ASM** is a solution
mainly geared to scanning and monitoring all these assets
for their enumeration in favor of their security.
In some cases,
ASM may focus only on internal or external asset enumeration.
In Gartner's "Innovation Insight for Attack Surface Management" report,
these two processes seem to correspond
to "cyber asset attack surface management" (CAASM)
and "external attack surface management" (EASM),
respectively.
Although they refer to them as two of the three capabilities of ASM,
it's not the point of this post to get involved in their categorization.
The fact is that EASM is the most famous at present.
It seeks to respond to a growing need for security
in the face of greater exposure to risk
due to organizations' increased use of external surfaces.

Nowadays,
it's becoming noticeable that
many organizations are not achieving complete visibility
of their attack surface.
Their perimeter is often not very well defined.
Many of their assets are scattered in different locations
outside the boundaries of their protected network.
Many of them are often completely unknown to organizations.
Some assets are dormant,
outdated or simply neglected,
with no security controls,
monitoring or maintenance by the organizations.
(Sometimes,
for example,
they are mistakenly believed to be implicitly secure,
such as supply chains or cloud resources.)
Some may even have unknown purposes,
connections and owners.
For instance,
so-called "shadow IT" involves an organization's staff
acquiring and using assets
without first informing and receiving approval from administrators
or security officers.

Beyond enumeration,
ASM typically aims to report and quantify risks
associated with the identified assets,
apparently from the criminals' perspective.
(In fact,
this appears to be the third and final ASM capability in Gartner's report:
"digital risk protection services" (DRPS).)
Such risks may be due to misconfigurations,
vulnerabilities and exposed data,
among other things,
within the assets and their interactions.
After the risks are reported,
the ASM seeks to prioritize them for prompt mitigation
(including elimination and patching of assets)
by the teams in charge.
Prioritization is fundamental
for properly managing an organization's resources,
such as time, effort and money.

Everything seems peachy with ASM,
but is it enough for an organization's cybersecurity plan?
One of the problems with ASM is its limitation to scanning,
to the mere intervention of automated tools
that supposedly "impersonate" attackers.
We must recognize that
the attackers' reconnaissance practice is not necessarily restricted
to using automated tools.
Hence the need for human intervention with manual procedures.
Another difficulty with ASM is that,
in some cases,
it is limited to external or internal environments.
This leaves substantial recognition gaps or blind spots for the organization
requesting the service.
[As Oltsik states in CSO](https://www.csoonline.com/article/3648998/look-for-attack-surface-management-to-go-mainstream-in-2022.html),
"the emerging attack surface management category
focuses on internet-facing assets alone."

An organization requires end-to-end visibility into its attack surface
and discovering all assets and interactions in its IT ecosystem.
A deep ASM does not just look at the URL level
but also enumerates the internal surface.
An extensive ASM should list technologies such as ports,
servers, operating systems, mobile and IoT devices,
third-party components
(including open-source),
APIs, microservices, containers,
IaC, SaaS, cloud resources,
as well as data such as IP addresses,
credentials and exposed code,
interactions with partners and third parties
(including supply chain vendors)
and more.
Internal and external environments are dynamic and constantly changing,
i.e., growing,
complexifying and dispersing with the addition of services,
interactions, software, users and devices.
Therefore,
another problem with ASM is that
it often isn't a continuous process,
with permanent monitoring of changes in the attack surface over time.

Of course,
providers can solve the aforementioned problems
by optimizing ASM solutions.
However,
processes as relevant in cybersecurity
as "vulnerability management,"
for example,
with classification and prioritization of vulnerabilities
in specific targets of evaluation,
are sometimes left out of ASM packages.
In fact,
Gartner mentions vulnerability management as one of the three pillars
of so-called "exposure management,"
the other two being ASM and the "validation" component.
Without getting into their classifications,
what we can say is that ASM always needs to be complemented.
As a single approach to cybersecurity,
it can be insufficient.

Organizations should recognize that
their cybersecurity plans should not only focus on identifying their assets
and the risks they may theoretically entail
but also on the practice of simulated attacks
and evaluation of their impacts.
With ASM,
it's possible to get an idea
of how the evaluated organization looks to attackers,
what attack paths they might employ
and what some of the potential risks are.
With the inclusion of vulnerability management
it's possible to answer questions
such as what are those security vulnerabilities
present on the organization's attack surface,
what are those assets with vulnerabilities
most likely to be exploited by threat actors,
and how can the organization achieve their remediation?
But what about what would happen if a malicious hacker were to launch an attack
against the organization?
How would it respond,
what would be the impact,
and would it be able to withstand it?

## Attack resistance management

The **ARM** then enters the picture.
In addition to seeking to enumerate resources,
improve an organization's knowledge about its attack surface,
qualify its risks
and even help remediate security issues detected on it,
this solution is clear in claiming that
it helps increase an organization's resistance to cyberattacks.
ARM seeks to answer the questions:
how do and how should an organization's attack prevention,
detection and response controls work?
With this solution,
an organization can manage and monitor not only the attack surface,
its vulnerabilities and risk exposure
but also its security testing.

<cta-banner
  buttontxt="Read more"
  link="/solutions/security-testing/"
  title="Get started with Fluid Attacks' Security Testing solution right now"
/>

Basically,
this new concept covers an ASM that,
as we said,
must be comprehensive and constant
to keep track of all assets and changes in an organization's local
and external environments.
To this ASM,
the ARM adds **continuous security testing**,
preferably from the beginning of the SDLC,
which also keeps abreast of updates
in the organization under assessment.
In other words,
assets detected means assets added to the scope of the tests.
These security tests in ARM go beyond the use of automated tools,
involving the work of highly certified and experienced ethical hackers.
These hackers aim to test all possible attack vectors,
adapting to each organization's specific contexts and business logic.

Thus,
in ARM,
there is an undeniable way to see
how a threat actor perceives the entire attack surface of an organization
and can act on it.
Following the tactics,
techniques and procedures employed by criminals,
ethical hackers recognize assets
(both known and unknown to the organization under assessment),
identify vulnerabilities in them,
and plan and carry out attacks that make it possible
to measure the risk exposure accurately.
Let us recall for the umpteenth time that
automated tools,
although faster and cheaper,
focus only on detecting common and well-known vulnerabilities.
To find those security issues outside the tools' databases,
i.e., those unknown to them,
often more complex and of greater severity,
and,
of course,
to exploit them,
come the ethical hackers.

On balance,
helping your organization know its entire attack surface,
identifying its security weaknesses,
and testing its response and resistance to real attacks
to encourage then risk mitigation
is what we at Fluid Attacks are all about.
Reaffirming this,
we consequently decided to modify from ASM to ARM
the name of our platform,
that paramount face of Fluid Attacks
we present to the eyes of the world.

## Fluid Attacks' ARM platform

At Fluid Attacks,
we offer you comprehensive [Continuous Hacking](../../services/continuous-hacking/)
with our automated tools and ethical hackers
that generate reports in a single place:
our [Attack Resistance Management platform](https://app.fluidattacks.com/).
In this platform,
you have not only a constant record
of your organization's identified and evaluated attack surface
but also of the vulnerabilities detected in it over time
and of your organization's exposure to risk.
There you receive extensive details on our findings
that make it easier for you to prioritize vulnerabilities for remediation.
From the attack resistance posture,
we provide you with evidence of the exploitation
and impact of our simulated and controlled attacks.
We also offer recommendations to your team of developers
to consider for remediation,
hopefully also serving as feedback
for their future development practices.
Indeed,
on our ARM platform,
you can assign specific remediation processes to each individual.
In an unlimited way,
you can ask our hackers to verify
the effectiveness of remediation through reattacks.
And,
if necessary,
you can ask them for consulting or advice.
You can also use our DevSecOps agent
to validate compliance with your organization's policies
before deploying software to production.
You can keep track of your progress in terms of remediation
and mitigation of risk exposure in your products
and also ensure compliance with security requirements
based on international standards.

If you are interested in trying our ARM platform for free,
we offer you our [21-day free trial](https://app.fluidattacks.com/SignUp)
in which you can enjoy continuous security testing
with our automated tools
(Machine Plan).
If,
instead,
you want to immediately enjoy comprehensive Continuous Hacking
with the intervention of our tools and our red team of ethical hackers
(Squad Plan),
please [get in touch with us](../../contact-us/).
