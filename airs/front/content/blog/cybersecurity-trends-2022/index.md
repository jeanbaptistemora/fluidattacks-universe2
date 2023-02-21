---
slug: cybersecurity-trends-2022/
title: Cybersecurity Trends 2022
date: 2022-10-27
subtitle: Trends in cyberattacks and prevention this year
category: opinions
tags: cybersecurity, trend, cloud, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1666899374/blog/cybersecurity-trends-2022/cover_cybersecurity-trends-2022.webp
alt: Photo by jean wimmerlin on Unsplash
description: In this post, Fluid Attacks shares a digest of trends in cyberattacks and prevention in 2022.
keywords: Cyberattacks, Trends, Prevention, Vulnerable Software Components, Supply Chain Attacks, Cloud Services, Cyberwar, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/DD13yRz0RwE
---

We are just a couple of months
away from the start of a new year.
So,
it's the right time to look at the trends
that marked 2022
in regard to cyberattacks and preventive measures.

## Cyberattack trends in 2022

<br />

### Cyberwar and state-sponsored attacks

This year we reported on the cyberattacks
that accompanied the first moments
of the ongoing Russian invasion of Ukraine
([here](../cyberwar-ukraine/)
and [here](../timeline-new-cyberwar/)).
Not that there had been no bad blood between these two nations before,
as they conducted cyberattacks against each other in the years past.
Rather,
the widespread interest in the conflict,
likely due to its escalation to a war,
brought the attention of the media
to the state-sponsored cyberattacks this year.

The earliest attacks included defacement of government websites
and the use of WhisperGate, HermeticWiper and IsaacWiper malware.
Following the invasion,
some gangs started announcing which side they were on,
and the attacks included even some in favor of Ukraine
and some that targeted the U.S.
Due to the latter,
the CISA and the White House [issued](../protection-recommendation-us/)
recommendations.
In the case of software companies,
these included embedding security in development
since the beginning
(see [DevSecOps](../devsecops-concept/)).

In the following months Conti,
a ransomware gang that sided with Russia in the conflict,
conducted a wave of [cyberattacks against Costa Rica](../conti-gang-attacked-costa-rica/).
This gang stole information from government organizations in that country
and threatened to disclose it.
Their attacks persisted,
representing [millions of dollars in losses](https://restofworld.org/2022/cyberattack-costa-rica-citizens-hurting/),
and apparently even spread to Peru.
Even though Conti is presumed gone since May,
it is believed that its members are now part of ransomware campaigns
such as BlackByte and BlackCat.
The latter,
as [reported by the FBI](https://www.ic3.gov/Media/News/2022/220420.pdf)
in April,
"had compromised at least 60 entities worldwide"
during the span of one month.

The above events have organizations around the world
keeping a wary eye on cyberattacks
coming from state-sponsored groups.
Precautions need to be taken
as the [average cost of a data breach worldwide](https://www.ibm.com/security/data-breach)
has reached a record high of $4.35M,
a 2.6% increase over last year's.

### Exploitation of vulnerabilities in software components

Last year ended with the hot mess that is [Log4Shell](../log4shell/),
and that mess hasn't been cleaned up yet.
The vulnerability affects Log4j, a highly popular logging tool
that is used in (potentially) millions of applications.
Patches have been issued for that and further vulnerabilities in the library,
but folks still fail to do the updating.
Meanwhile,
threat actors have been exploiting it throughout the year.

Use of software dependencies with known vulnerabilities
is a widespread issue.
Our [2022 State of Attacks](https://try.fluidattacks.tech/state-of-attacks-2022/)
report shows
that almost **75%** of the systems we assessed this year
used vulnerable software components.
Notably,
this is the type of vulnerability
that generated the most exposure to risk when aggregated.
(Our analyses included systems
where our software composition analysis ([SCA](../../product/sca/))
detected Log4Shell,
among others.
Recently,
our SCA was enabled to detect the critical flaw [Text4Shell](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42889).)

Vulnerable dependencies that go unchecked
create the risk of suffering supply chain attacks.
According to [research by the Ponemon institute](https://www.ibm.com/security/data-breach),
in 2022 the cost of such a compromise is $4.46M on average globally
(surpassing that of data breaches
attributed to attacks of all categories).

### Exploitation and misconfiguration abuse in the cloud

Even though mainframe architecture is very much present,
the adoption of the cloud is ever growing
and is indeed a much more realistic option
for emerging businesses around the world.
You've heard about the positive side before:
Moving to the cloud provides scalability for good prices.
And again,
you've heard about the risks:
sensitive data loss,
compromised accounts,
servers shut down, etc.
But these [can be tackled](../why-is-cloud-devsecops-important/).
So what are teams doing wrong?

The main theme of successful attacks in the cloud this year
was **exploitation of vulnerabilities**.
Again:
We saw in our [annual report](https://try.fluidattacks.tech/state-of-attacks-2022/)
that using vulnerable software components was the biggest issue
exposing systems to compromise.
It's got repercussions worldwide:
IBM X-Force [says](https://securityintelligence.com/posts/new-report-finds-businesses-introducing-security-risk-cloud-environments/)
26% of cloud incidents
from July last year to 12 months later
shared this initial entry point.
One of the most exploited vulnerabilities this year was,
of course,
Log4Shell.

Another attack trend was **misconfiguration abuse**.
We've been vocal
about how our hackers recurrently find problems
with misconfigured cloud services.
In our annual report,
we show that it was among the top five problems
that exposed infrastructure the most to risk.
A related problem that also made it to that top
is the absence of authentication mechanisms
or having one that can be bypassed.
Additionally to this,
IBM X-Force found overly privileged user accounts
in 99% of their penetration tests.

## Cyberattack prevention trends in 2022

<br />

### Implementing DevSecOps

As we mentioned above,
the Biden Administration recommended technology and software firms
integrate security from the beginning of product development.
This is one of the main themes
of [implementing the DevSecOps culture](../how-to-implement-devsecops/).
Compared to last year,
[we saw](https://try.fluidattacks.tech/state-of-attacks-2022/)
a **32.5% increase** in systems using our
[Continuous Hacking solution](../../services/continuous-hacking/).
These systems' owners are constantly receiving security testing findings
from the early stages of the software development lifecycle (SDLC).
What's more,
some enable a feature in their CI/CD
to avoid deploying software into production when there are open vulnerabilities
(what's known as "breaking the build").
This year,
we found
that customers who break the build take about **30% less time** on average
to remediate vulnerabilities in their software.
We also saw
that deploying manual penetration tests
in combination with automated tests
allows teams to find critical severity vulnerabilities in their software,
since they were **all** shown to be found only by our ethical hackers.

In line with this rising trend,
we have been enriching our [DevSecOps blog series](../tags/devsecops/).
Be sure to check it out.

<cta-banner
  buttontxt="Read more"
  link="/solutions/devsecops/"
  title="Get started with Fluid Attacks' DevSecOps solution right now"
/>

### Identifying risk in software components

Due to the heightened chances
of threat actors exploiting a single vulnerability
(e.g., Log4Shell, Text4Shell)
disrupting the software supply chain,
there's an urgent call for developers
to understand the risks
each given third-party dependency can introduce to a project.

In May,
NIST released [key practices](../nist-supply-chain-risk/)
for building,
sustaining
and enhancing cybersecurity supply chain risk management capabilities.
Notably,
the institute advised firms
to map such risk to the overall enterprise risk management,
making it an essential point in the boardroom agenda.

Just this month,
[Google launched](https://security.googleblog.com/2022/10/announcing-guac-great-pairing-with-slsa.html)
an initiative
to make knowledge about the details of software available to everyone.
This initiative is called GUAC
(which does not refer to the delicious avocado-based dip,
but rather stands for Graph for Understanding Artifact Composition).
By adding up software security metadata from public and private sources,
it aims to create a graph
that can answer queries about supply chain risk associated with each software,
as it shows relationships between projects,
resources, artifacts, repositories, etc.

And this year we gave a demonstration
at Black Hat 2022 Arsenal
of our open-source tool called [Makes](https://github.com/fluidattacks/makes).
It is used for building CI/CD pipelines and application environments,
with the particularity
that it cryptographically signs direct and indirect dependencies.
This allows teams
to defend their application from supply chain attacks.
Regardless,
it's a good practice
to perform
[software composition analysis (SCA) scans](../sca-scans/) continuously.

### Secure authentication measures

Tackling the issue of compromised credentials is key
to prevent threat actors from entering and exfiltrating data
or even further exploiting any misconfiguration of cloud services.
Multi-factor authentication (MFA) is still going strong
to counter brute-force attacks and other kinds.
Entrusting authentication to a single password factor is just too risky.
This month,
[it's been reported](https://www.tomshardware.com/news/rtx-4090-password-cracking-comparison)
that hackers using eight Nvidia RTX 4090 graphics cards
can crack an eight-digit password (the most popular length)
in 48 minutes.
All it takes is taking leaked passwords as encoded hashes,
reverse-engineering them to view them as plain text,
and they're good to use in targeted attacks.

Apart from having MFA,
it's important that software itself is safe.
Regarding authentication,
it's time that software solution developers start
requesting a combination of automated and manual
static application security testing ([SAST](../../product/sast/))
to see if credentials are exposed in code,
as this was another prominent, high-risk flaw
that [we found](https://try.fluidattacks.tech/state-of-attacks-2022/)
in systems this year.

### Risk-data-driven decision-making

In a final note,
we'd like to share
that the cybersecurity community is pushing for a shift
in how we understand risk in a system.
In a few words,
instead of counting vulnerabilities,
teams are encouraged
to determine the risk they each represent.
At `Fluid Attacks`,
we have come up with a solution
that takes the CVSS base score as a basis
and further augments it significantly and exponentially
as the base score increases,
attempting to depict more accurately what our hackers see in practice.
This gives us a risk exposure measure we call [CVSSF](https://try.fluidattacks.tech/report/cvssf/).
As a result,
visibility becomes greater the riskier vulnerabilities get.
Our clients get the CVSSF of each detected vulnerability
on our [Attack Resistance Management platform](../../platform/) (ARM)
and make better decisions to prioritize remediation,
not thinking about numbers, but risk.

## Secure against cyberattack trends with Fluid Attacks

Want some help implementing the above preventive security measures?
We offer a [21-day free trial](../../free-trial/)
of our Continuous Hacking Machine Plan,
which can help you find vulnerable software dependencies
and proprietary code,
improper configuration of cloud services,
and more.
[Contact us](../../contact-us-demo/) if you have any questions!
