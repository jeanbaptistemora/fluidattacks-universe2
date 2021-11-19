---
slug: lockbit-ransomware/
title: Now a Ransomware Seducing Insiders?
date: 2021-08-27
subtitle: Find out about LockBit, now in its menacing 2.0 version
category: techniques
tags: software, hacking, cybersecurity, company, risk, information
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1630079924/blog/lockbit-ransomware/cover_lockbit_xhxdf5.webp
alt: Photo by Icons8 Team on Unsplash
description: In this post, you'll learn in general terms what LockBit
  ransomware is, what its characteristics are and why it can pose
  a significant threat to your business.
keywords: Lockbit, Ransomware, Malware, Encryption, Insider, Employee, Company,
  Pentesting, Ethical Hacking
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/sBbm92cRIQo
---

[Ransomware](../ransomware/),
[ransomware](../pipeline-ransomware-darkside/),
[ransomware](../cyber-insurance-ransomware/); everyone is talking about
it. Thinking about being a victim of ransomware surely scares many of
us. Nevertheless, despite all the dissemination about it, many people
may not be, or irrationally may not *want* to be, sufficiently aware of
it. That’s why we continue to publish information related to this type
of attack. Also, because it is a phenomenon that continues to evolve,
and new groups of criminals with different forms of malware and
strategies keep sprouting up and shooting at new targets. Today it’s
time for LockBit, the ransomware behind which there is a gang that would
like to hire some of your employees. Let’s see what it’s all about.

## What is LockBit, and what does it do?

[Two years
ago](https://resources.infosecinstitute.com/topic/lockbit-malware-what-it-is-how-it-works-and-how-to-prevent-it-malware-spotlight/),
the data encryption malware LockBit began operating, which later became
part of the Ransomware as a Service (RaaS) model —something we have
already referred to [in a previous post](../ransomware-as-a-service/).
Among Lockbit’s outstanding attributes are its abilities to
self-propagate and encrypt large and valuable enterprise IT systems in a
short time to avoid detection. [As Ilascu for Bleeping Computer once
said](https://www.bleepingcomputer.com/news/security/lockbit-ransomware-moves-quietly-on-the-network-strikes-fast/),
"LockBit attacks leave few traces for forensic analysis as the malware
loads into the system memory, with logs and supporting files removed
upon execution."

LockBit is launched by attackers through a PowerShell script, usually
after compromising a network, for example, by [brute
force](../pass-cracking/) or [phishing](../phishing/) (or at one of your
employees' own will). This malicious software disables the security and
information recovery programs as a preliminary step in an independent
way. Once the network is vulnerable, LockBit automatically spreads
easily across different devices. From there, in its operation as
ransomware, it starts encrypting system files. And, [as shared in
Kaspersky](https://www.kaspersky.com/resource-center/threats/lockbit-ransomware),
"Victims can only unlock their systems via a custom key created by
LockBit’s proprietary decryption tool." LockBit changes the names of the
file extensions on the target device to ".abcd" and creates a text file
in each affected folder, with instructions for the victim, called
"Restore-My-Files.txt" (see Figure 1).

<div class="imgblock">

![Restore-My-Files.txt](https://res.cloudinary.com/fluid-attacks/image/upload/v1630080709/blog/lockbit-ransomware/lockbit_howtoremove_vprjhu.webp)

<div class="title">

Figure 1. Restore-My-Files.txt screenshot
(source: [howtoremove.guide](https://howtoremove.guide/wp-content/uploads/2020/01/lockbit.png)).

</div>

</div>

[The victim
then](https://resources.infosecinstitute.com/topic/lockbit-malware-what-it-is-how-it-works-and-how-to-prevent-it-malware-spotlight/)
has at her disposal a [Tor](https://www.torproject.org/) link through
which she can learn more about the ransomware, even establishing direct
communication with one of the LockBit operators. These conversations
begin to revolve around "the ransom demand, payment deadline, method
—usually in Bitcoin— and instructions on how to purchase
cryptocurrency," [said Osborne for Zero
Day](https://www.zdnet.com/article/a-deep-dive-into-the-operations-of-the-lockbit-ransomware-group/).
The victim also receives the opportunity to decrypt and recover a small
file as a supposed warranty that the other files can be retrieved once
the payment is made. We must also note that, apart from this ".abcd"
variant, [we can also
find](https://www.kaspersky.com/resource-center/threats/lockbit-ransomware)
the ".LockBit" extension variant and even a version in which the Tor
browser ([generally used for the Dark Web](../dark-web/)) is no longer
required.

On the other hand, among the improvements to this malware that were
reported later, we can recognize its ability to disable the security
prompts that users receive when an application tries to run as
administrator. LockBit now has a configuration that allows it to steal
copies of data from servers. That’s data that can be made public at the
whim of the attackers, especially if the victims are reluctant to
respond with the requested payment. LockBit, in its 2.0 version, has
"one of the fastest and most efficient encryption methods in today’s
ransomware threat landscape," [according to Trend
Micro](https://www.trendmicro.com/en_us/research/21/h/lockbit-resurfaces-with-version-2-0-ransomware-detections-in-chi.html).
[Another significant
change](https://www.bleepingcomputer.com/news/security/lockbit-ransomware-recruiting-insiders-to-breach-corporate-networks/)
(in terms of presentation), for many people outlandish, has been the
offer of millions of dollars in exchange for "**corporate insiders**"
who help breach and encrypt the targeted companies' networks (see Figure
2).

<div class="imgblock">

![LockBit 2.0 wallpaper](https://res.cloudinary.com/fluid-attacks/image/upload/v1630080709/blog/lockbit-ransomware/lockbit_bleepstatic_lkng4v.webp)

<div class="title">

Figure 2. LockBit 2.0 wallpaper for insider recruitment
(source: [bleepstatic.com](https://www.bleepstatic.com/images/news/ransomware/l/lockbit/lockbit-2.0/recruiting-insiders/wallpaper.jpg)).

</div>

</div>

## An eye-catching recent case

[It is now
common](https://www.zdnet.com/article/a-deep-dive-into-the-operations-of-the-lockbit-ransomware-group/)
for ransomware payouts to reach millions of dollars; remember [the case
of JBS](../jbs-revil-cyberattack/). However, [according to
Osborne](https://www.zdnet.com/article/a-deep-dive-into-the-operations-of-the-lockbit-ransomware-group/),
LockBit affiliates are currently requesting an average of around 85
thousand dollars from each victim, of which 10-30% corresponds to RaaS
operators. One of the most reported cases of attack with this malware in
recent days has been the hit on the Fortune 500 [professional services
and consulting multinational](https://en.wikipedia.org/wiki/Accenture)
[**Accenture**](https://www.accenture.com/us-en). [They were
listed](https://www.zdnet.com/article/accenture-says-lockbit-ransomware-attack-caused-no-impact-on-operations-or-clients/)
on the leak site of the LockBit group next to a countdown timer, and the
operators left a short message from a supposed insider (see Figure 3).

<div class="imgblock">

![LockBit page](https://res.cloudinary.com/fluid-attacks/image/upload/v1630080708/blog/lockbit-ransomware/lockbit_zdnet_a6sdhw.webp)

<div class="title">

Figure 3. LockBit page screenshot
(source: [zdnet.com](https://www.zdnet.com/a/hub/i/2021/08/11/86850a36-4a44-4a8b-bf62-768796ddcb50/e8fcnngucaqitfy.png)).

</div>

</div>

Once the timer reached zero, some of Accenture’s information would be
released, and indeed it was. However, there was [no sensitive
information
there](https://therecord.media/accenture-downplays-ransomware-attack-as-lockbit-gang-leaks-corporate-data/)
—mainly marketing material. The company had already said that the
ransomware had not affected its operations and that they had managed to
restore systems from their backups. [From the research firm
Cyble](https://twitter.com/AuCyble/status/1425422006690881541), there
was commentary that the LockBit group was demanding $50M as a ransom for
a database of approximately 6TB. Do they really have all that data, and
will they reveal it later? Or is it just a bluff? Has Accenture already
made a payment? One thing that seems clear for now is that the attack’s
aftermath will be a bad reputation for this organization, at least as
far as [its cybersecurity
services](https://www.accenture.com/us-en/services/security-index) are
concerned.

## For the umpteenth time, let’s question ourselves

Today, it is quite curious that most of the companies that were victims
of ransomware attacks and paid the ransom ([said to be around 80% within
one
study](https://www.zdnet.com/article/most-firms-face-second-ransomware-attack-after-paying-off-first/))
have been victims a second time, perhaps even at the hands of the same
criminals. How not to come to one’s senses after such a blow?
Professional services and sectors such as transportation, construction,
and food are among the most threatened by LockBit around the world.
Within these sectors and, in fact, within all companies, cybersecurity
should gain priority, primarily in terms of prevention. But we are
witnessing the paltry value that messages like "don’t wait to be
attacked to take action" are having. Now, in many cases, there’s no
action even after impact\!

Regardless of the veracity of what a man referred to as "Aleks," an
alleged LockBit operator, [told Cisco Talos a year
ago](https://talos-intelligence-site.s3.amazonaws.com/production/document_files/files/000/095/481/original/010421_LockBit_Interview.pdf),
some of the words he conveyed could work as an additional nudge for many
of us. Not a boost to criminality, of course not, but to adequate
security practices. What Aleks said was that he became interested in
ransomware because of its profitability but that it also allowed him to
"*teach*" organizations about the consequences of inappropriate data
protection. Therefore, it is worth asking, how sure are you that your
software and systems are in optimal security conditions?

Additionally, the intentions of LockBit 2.0 are already forcing even
many to ask questions perhaps not previously considered. We now enter
the area of **reliability** of your staff. To conclude, a perfect
example of such questions is the one [posed by Div of
Cybereason](https://securityboulevard.com/2021/08/lockbit-ransomware-wants-to-hire-your-employees/):

> Can you be sure that there is nobody in your company who might
> consider potentially making millions of dollars by helping to launch a
> ransomware attack?

At `Fluid Attacks`, we can help you with cybersecurity from prevention.
[Contact us\!](../../contact-us/)
