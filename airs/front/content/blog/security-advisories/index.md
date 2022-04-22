---
slug: security-advisories/
title: A Vulnerability Has Been Found!
date: 2022-04-18
subtitle: What you should know about our security advisories
category: philosophy
tags: cybersecurity, red-team, vulnerability, risk, software, hacking
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1650288075/blog/security-advisories/cover_advisories.webp
alt: Photo by Bank Phrom on Unsplash
description: In this blog post we explain what our Advisories are and, in the process, share some information on how the Fluid Attacks Research Team works.
keywords: Advisory, Zero Day, Cve, Vulnerability, Research, Responsible Disclosure, Cve Numbering Authority, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/Tzm3Oyu_6sk
---

Tons of vulnerabilities are found daily
in all kinds of software.
You can know this just by looking at the frequency
with which the [CVE Program tweets](https://twitter.com/cvenew/).
This program identifies,
defines
and catalogs publicly disclosed cybersecurity vulnerabilities.
In fact,
you probably see "CVE-..." constantly in your news feed.

Behind the constant flux of common vulnerabilities and exposures,
there are the people constantly probing software,
gathering vulnerability exploitation evidence
and reporting it through the right channels.
The Fluid Attacks Research Team does this too,
and as we at `Fluid Attacks` are proudly a [CNA](https://www.cve.org/ResourcesSupport/AllResources/CNARules#section_1-1_cnas)
(CVE Numbering Authority),
the team gets to assign CVE IDs
to the zero-day vulnerabilities they discover.
After contacting the vendor of the affected software,
a team member creates an advisory draft
on our [dedicated webpage](../../advisories/).

In this blog post,
we would like to share some information
about our Advisories
that may shed some light on how the Fluid Attacks Research Team works.

## What is in Fluid Attacks' Advisories?

Our Advisories are official documents
that communicate information
about the vulnerabilities discovered by our research team,
such as their [CVSSv3 base score](https://www.first.org/cvss/),
type according to our own [extensive list](https://docs.fluidattacks.com/criteria/vulnerabilities/),
and CVE ID.

The team also assigns each vulnerability a code name.
Why this?
Well,
you can probably recognize a vulnerability more reliably by its nickname
than by its CVE ID.
Or do you wanna try to guess what CVE-2021-44228
and CVE-2022-22947
refer to?
(Find the nicknames each of these were given at the end of this post.
But we invite you to try and guess\!)

Code names are assigned by the team member
who discovered the vulnerability.
They are last names of musicians and artists,
much like names given randomly to our clients' organizations
on our [attack surface management platform](../../categories/asm/)
are city names.
That's the bit of trivia we've brought you today\!

The information about which versions of the product are affected
is readily available as well.
But whether the entry includes the description of the vulnerability,
a proof of concept
and a custom exploit,
depends on whether this information can be disclosed at the time,
following our [Disclosure Policy](../../advisories/policy/).

Our policy describes the process
of how we responsibly communicate third-party product vulnerabilities
found by our offensive team or our research team.
We update advisory drafts at each relevant event,
such as when the vendor replies to the initial contact
or releases patches,
or when,
either in coordinated vulnerability disclosure
or lack of vendor response,
we must release a proof of concept.

Of course,
our policy allows time for vendors to reply,
acknowledging the vulnerability
or agreeing to a coordinated disclosure along with a patch.
These actions should lead to a positive outcome,
which is improving software
before its vulnerabilities are exploited by threat actors.
If the vendor fails to act promptly,
our research team proceeds with the responsible disclosure process.
In any case,
the idea of releasing these advisories is
to reduce the risk for users through awareness.
Figure 1 works as an example of the images we post on social media
accompanying the invitation to read our Advisories.
We also promote them in our weekly newsletter.

<div class="imgblock">

![Example of an advisory](https://res.cloudinary.com/fluid-attacks/image/upload/v1650288133/blog/security-advisories/advisories-figure-1.webp)

<div class="title">

Figure 1. The image we shared on social media
promoting the advisory of [a vulnerability](../../advisories/spinetta/)
in Network Olympus v1.8.0.

</div>

</div>

Next, we would like to share how
the Fluid Attacks Research Team decides what software to investigate.

## Of what products does Fluid Attacks release Advisories?

Decidedly,
there are too many products to choose from
when deciding where to look for vulnerabilities.
Our research team browses projects on sources like [GitHub](https://github.com/search)
and [SourceForge](https://sourceforge.net/),
or even looks them up on Google.
They focus on open-source software (OSS)
and check especially whether it satisfies two criteria.
Namely,
that it has a security policy
and that no other CNA has already called dibs
on researching its vulnerabilities.

We already emphasized the importance of the first criterion
in our blog post about a [guideline for vulnerability disclosure](../iso-iec-29147/)
(ISO/IEC 29147).
In short,
vendors should specify the process
and the required content that should be provided
for vulnerability reporting.
Regarding the second criterion,
although [it's not mandated by the CVE Program](https://www.cve.org/ResourcesSupport/AllResources/CNARules#section_7-3_cna_scope),
`Fluid Attacks` defines its scope
as one that does not overlap with that of other CNAs
(to put if briefly),
thus avoiding discovering the same vulnerability
at the same time as another CNA
and having to negotiate who should assign the CVE ID.

There are some other attributes
that help the team prioritize
which OSS to research.
For instance,
they have noticed there's a big chance of finding vulnerabilities
in web applications and OSS with web components.
So those are promising targets.
They also expect to have a better chance of finding issues
in OSS in which vulnerabilities have previously been reported.
Lastly,
they also suspect OSS with few released versions
to more likely have vulnerabilities.
However,
their primary two criteria are the ones mentioned in the above paragraph.
Once the research team selects an OSS,
they install the last version on their machines
and start looking for vulnerabilities.

## Does Fluid Attacks divulge issues found in your system?

Our [One-Shot Hacking](../../services/one-shot-hacking/)
and Continuous Hacking [Squad Plan](../../plans/) services
employ highly certified ethical hackers
to find vulnerabilities in our clients' systems.
In their assessment,
our hackers may find zero-days in third-party software.
When this happens,
we notify the client first
and then ask for their permission to proceed
with our vulnerability disclosure process,
that is,
to send the report to the product vendor.

Of course,
when it comes to our clients' software,
reported vulnerabilities are covered by a Non-Disclosure Agreement.
Unless they give us explicit permission
to publicly disclose a vulnerability,
they and limited `Fluid Attacks` staff are the only ones who know about it.
But we do urge them constantly to remediate it!

At `Fluid Attacks`
we are committed to research.
[Here](../../advisories/) you can find a list of our Advisories.
Follow us on social media
and [subscribe](../../subscription/) to our newsletter
to get our latest updates
on zero-day vulnerabilities found by the Fluid Attacks Research Team.

> **Note:** The nicknames given to the vulnerabilities mentioned
> in this post's proposed activity are,
> respectively, [Log4Shell](../log4shell/)
> and Spring4Shell.
> How well did you do?
