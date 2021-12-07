---
slug: attribution-clues/
title: Jigsaw Falling Into Place
date: 2021-12-07
subtitle: Clues in the investigation of cyberattacks
category: attacks
tags: cybersecurity, software, vulnerability, company, exploit, training
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1638883041/blog/attribution-clues/cover_attribution.webp
alt: Photo by Clark Van Der Beken on Unsplash
description: We describe the kinds of technical traces
  left in the phases of a cyberattack
  and talk about how they may help the attribution process.
keywords: Artifacts, Attribution, Malware, Investigation, Phishing, Attack,
  Ttp, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/596baa0MpyM
---

When investigating a cyberattack,
the question arises as to who was the perpetrator.
The process of finding the answer is commonly referred to as "attribution."
According to Dr. Char Sample,
a research scientist at Carnegie Mellon University,
[attribution is](https://securityintelligence.com/qa-with-dr-char-sample-what-is-attribution-and-how-can-it-help-fight-attackers/)
"determining the source identity or location of the intruder."
This is a complex thing.
Authors Florian Skopik and Timea Pahi [posit](https://doi.org/10.1186/s42400-020-00048-4)
that attribution must be done
knowing the adversaries' common attack tools and techniques.
They explain
that these techniques may leave traces in the victim's infrastructure.
So,
it is important to study these traces carefully.

We would like to share a few contents from [an article](https://doi.org/10.1186/s42400-020-00048-4)
by Skopik and Pahi published in the Journal Cybersecurity.
They present,
among other things,
the common phases in attacks,
the traces that they leave,
and the questions in the attribution process
that can be answered by investigating these traces.

## Phases in the kill chain

An attack commonly starts with a **reconnaissance** phase.
Adversaries first probe and research their victims as thoroughly as possible.
Having gained sufficient knowledge,
they borrow or craft malware,
malicious code or files in a **weaponization** phase.
Next is **delivery**,
for example,
via [phishing](../phishing/) emails
or through [injection](../sql-injection/)
(e.g., disrupting the target by entering code via an interface for data input).

After a successful delivery,
attackers do things like installing [backdoors](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-83r1.pdf)
during **exploitation**.
These are programs
that enable remote access to the host's functions and data.
During **installation**,
attackers pivot through the system to find valuable information.
For them,
gaining permanent control is crucial.
So,
during the **command and control** phase,
they may execute specific malware
to create a channel where they can control a system remotely.
From then on,
they are in the **actions** phase.
(Well,
we've described actions all the way until now,
but let's just agree that there's no single, simple way
to call what attackers do from then on.)
In this phase,
attackers carry out their goal remotely,
be it system damage, interruption of operations, data exfiltration,
manipulation or destruction, etc.

Behavior pertaining to the phases described above leave traces
that may aid the attribution process.
These are commonly known as "[artifacts](https://insider.ssi-net.com/insights/what-is-an-artifact-in-cyber-security)."
Let's take a look at them.

## Hunting for clues

**Reconnaissance artifacts** help researchers identify
whether attackers did any scanning attempt on the network,
tried to gather information through phishing,
performed [brute force attacks](../pass-cracking/),
and so on.
Some of these artifacts may be registered in logs.
Others,
like repeated visits to the victim's social networking profiles,
are shown in the profile statistics.
Phishing may be evident in emails,
the content of which may include messages trying to influence the victim
(read more [here](../social-engineering/)).
What's written tells researchers how much insider knowledge was used,
if any.
If the email seems extremely legit,
that may mean the attackers knew the victim pretty well.

**Weaponization artifacts** respond to the questions
of how complex the attack was and,
consequently,
how much effort the attackers had to exert.
Maybe the attackers exploited a known vulnerability.
Maybe the malware's signature (its unique identifier) may hint
where the attackers rented malware.
Maybe there are URLs embedded in the malware reported already.
That is,
addresses through which it is known specific malware is distributed.

**Delivery artifacts** give researchers hints
about things like where the user acquired the malware.
In phishing,
the medium may be different from email.
For example,
instant messenger apps.
But the attackers may also use physical tools.
They may install [devices](../human-security-sensor/)
inside the company's facilities
or leave behind malware-carrying [USB flash drives](https://hackcontrol.org/cases/thumb-drive-awareness-lost-usb-attacks-explained/).

**Exploitation artifacts** address questions
like the number of techniques that had to be applied
and whether the attack was centered in a carefully selected device.
Malware analysis may show reported [obfuscation techniques](https://www.zdnet.com/article/a-question-of-security-what-is-obfuscation-and-how-does-it-work/).
That is,
how it hides its functionality
and prevents being detected by anti-malware software.
Moreover,
it may also show how personalized the code is.
When testing malware functionality,
researchers can determine whether it is a [Remote Access Trojan](https://www.techtarget.com/searchsecurity/definition/RAT-remote-access-Trojan),
which enables the attackers to have full remote control over the system,
or if its functionality seems more specific to the target.

**Installation artifacts** may be used
to find out the time it took the attackers to scan the network
and localize the resources of interest (like valuable information),
as well as the path they followed.
Researchers can make assumptions about the number of people involved
in the operation
and their working hours
from the attackers' behavior traceable in the log files,
including recorded user sessions.
Further,
it's useful to know whether the attackers modified log files to hide tracks
and used techniques to distract monitoring.
The authors remark
that "Often only secret services have the capabilities and resources
to carry this out on a high sophistication level."
This may be key when identifying attacks carried out
in the name of a [nation-state](https://www.forbes.com/sites/forbesbusinesscouncil/2021/04/16/cybersecurity-and-nation-state-threats-what-businesses-need-to-know/?sh=239a99587c21).

**Command and control artifacts** tell researchers
what infrastructure the attackers used.
Logs in infected devices provide information
about the communication with malicious URLs and external domains.
As infrastructures are costly,
attackers likely rented theirs.
Indeed,
the domain used to host the command and control servers may link
to a registrar and payment information.
Further,
given that the servers had to be acquired and paid for,
the providers might help identify the actors.
In an [exceptional example](https://www.securityweek.com/attackers-leave-server-credentials-ransomwares-code),
attackers left,
among other things,
their credentials for access to their server
in the code of the ransomware they deployed.
Further,
it was possible to access the decryption key and free the files.

Lastly,
**actions artifacts** may be the executed processes
and accessed files shown in an infected device's log data.
Researchers can recognize unknown traffic
that they can gather from firewalls,
proxies and Domain Name System servers.
They may find addresses of external devices used by the perpetrators
and addresses to external infrastructures,
such as the cloud service where their drop zone is located.
That is,
sites where exfiltrated files are stored.
If cloud and domain service providers are cooperative,
they may help identify the attackers.

<div class="imgblock">

![Artifacts categorization](https://res.cloudinary.com/fluid-attacks/image/upload/v1638883248/blog/attribution-clues/attribution_Figure-1.webp)

<div class="title">

Figure 1. The authors' categorization of artifacts for the attribution process.
Source: [media.springernature.com](https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs42400-020-00048-4/MediaObjects/42400_2020_48_Fig4_HTML.png?as=webp).

</div>

</div>

## Putting the pieces together

So, now what?
Well,
the several collected artifacts should reveal some characteristics
about the capabilities of the attackers:
Whether they seem skilled and experienced,
if they knew the victim well
and whether they were on a budget or had lots of resources.
Artifacts may also offer a hint
as to whether the attack is part of a bigger campaign,
what are the motivations
and whether a known threat actor is responsible.

Granted,
the investigation is rife with challenges.
The authors know
that some clues are more trustworthy than others that can be modified.
Further,
similar modi operandi are adopted from one group of attackers to another.
Complicating matters,
private investigators may not be able to gather some information
regarding the attackers' infrastructure
that may,
however,
be made available to a nation-state's secret services.
Additionally,
sociopolitical events should be accounted for in the analysis.

Despite the limitations of the attribution process
based on technical artifacts,
it remains highly interesting.
If the evidence doesn't point to the specific attackers,
at least a comprehensive account is made of what needs to be remediated.

Want to find your software's vulnerabilities before attackers do?
[Contact us](../../contact-us/)\!
