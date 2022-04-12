---
slug: what-is-ethical-hacking/
title: What Do Those in White Hats Do?
date: 2022-04-11
subtitle: A very brief introduction to ethical hacking
category: philosophy
tags: cybersecurity, ethical-hacking, pentesting, red-team, security-testing, vulnerability
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1649710011/blog/what-is-ethical-hacking/cover_ethical_hacking.webp
alt: Photo by Bruno Kelzer on Unsplash
description: Our blog needed a basic post about ethical hacking. It can be helpful as an introduction for those who don't know and want to learn about it.
keywords: Ethical Hacking, Red Team, White Hat, Black Hat, Hacker, Vulnerability, Cyberattack, Introduction, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/J1sd2zy87rc
---

As you may know,
`Fluid Attacks` is a company
that specializes in [ethical hacking](../../solutions/ethical-hacking/).
We are a big [red team](../../solutions/red-teaming/),
an offensive security team
with the mission to detect security vulnerabilities in [IT systems](../../systems/).
As we recently realized that
we didn't have an informative, introductory blog post
about what ethical hacking is,
we decided to create it.
This text is aimed mainly at those who're new to the subject
and want to get an introduction.
It is based on a recent workshop given by our Red Team Leader,
[Andres Roldan](../../about-us/people/aroldan/),
to a group of journalists.

As Andres did,
let's start by answering a couple of basic questions:

### What is cybersecurity?

[It is said that](https://datareportal.com/global-digital-overview)
almost five billion people currently use the Internet,
which corresponds to nearly 63% of the world's population.
Moreover,
around 92% of these users,
at some point,
virtually from anywhere,
have access to the network through mobile devices.
We are undoubtedly in a highly interconnected digital world
where,
as in the "tangible" reality,
menaces exist [from the outset](../first-cyberattack/).
In the face of constant threats,
**cybersecurity** became necessary.
[Gartner](https://www.gartner.com/en/information-technology/glossary/cybersecurity),
partially right,
defines this term
as "the combination of people,
policies, processes and technologies
employed by an enterprise
to protect its cyber assets."
(I said "partially"
because it is also true that as an individual user,
you can access cybersecurity).
But what should cyber assets be protected against?
—Cyberattacks.

### What are cyberattacks?

[These are assaults](https://www.checkpoint.com/cyber-hub/cyber-security/what-is-cyber-attack/)
carried out by **cybercriminals**
who attack one or more IT systems
from one or more computers.
Cyberattacks can disable victim systems,
steal their data
or use them as launching points for other assaults.
According to an [IBM security report](https://www.ibm.com/security/data-breach/threat-intelligence/),
the top cyberattack types (tactics) last year
included the following:
[ransomware](../ransomware/),
unauthorized server access,
[business email compromise](../cost-cybercrime-ii/),
data theft and credential harvesting.
And among the most frequently used techniques
to achieve these objectives
were the following:
[phishing](../phishing/),
vulnerability exploitation,
stolen credentials,
[brute force](../pass-cracking/) and remote desktop.

Many cybercriminals
who execute the assaults are so-called malicious hackers,
threat actors or black hat hackers.
Among their primary motivations is the idea of obtaining some financial reward.
They may also attack just to express their disagreement
with the decisions of governments or companies.
There are also attacks resulting from the mere desire of hackers to take risks
and achieve recognition in certain groups of people.
Sometimes,
cybercriminals are even hired by dishonest firms to spoil projects
and affect the reputation of their rivals.
Something similar happens among governments
(e.g., [the Russia-Ukraine cyberwar](../timeline-new-cyberwar/)).
(If you want to know more about how hackers think,
[visit this blog post](../thinking-like-hacker/).)
Regardless,
in a universe where we can experience lots of counter-stimuli,
it is to be expected that
there are **white hats** if there are black hats.
Namely,
if there is malicious hacking,
there is also **ethical hacking**.

## What is ethical hacking?

Ethical hacking is perhaps the best way to respond to malicious hacking.
In ethical hacking,
cyberattacks are conducted by white hat hackers
in favor of organizations' cybersecurity.
Systems are attacked to find out their vulnerabilities
by copying threat actors' tactics,
techniques and procedures.
The big difference is that
the attack is carried out with the system owner's consent,
who will be responsible for remediating the reported security vulnerabilities.

In ethical hacking,
experts must keep up to date
on the existence and use of hacking tools,
as well as on the attack trends used by adversaries.
In their reports,
ethical hackers provide information about identified vulnerabilities,
including how critical they are.
They do this by following public frameworks
such as [CVE](../../compliance/cve/)
and [CVSS](https://www.first.org/cvss/).
They also provide evidence of exploitation of vulnerabilities
and which information assets can be compromised in an attack.
Beyond finding known vulnerabilities,
ethical hackers can also conduct research
to discover and record zero-day vulnerabilities,
i.e., previously unknown threats.

### How does ethical hacking work?

For ethical hacking to happen,
the systems' owner must previously define and approve an attack surface
and a target of evaluation
(i.e., part or all of the attack surface).
The targets can be [web](../../systems/web-apps/)
or [mobile apps](../../systems/mobile-apps/),
[APIs and microservices](../../systems/apis/),
[thick clients](../../systems/thick-clients/),
[cloud infrastructure](../../systems/cloud-infrastructure/),
[networks and hosts](../../systems/networks-and-hosts/),
[IoT devices](../../systems/iot/)
and [operational technology](../../systems/ot/).
The commonly used ethical hacking methodology
can be divided into reconnaissance,
enumeration, analysis, exploitation and reporting phases.

1. **Passive reconnaissance phase:**
   In this first phase,
   the ethical hackers collect information from external sources
   without interacting directly with the target.
   They employ,
   for example,
   [Open Source Intelligence](../social-engineering/)
   (i.e., publicly available information)
   collection techniques.
   They can resort to common web search engines
   such as Google and Bing
   to discover relevant details about the target.
   Due to the characteristics of this phase,
   there is little chance of the hackers being detected.

2. **Active reconnaissance phase:**
   In this phase,
   the ethical hackers already have direct contact with the target.
   They identify sources of information
   and technology belonging to the organization
   that owns the system under evaluation.
   They interact with the organization's services,
   systems and even personnel
   to collect data and define attack vectors.
   The chances of hackers being discovered increase considerably
   if we compare this phase with the previous one.

3. **Enumeration phase:**
   In this phase,
   ethical hackers set out to sketch the target's security state
   and prepare for the attack.
   They identify its strengths and weaknesses
   and begin envisioning the possible impacts
   that may result from the assault.
   According to the particular characteristics of the target,
   hackers prepare a special arsenal for it.

4. **Analysis phase:**
   In this phase,
   ethical hackers are responsible
   for determining the exact impact
   of attacking each of the vulnerabilities they have identified.
   They evaluate each scenario and attack vector,
   as well as the difficulties of exploitation.
   They take into account the damage on the integrity,
   confidentiality and availability of the target in each case.
   In addition,
   the hackers examine the potential impact
   on systems close to the target.

5. **Exploitation phase:**
   According to Roldan,
   it's this phase
   where ethical hacking differs
   from the operation of automated security testing tools.
   The tool is limited to identifying vulnerabilities,
   while ethical hackers exploit them
   to reach high-value objectives
   within their target of evaluation.
   In this way,
   they can identify the real effects
   that a cybercriminal could achieve
   by exploiting these vulnerabilities.

6. **Reporting phase:**
   After the exploitation is completed,
   ethical hackers have to present the findings to all stakeholders.
   One of the hackers' deliverables is an executive summary,
   thanks to which the managers of the organization
   that owns the target
   can easily understand the identified risks.
   From this report,
   they can manage processes for risk mitigation.
   Another deliverable is a technical summary
   so that developers
   or other professionals
   can understand each vulnerability in detail
   and proceed with remediation.

### For whom is ethical hacking recommended?

Financial institutions are the ones that hire this service the most,
mainly due to regulations that require it.
However,
it's recommended that any organization with a presence on the Internet
or developing digital products
test the security of their systems with ethical hacking
to prevent suffering from cyberattacks.

Follow [this link](../../solutions/ethical-hacking/)
if you and your company are interested in knowing details
about `Fluid Attacks'` Ethical Hacking solution.
But if what you'd like is to wear a white hat
and be an ethical hacker on our red team,
follow [this one](../../careers/).
For more details on each case,
don't hesitate to [contact us](../../contact-us/).
