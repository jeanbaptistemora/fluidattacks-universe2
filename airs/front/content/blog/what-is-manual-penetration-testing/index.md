---
slug: what-is-manual-penetration-testing/
title: What Is Manual Penetration Testing?
date: 2022-10-20
subtitle: How it works and how it differs from the "automated"
category: philosophy
tags: pentesting, cybersecurity, security-testing, hacking, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1666278975/blog/what-is-manual-penetration-testing/cover_manual_pentesting.webp
alt: Photo by ian dooley on Unsplash
description: This blog post explains what manual penetration testing is, how it works to discover vulnerabilities, and its difference from so-called "automated pentesting."
keywords: Manual Penetration Testing, Automated Penetration Testing, Black Box, White Box, Gray Box, Vulnerability Scanning, Pentester, Pentesting, Ethical Hacking
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/iD5aVJFCXJg
---

[Penetration testing](../../solutions/penetration-testing/) or pentesting
is a type of [security testing](../../solutions/security-testing/)
in which one or more ethical hackers attack an information system
with the authorization of its owner
to identify and report security vulnerabilities.
What? Yes, we know.
You've probably heard that this is something
that can also be performed and achieved by specific automated tools.
People usually talk about "manual penetration testing"
and "automated penetration testing."
However,
some of us consider and affirm that
what happens in the latter
doesn't comply with what *pentesting* really is
and that this name was just a fruit of a marketing strategy.
Manual pentesting,
as we'll see,
is the only pentesting.

## Manual vs. automated penetration testing?

**Manual penetration testing (MPT)** is pentesting
carried out by offensive security experts
called pentesters or ethical hackers.
In their work,
they must use proprietary or public tools as support,
some of which can be automated tools.
On the other hand,
**automated penetration testing (APT)** is supposedly pentesting
performed by automated tools.
A person with basic knowledge of cybersecurity,
let's say from a regular IT staff,
could run such tools without any problem.

The pentesters in **MPT** simulate real-world attacks,
employing various tactics,
techniques and procedures
that malicious hackers might also use.
The pentesters show creativity in their ways of attacking.
They can make unexpected turns during the tests,
depending on their objectives and results.
**APT** tools,
in contrast,
follow a standard,
delimited pattern.
They are restricted to delivering reports with predetermined,
known vulnerabilities,
many of them mere low-hanging fruits.
They cannot do what the pentesters can,
that is,
identify zero-day vulnerabilities
(i.e., previously unknown security issues).

In **MPT**,
the pentesters seek to understand
the structure and functionality of the target of evaluation (ToE).
From there,
they are able to identify types of vulnerabilities
that are not or hardly detected in **APT**.
For example,
the detection and verification of some issues with data handling,
such as Cross-site Scripting (XSS) and SQL Injection,
as well as business logic flaws and access control vulnerabilities,
depend more on **MPT**.
**APT** focuses more on,
for instance,
faulty permission rules,
missing updates and misconfigurations.
ToE responses to certain inputs may appear valid to automated tools
when, in fact, they are anomalies
in the eyes of the pentesters.
Because of its depth and analysis,
the MPT can report the most complex and critical vulnerabilities,
which,
by the way,
the pentesters can exploit to assess their impact.
Something the tools do not accomplish.

Since it involves humans in deep immersion,
**MPT** usually takes longer and is more expensive.
Rented or purchased **APT** tools perform their tests much faster
but superficially.
Another problem for the latter is that
they often report false positives.
Part of the time gained in their evaluations is lost
with the need to verify false positives.
Developers end up spending hours dealing with lies.
Because it is cheaper,
**APT** is often applied more regularly than MPT.
However,
as in PTaaS ([penetration testing as a service](../what-is-ptaas/)),
**MPT** can also be implemented for continuous assessments.

The reports of some **APT** tools may not be very detailed
or provide solution recommendations.
This is different from what pentesters can achieve.
In addition,
by evaluating more attack surfaces through various methods,
the pentesters allow development teams to have results in hand
to deal with a broader range of cyberattacks.
It should be noted that
the effectiveness of **MPT**
depends on the capabilities of each ethical hacker hired
and may vary from time to time.
In **APT**,
on the other hand,
the effectiveness is always predetermined.

Merging both presented methodologies
allows us to obtain benefits from each of them.
Automated tools' fast and superficial work enables pentesters
to invest time in complex assessments.
In fact,
this is how proper pentesting is usually done.
The tools contribute in one of its phases
to what we could say they actually do:
**vulnerability scanning**.
There is no automated penetration testing.
That doesn't exist so far.
It is the expert humans who do the pentesting,
within which,
in one of the phases we'll see later,
they can call on the assistance of automated tools.

## Black, white and gray box pentesting

Manual penetration testing,
i.e., pentesting itself,
can be classified according to the information
initially available to the pentesters:

### Black box pentesting

As can happen for a threat actor,
in this type of pentesting,
the pentesters only know the name and location of the target.
They have no details about it.
That is,
the structure,
source code and internal workings of the system to be attacked
are unknown to them.
This is why the pentesters are forced to gather much information
and resort to methods such as brute force
to access the ToE.
This test can take longer than the others,
where the system's owners give information to the ethical hackers
from the beginning.
In black box pentesting,
the pentesters don't evaluate code
unless they gain access to it for some reason.
What they do is focus on the external attributes
and behavior of the ToE.
This evaluation mode,
also called "trial and error,"
can lead to identifying fewer vulnerabilities
compared to the other modes.

### White box pentesting

In this mode,
also called clear-box or glass-box testing,
the pentesters have extensive knowledge of the ToE,
as well as access to its source code and other resources
that its developers can access.
Code review involves the use of tools
not employed in black box pentesting.
It can then be a more complete and exhaustive assessment
for the possible identification
of a more significant number of existing vulnerabilities.
Indeed,
although,
in this case,
the pentesters perform structural testing
(perhaps giving it a higher priority),
they can also perform functional or business testing,
as in black box mode.

### Gray box pentesting

In this case,
the two previous modes are mixed.
Here the pentesters receive partial information about the ToE.
For example,
they only have access to relevant internal elements
for the scheduled tests,
such as documentation and architecture,
but not to the source code.
In gray box pentesting,
the evaluation focuses on both the functionality
and structure of the target
but without being a method of intruding into the code.

<cta-banner
  buttontxt="Read more"
  link="/solutions/penetration-testing/"
  title="Get started with Fluid Attacks' Penetration Testing solution
  right now"
/>

## How to do penetration testing

There is no universal standard for this activity,
which,
in fact,
involves a great deal of creativity and adaptation
to the characteristics of the ToE
by the pentesters.
However,
some general steps or phases are usually followed,
which are presented below:

### Planning phase

The scope is determined,
considering security policies and standards.
The pentesters begin to define strategies
based on their knowledge and experience.

### Data collection or reconnaissance phase

The pentesters begin to collect information about the ToE.
This will depend on the mode of testing.
Although it is true that in a white box pentesting
the pentesters have a large amount of information,
further nurturing these resources allows for making it clear
what a malicious hacker could access in the ToE.
There are many useful free tools for collecting data on,
for instance,
software versions and databases,
hardware types and third-party components used in the ToE.
(Some can be found thanks to the [OSINT framework](https://osintframework.com/).)
In their attempt to access the system,
the pentesters may also look for ways
to obtain data such as usernames and passwords.

Reconnaissance is usually initially passive and then active.
In the former,
the pentesters gather information about the ToE
without direct contact with it.
In this process,
there is no way to activate some intrusion detection system
or to leave any traces.
Google searching,
social media scanning,
and sites such as [netcraft.com](https://www.netcraft.com/)
and [archive.org](https://archive.org/)
come into play.
In active reconnaissance,
instead,
there is interaction with the ToE.
The collection of information is more intrusive,
so there is the possibility of the pentesters being detected.
The idea is to identify the technology used by the ToE
and possible entry and attack vectors.
Here,
for example,
a port scan is usually carried out
to determine which ports are open
and which services and operating systems they are related to.
One of the most recognized port scanners is [nmap](https://nmap.org/).

In connection with the above,
there is also a process called enumeration.
Here,
the attack surface is reviewed in detail.
The pentesters seek to determine what is in the ToE.
Depending on the target,
it is then possible to know,
for instance,
servers and devices involved,
as well as users,
folders and files.
Some enumeration tools are [Cain and Abel](https://sectools.org/tool/cain/)
(as we saw some time ago, it is also used for password cracking),
[Angry IP Scanner](https://angryip.org/) and [SuperScan](https://sectools.org/tool/superscan/).
Apart from port scanners and enumeration tools,
the pentesters can also use packet sniffers,
which are used to intercept and log network traffic.

### Vulnerability assessment phase

The pentesters identify possible security weaknesses
that can be used to gain access to the system
and cause an impact.
This is where so-called "automated penetration testing,"
i.e., vulnerability scanning,
can spring into action.
Tools can be helpful to speed up the process
by detecting some known vulnerabilities.
However,
we already know that identifying the riskiest security issues
depends on the manual work of the pentesters.
In this phase,
the experts can monitor current trends
to clarify which threats are problematic for the specific ToE.
In addition,
they determine the impact of the identified vulnerabilities,
considering factors such as the attack scenario,
difficulty of exploitation,
effect on the integrity,
confidentiality and availability of the system,
and influence on nearby systems.

### Exploitation phase

Here,
we talk explicitly about launching attacks against the ToE
and assessing the real impact.
The pentesters develop or obtain exploits
(pieces of software)
to take advantage of the identified vulnerabilities.
They can move through the ToE
and achieve specific objectives
that demonstrate what a malicious hacker could accomplish
(e.g., data theft and disruption of operations).
In this phase,
providers such as `Fluid Attacks` can operate in a "safe mode"
to not affect service availability or business functionalities
within the organization that owns the ToE.

### Report phase

Once ToE security issues are identified and exploited,
they are reported.
The pentesters must deliver detailed findings
after proper interpretation and analysis.
The report includes evaluated locations and scope,
detection methodologies,
vulnerabilities identified,
vulnerability exploitation methodologies and attempts
(the pentesters' work must be reproducible)
and remediation recommendations.
Thanks to the latter,
the owner,
who should be left with a clear report of his risk exposure,
can take corrective measures
to improve the security of their assessed system.

## Fluid Attacks' Pentesting solution

At `Fluid Attacks`,
penetration testing is performed by groups of experienced
and highly certified pentesters or ethical hackers.
Our red team has individuals with diverse skills
who assume different roles within the tests.
So,
for example,
what may escape one group
may possibly be discovered by another from a different perspective.
We make use of our own automated tools
for [SAST](../../categories/sast/), [DAST](../../categories/dast/)
and [SCA-type](../../categories/sca/) tests.
However,
as happened last year
and we highlighted in our last [State of Attacks](https://fluidattacks.docsend.com/view/d7wbu584digrbe9a)
report,
the detection of critical severity vulnerabilities
may depend *entirely* on the manual work of our hackers.

In our pentesting solution,
we test,
from a threat actor perspective,
the security of your web and mobile apps,
cloud infrastructure,
networks, and IoT devices,
among many other information systems.
In our [Attack Resistance Management platform](https://app.fluidattacks.com/)
(ARM),
you receive continuous reports of our findings
with minimal false positive and false negative rates.
There you get detailed outcomes,
including evidence.
You can assign vulnerabilities for remediation to your staff,
request as many reattacks as necessary,
and also have the support of our hackers.

[Pentesting](../../solutions/penetration-testing/) is a thorough assessment
by experts
that vulnerability scanning cannot replace.
(If you want to take the first step in security
by trying a scan with our automated tools,
request our [21-day free trial](../../free-trial/)).
It is striking how many believe that both are the same thing.
But there are indeed scammers in the market,
and they can tell you that they do penetration testing when,
in fact,
they apply vulnerability scanning.
Don't be misled.
If you want more details
on what to base your choice of the right pentesting provider
for your organization,
read our blog post "[Choosing the Right Pentesting Team](../choosing-pentesting-team/)."
If you are interested in learning about the PTaaS model
(which involves continuous penetration testing)
and its benefits for your company,
we invite you to read "[Penetration Testing as a Service](../what-is-ptaas/)."
Any doubt?
Don't hesitate to [contact us](../../contact-us/).
