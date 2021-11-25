---
slug: emotet-returns/
title: The Dangerous Comeback of the Year
date: 2021-11-24
subtitle: Emotet may be back for the crown as king of malware
category: attacks
tags: cybersecurity, windows, software, social-engineering, flaw, risk
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1637711055/blog/emotet-returns/cover_emotet.webp
alt: Photo by Markus Spiske on Unsplash
description: Emotet reigned as the most dangerous malware before the shutdown
  of its servers earlier this year. Unfortunately, this month
  has seen its reappearance.
keywords: Emotet, Trickbot, Malware, Botnet, Email Spoofing, Word Document,
  Macros, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/KP1bubr2j4A
---

Emotet is a malicious program whose distribution infrastructure was
taken down this year in January by law enforcement agencies from several
countries. Up until that point, Emotet had infected more than 1.6M
computers "and caused hundreds of millions of dollars in damage
worldwide," according to a
[publication](https://www.justice.gov/opa/pr/emotet-botnet-disrupted-international-cyber-operation)
by the US Department of Justice’s Office of Public Affairs. The victims
stemmed from various sectors, including the government, academia,
banking, technology, e-commerce and healthcare.

Even though Emotet’s dismantling drastically reduced the number of
events related to that malware, the victory was relatively short-lived.
Recently, TrickBot, a malware closely linked to Emotet, has been
distributing emails with attachments laced with malware in a way that
resembles the latter. These facts point to the possible comeback of the
"king of malware," as the president of the German Federal Office for
Information Security
[called](https://www.zeit.de/news/2021-01/27/koenig-der-schadsoftware-emotet-ist-entmachtet)
it.

## Emotet’s rise and fall

[Emotet](https://thehackernews.com/2020/11/anyrun-emotet-malware-analysis.html)
was discovered in Europe in 2014. Its first victims were small companies
located mainly in Austria and Germany. In its beginnings, its
functionality was that of the standard banking malware. That is, it was
essentially a program used to steal credentials for bank accounts. It
was [delivered](https://www.malwarebytes.com/emotet) to unsuspecting
users via legit-looking emails referencing financial documents, using
lures like "Your Invoice" or "Payment Details." The user was
[prompted](https://www.kaspersky.com/resource-center/threats/emotet) to
follow an embedded link to a malicious Word file or download the file
directly from the email. The Word document asked the user to enable
macros. If enabled, that triggered an automated procedure to read hidden
code that installed the malware. Once in the system, Emotet read the
victim’s emails and constructed malicious ones out of them, which it
later sent to the victim’s contacts.

The malware [later](https://www.malwarebytes.com/emotet) evolved to have
spamming and malware delivery services. Functioning as the initial
infection vector, it started
[distributing](https://www.checkpoint.com/downloads/resources/cyber-attack-trends-report-mid-year-2021.pdf?mkt_tok=NzUwLURRSC01MjgAAAGAOUl3icS9KYCbEoZ423xraTBSpYqDprjf6yC9DTL-5CrR1SrAngrHRuxpHMzPepxIx23Y4o9X33cVflu8UjtFpD9laKtOWumSaxU4LToSUGoiz8Bj)
Qbot and TrickBot banking Trojans, as well as
[Ryuk](https://www.kaspersky.com/resource-center/threats/ransomware-attacks-and-types)
ransomware. Emotet has always liked to expand its horizons. In recent
years, it was
[present](https://thehackernews.com/2020/11/anyrun-emotet-malware-analysis.html)
in several countries and was rented to cybercrime groups. Further, in
February last year, it was found that the malware was [scanning Wi-Fi
networks](https://www.kaspersky.com/resource-center/threats/emotet) from
connected affected devices. It tested passwords trying to get access,
which it then leveraged to spread to other devices.

The difficulty of getting rid of Emotet was one of its strengths. It has
been [called](https://www.kaspersky.com/resource-center/threats/emotet)
polymorphic. This refers to the malware’s mutability. Every time its
code was accessed, it somehow suffered changes. Given that many
antivirus programs perform signature-based searches (i.e., they find a
threat if it matches a unique identifier), the ever-changing Emotet
escaped detection. Another evasion technique was that Emotet could lie
dormant if it arrived in a [sandbox
environment](https://stackoverflow.com/a/2126185). This refers to an
isolated test environment where malware functionalities can be observed
without major threats to servers and other resources.

Emotet’s destructiveness throughout the years was huge, with the
remediation of each incident in the US
[costing](https://us-cert.cisa.gov/ncas/alerts/TA18-201A) up to $1M. In
2020, it was the most distributed malware worldwide. But on January 26,
2021, Europol informed in a [press
release](https://www.europol.europa.eu/newsroom/news/world%E2%80%99s-most-dangerous-malware-emotet-disrupted-through-global-action)
that investigators had taken down Emotet’s infrastructure, which
"involved several hundreds of servers located across the world," in a
multinational operation. Further, in April, a [mass
uninstall](https://therecord.media/emotet-botnet-returns-after-law-enforcement-mass-uninstall-operation/)
got rid of the malware from infected computers. With Emotet banished,
[TrickBot and a few
other](https://www.checkpoint.com/downloads/resources/cyber-attack-trends-report-mid-year-2021.pdf)
contenders stepped up to claim the throne.

## Emotet, back from the grave

On November 14, security researchers Luca Ebach and colleagues
[observed](https://cyber.wtf/2021/11/15/guess-whos-back/) on their
TrickBot trackers that this malware was attempting to install Emotet.
Well, at least what looks like Emotet. They executed a sample, a URL
dropped by TrickBot, in their sandbox system. They observed that "The
network traffic originating from the sample closely resembles what has
been observed previously \[…​\]: the URL contains a random resource path
and the bot transfers the request payload in a cookie \[…​\]." However,
the researchers noted that the malware now uses different encryption to
hide data and [secures network
traffic](https://attack.mitre.org/techniques/T1071/001/) with HTTPS
instead of unencrypted HTTP. This means that communication between the
infected system and Emotet’s command and control server can be
concealed. This state of affairs suggests that TrickBot is now offering
help in Emotet’s resurrection by installing it on systems it has
infected. Indeed, it has been reported
[elsewhere](https://www.zdnet.com/article/emotet-once-the-worlds-most-dangerous-malware-is-back/)
that Emotet’s new variant is not redistributing itself but relying on
TrickBot for spreading.

A thread in the SANS Internet Storm Center forums
[reported](https://isc.sans.edu/forums/diary/Emotet+Returns/28044/) that
the emails of the new variant have three types of attachments: Word
files, Excel files and a password-protected zip folder containing a Word
document. The original poster added that the emails were
[spoofed](../spoofing/) replies. They were created out of data from
stolen email chains that may have been gathered from previously infected
hosts. All in all, this new variant seems at least as sophisticated as
you would expect from Emotet. Therefore, it may be a sign that there is
trouble ahead.

<div class="imgblock">

![Emotet infection process](https://res.cloudinary.com/fluid-attacks/image/upload/v1637711055/blog/emotet-returns/Emotet-Figure-1.webp)

<div class="title">

Figure 1. The process of new Emotet infections. Source:
[isc.sans.edu](https://isc.sans.edu/diaryimages/images/2021-11-15-ISc-diary-image-01.jpg).

</div>

</div>

It has been said (e.g.,
[here](https://therecord.media/emotet-botnet-returns-after-law-enforcement-mass-uninstall-operation/)
and
[here](https://www.zdnet.com/article/emotet-once-the-worlds-most-dangerous-malware-is-back/))
that it is uncertain whether or not Emotet will get back to its place on
the top. Admittedly, Emotet is pretty far from regaining its previous
title. But it really is too soon to tell. For now, security researchers
are urging network administrators to block [a
list](https://twitter.com/abuse_ch/status/1460308766767915013) of
command and control servers to prevent traffic to them and, ultimately,
infection.
