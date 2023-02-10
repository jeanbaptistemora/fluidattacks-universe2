---
slug: linux-trojan-xorddos/
title: XOR DDoS, Top Threat to Linux Today
date: 2022-05-26
subtitle: How does this clever Linux Trojan operate?
category: attacks
tags: cybersecurity, risk, credential, malware
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1653575325/blog/linux-trojan-xorddos/cover_xorddos.webp
alt: Photo by Jez Timms on Unsplash
description: Reportedly, the last six months have seen a 254% surge in this Linux Trojan's activity. Read this post to learn what it is and what should be done about it.
keywords: Xor Ddos, Xorddos, Linux, Trojan, Distributed Denial Of Service, Iot, Microsoft, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/pdR9sdvdb7Y
---

It has been a while since we covered issues on Linux.
Last time, [we talked about PwnKit](../linux-polkit-vulnerability/),
an "ancient" vulnerability common to several distributions
that allowed privilege escalation
to achieve root user permissions.
Now,
we look at a Linux Trojan
that acts as a distributed denial of service (DDoS)
[botnet](https://www.merriam-webster.com/dictionary/botnet).
Though this Trojan was [discovered in 2014](https://blog.malwaremustdie.org/2014/09/mmd-0028-2014-fuzzy-reversing-new-china.html),
the Microsoft 365 Defender Research Team [says](https://www.microsoft.com/security/blog/2022/05/19/rise-in-xorddos-a-deeper-look-at-the-stealthy-ddos-malware-targeting-linux-devices/)
they have observed a 254% jump in its activity
over the last six months.
Let's see what it is about.

## What is XOR DDoS?

The Trojan's name is XOR DDoS (or XorDdos).
Let's break that name down real quick:
XOR refers to the form of encryption it uses
for communications with its command-and-control
[(C2) server](https://www.techtarget.com/whatis/definition/command-and-control-server-CC-server)
(e.g.,
it writes the string `m6_6n3` to mean directory `/tmp`),
and DDoS refers to the [kind of attack](https://attack.mitre.org/techniques/T1498/001/)
it carries out.
This Trojan accomplishes DDoS by flooding the server with threads
(i.e., lightweight processes),
which are so many that,
in the end,
legitimate clients are denied the targeted resources,
or the server crashes.
These attacks can also be a way
to mask the attacker's further malicious activities,
which include gaining unauthorized access.

Back in 2014,
when the ethical hacking group [MalwareMustDie](https://www.malwaremustdie.org/)
discovered this Trojan,
they attributed it to Chinese threat actors
and warned how serious it was,
given its complexity and how hard it was to detect.
By 2015,
the Trojan [was said](https://thehackernews.com/2015/09/xor-ddos-attack.html)
to have compromised more than 20 websites per day,
mainly in Asia.
It has become more pervasive in recent years,
rising as [the top threat](https://thehackernews.com/2022/05/microsoft-warns-rise-in-xorddos-malware.html)
to Linux machines.
Reportedly,
XOR DDoS has been affecting Internet of Things (IoT) devices
and cloud infrastructures,
progressively gaining points from which to launch further attacks.

XOR DDoS attempts to get access to systems
[mainly](https://www.microsoft.com/security/blog/2022/05/19/rise-in-xorddos-a-deeper-look-at-the-stealthy-ddos-malware-targeting-linux-devices/)
by conducting [brute force attacks](../pass-cracking/)
on devices across loads of servers.
Once it finds credentials that work on a device,
this Trojan runs a script with root privileges
to download and install itself on the device.
It uses clever ways to conceal how it got there,
like downloading itself to a temporary file storage directory
or overwriting log files.

<cta-banner
  buttontxt="Read more"
  link="/solutions/ethical-hacking/"
  title="Get started with Fluid Attacks' Ethical Hacking solution right now"
/>

This Trojan has several persistence mechanisms,
that is,
techniques to keep its access to systems across restarts.
Put simply,
it stores scripts to determine
that it should be run every time the system starts up.
Its mechanisms are plenty
so that at least one of them works
on any of several Linux distributions.

Another malicious action that XOR DDoS does is
it sends device information to the threat actor.
As [reported by Microsoft](https://www.microsoft.com/security/blog/2022/05/19/rise-in-xorddos-a-deeper-look-at-the-stealthy-ddos-malware-targeting-linux-devices/),
it includes "OS release version,
malware version,
rootkit presence,
memory stats,
CPU information,
and LAN speed."
This data can be used to plan more specific,
custom attacks on the device.
An example of this is
that another Linux Trojan called Tsunami was contracted later
by some of the infected devices
but, as Microsoft explained,
this other Trojan was not installed by XOR DDoS,
so it is likely that the latter
"is leveraged as a vector for follow-on activities."

To perform DDoS,
the Trojan enumerates the processors in the device
and then moves on to create threads twice that number.
After that,
the Trojan receives commands from the C2 server to flood the device,
rendering it unable to respond.

## What Linux users should be doing about XOR DDoS

Currently,
a generalized warning has been made to Linux administrators.
They are being urged
to have the latest endpoint
and server defenses on their systems.
The risk is clear:
DDoS attacks are a big deal.
They are even used as a weapon in cyberwar.
This has been reported,
for example,
in the [conflict between Russia and Ukraine](../timeline-new-cyberwar/).
Moreover,
as shown in a [report by Kaspersky](https://securelist.com/ddos-attacks-in-q1-2022/106358/),
this kind of attack hit record numbers
in the first quarter of the current year.
An aggravating factor is that,
as mentioned,
many of the Internet-connected devices that have been affected are IoT devices.
This poses a challenge for many users
because [these are often not properly secured](https://techmonitor.ai/technology/cybersecurity/xorddos-malware-targeting-linux-devices),
as manufacturers prioritize
quickly getting the product out in the market.

There are some [specific things](https://www.microsoft.com/security/blog/2022/05/19/rise-in-xorddos-a-deeper-look-at-the-stealthy-ddos-malware-targeting-linux-devices/)
that Linux administrators should start doing right now.
First thing is becoming aware
of whether their systems are being targeted.
It could be the case
if they detect a large number of failed login attempts.
Also,
some ways of protecting their Internet-facing servers
are to deploy antimalware software
and disallow remote password access.
Furthermore,
administrators need to "enable network protection
to prevent applications or users from accessing malicious domains
and other malicious content on the internet."
Lastly,
all other users should be urged to be cautious too.
They really need to take security measures
as simple as creating and rotating strong passphrases
(even [more secure than passwords](https://docs.fluidattacks.com/criteria/requirements/132/))
and complying with the activation of multi-factor authentication.

Did you like this post?
Then subscribe to our newsletter
to be up to date on the latest cyberattacks
and cybersecurity trends.
