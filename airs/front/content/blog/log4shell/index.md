---
slug: log4shell/
title: Log4Shell Is the Biggest Threat Yet
date: 2021-12-23
subtitle: Patch these Log4j vulnerabilities or perish!
category: attacks
tags: cybersecurity, software, vulnerability, company, exploit, hacking
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1640267729/blog/log4shell/cover_log4shell.webp
alt: Photo by tabitha turner on Unsplash
description: A vulnerability in the ubiquitous open-source library Log4j
  has revealed terrifying exploit possibilities.
  Learn what it is and what you should do about it.
keywords: Log4j, Log4shell, Upgrade, Apache, Remote Code Execution, Java,
  Vulnerability, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/hNkp2QhTWfA
---

The world is quaking
since the disclosure of a zero-day vulnerability
found in Apache's open-source library [Log4j](https://logging.apache.org/log4j/2.x/manual/index.html).

There are at least two reasons why this finding is a big deal.
One is that Log4j is a logging tool used in [potentially](https://www.csoonline.com/article/3644472/apache-log4j-vulnerability-actively-exploited-impacting-millions-of-java-based-apps.html)
millions of Java-based applications.
People normally use open-source libraries as software components because
pre-written code is handier and faster than writing everything from scratch.
Seeing as [logging](https://www.wired.com/story/log4j-log4shell/)
is so very important to keep track of what happens in a given application,
Log4j happens to be an extremely popular library.
However,
lots of people **may not even know they use it**.

The other reason is
that this actively exploited vulnerability enables attackers
to trigger unexpected actions remotely.
This known exploit is commonly referred to as [remote code execution](../close-invisible-doors/).
As it poses a major security threat,
this vulnerability,
known as [Log4Shell](https://www.lunasec.io/docs/blog/log4j-zero-day/)
or [CVE-2021-44228](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44228),
has been rated critical with the highest possible [CVSS score of 10](https://nvd.nist.gov/vuln/detail/CVE-2021-44228).

After the discovery of Log4Shell on December 9,
the Apache Software Foundation has promptly released fixes
that have led to the discovery of two other vulnerabilities.

## The bombshell zero-day exploit

Log4j2 versions up to and including 2.14.1 are [vulnerable](https://logging.apache.org/log4j/2.x/security.html)
to Log4Shell.
These versions have a lookup feature that is used for fetching resources,
including accessing data
and downloading stuff from websites or other Java-based applications.
Since the beginning of this month,
attackers [have been exploiting](https://www.zdnet.com/article/log4j-flaw-attackers-are-making-thousands-of-attempts-to-exploit-this-severe-vulnerability/)
this feature
by logging a specially crafted string
(i.e., a specific sequence of characters)
into an interface that allows external input.
When their malicious code is included in a log message,
the attackers can get the application to execute various actions,
like connecting to a remote server,
performing [data leakage](https://www.microsoft.com/security/blog/2021/12/11/guidance-for-preventing-detecting-and-hunting-for-cve-2021-44228-log4j-2-exploitation/)
or installing malware.
For example,
threat actors are recently exploiting Log4Shell to [infect Windows devices](https://www.bleepingcomputer.com/news/security/log4j-vulnerability-now-used-to-install-dridex-banking-malware/)
with Dridex,
a Trojan for stealing bank credentials.
The attack chain is shown in Figure 1.

<div class="imgblock">

![Log4j attack chain](https://res.cloudinary.com/fluid-attacks/image/upload/v1640275685/blog/log4shell/log4shell-Figure-1.webp)

<div class="title">

Figure 1. Attack chain and recommended mitigating measures (in all caps).
Source: [govcert.ch](https://www.govcert.ch/blog/zero-day-exploit-targeting-popular-java-library-log4j/assets/log4j_attack.png).

</div>

</div>

A myriad of well-known services is vulnerable to Log4Shell.
To name a few:
The security issue has been proven on the [iCloud](https://www.lunasec.io/docs/blog/log4j-zero-day/)
infrastructure by replacing an iPhone's name with the malicious string.
It has also been discovered [on Steam](https://news.ycombinator.com/item?id=29499773)
by only entering the malicious code in the search box.
Even games are affected:
Attackers could get their way in by typing the code in the chatbox
in Minecraft Java Edition.
The list goes on:
[Amazon Web Services](https://aws.amazon.com/security/security-bulletins/AWS-2021-006/),
[Okta](https://sec.okta.com/articles/2021/12/log4shell),
[Cisco](https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-apache-log4j-qRuKNEbd),
etc.

## A patch a day keeps the attackers away

This vulnerability asked for an urgent call to action.
The Apache Software Foundation swiftly released Log4j version 2.15.0,
where they disabled the message lookups feature by default.
However,
users of this version can still enable this feature in configuration.
This gave way to another vulnerability,
discovered on December 14.
It is known as [CVE-2021-45046](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-45046)
and is rated critical with a CVSS score of 9.

Version 2.15.0 still left paths where message lookups could occur.
With the possibility to send the exploit code with the request,
threat actors could leak information
and execute code remotely in some environments
and locally in all environments.
So,
Apache released version 2.16.0.
Unfortunately, this version does not protect from [uncontrolled recursion](http://cwe.mitre.org/data/definitions/674.html).
That is,
any attacker could make the application crash by entering malicious data
that would cause excessive consumption of resources,
such as allocated memory.
This vulnerability,
discovered on December 16,
is known as  [CVE-2021-45105](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-45105)
and has a high severity rating with a CVSS of 7.5.

The risk of Denial of Service has already been addressed in the latest release,
**Log4j 2.17.0**.
For that,
we have to thank Apache Software Foundation's efforts
and security researchers that have worked inspecting every patch.

The global response to Log4Shell has been historical.
[Many](https://gist.github.com/SwitHak/b66db3a06c2955a9cb71a8718970c592)
organizations have already released their statements
saying whether they are affected by it.
Further,
[many](https://www.govcert.ch/blog/zero-day-exploit-targeting-popular-java-library-log4j/)
vendors that use the open-source library have rushed to patch their products.
Importantly,
the US Cybersecurity & Infrastructure Security Agency (CISA)
issued an [emergency directive](https://www.cisa.gov/emergency-directive-22-02)
where it ordered federal agencies to update
or apply mitigation measures (see Figure 1) by 5 p.m. EST on December 23.

Right now,
identification and remediation are key.
This may pose a problem for some.
As we hinted in the beginning of this post,
many organizations don't know
they use programs with Log4j.
This may be because
they don't maintain inventories of their software's components
and subcomponents.
Additionally,
the latest events may increase the activity of threat actors.
As independent security researcher Chris Frohoff [said](https://www.wired.com/story/log4j-log4shell/),
"What is almost certain is
that for years people will be discovering
the long tail of new vulnerable software
as they think of new places to put exploit strings."

## Our clients stand strong!

At `Fluid Attacks`
we're prepared to overcome this challenge.
Our clients using any of our [Plans](../../plans/)
can immediately find out if they use Log4j in their software.
In our [Attack Surface Manager](../../categories/asm/),
they can look for the vulnerability type
"011. Use of software with known vulnerabilities,"
under which any of Log4j's high to critical vulnerabilities should appear.
What should people do then?
Well,
teams that have Log4j 2 in their software should
**upgrade to [version 2.17.0](https://logging.apache.org/log4j/2.x/download.html)**
or the latest version,
should a newer version be released.

New vulnerabilities are being exploited daily.
Want to learn how to be better prepared for these threats?
[Get a demo](../../contact-us/)\!
