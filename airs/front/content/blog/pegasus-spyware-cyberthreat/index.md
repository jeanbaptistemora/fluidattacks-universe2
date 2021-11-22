---
slug: pegasus-spyware-cyberthreat/
title: Pegasus, Fraught With Peril!
date: 2021-07-26
subtitle: The spyware that threatens the world
category: attacks
tags: cybersecurity, company, trends, risk, technology, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1627305052/blog/pegasus-spyware-cyberthreat/cover-pegasus_blxx6i.webp
alt: Photo by Roi Dimor on Unsplash
description: 'In this post, we will look at the software everyone
  is talking about: Pegasus.'
keywords: Malware, Attack, Vulnerability, NSO, Cybersecurity, Ethical Hacking,
  Pegasus, Pentesting
author: Felipe Zárate
writer: fzarate
name: Felipe Zárate
about1: Cybersecurity Editor
source: https://unsplash.com/photos/70lKY2pk3yo
---

If you clicked on this post, it is because you want to understand what’s
going on with Pegasus, the world’s greatest cyber-hazard. And yes, the
situation is much more dangerous than you think.

Without a doubt, we are talking about something much more powerful than
the winged, immortal creature born from its mother blood, **Medusa**,
after being beheaded by **Perseus**. Unlike such a powerful mega-equine,
the software we’re talking about works almost undetectably. It has more
eyes than Gorgon’s head, more range than her son’s flight, and is more
ubiquitous than the constellation into which Zeus transformed the
beautiful winged horse.

With **Pegasus**, we have entered an era of espionage unprecedented in
human history. Today, each of us carries a potential spy in our pockets.
Yes, we had been warned for years about this possibility. [Privacy
policies](../gdpr-compliance/) have been created to prevent those small
devices from becoming omniscient eyes and ears of our life. However, no
program capable of using all those functions against us had ever been
made public… at least not until Pegasus arrived.

In this post, we will not focus on the
[political-international](https://www.washingtonpost.com/investigations/interactive/2021/nso-spyware-pegasus-cellphones/)
discussion behind
[Pegasus](https://www.nsogroup.com/Newses/following-the-publication-of-the-recent-article-by-forbidden-stories-we-wanted-to-directly-address-the-false-accusations-and-misleading-allegations-presented-there/).
Nor will we focus on the [ethical
considerations](https://www.theguardian.com/world/2021/jul/18/revealed-leak-uncovers-global-abuse-of-cyber-surveillance-weapon-nso-group-pegasus)
behind the development and use of this type of software. There are much
more [prepared
people](https://forbiddenstories.org/pegasus-the-new-global-weapon-for-silencing-journalists/)
doing such dissertations.

<div class="imgblock">

![Countries were Pegasus have operated](https://res.cloudinary.com/fluid-attacks/image/upload/v1627306731/blog/pegasus-spyware-cyberthreat/countries-pegasus_pkprvc.webp)

<div class="title">

Figure 1. Countries were **Pegasus** have operated. Taken from
[The Guardian](https://www.theguardian.com/news/video/2021/jul/19/pegasus-the-spyware-technology-that-threatens-democracy-video).

</div>

</div>

## What do we know about Pegasus?

Pegasus [is the main
product](https://www.theguardian.com/news/2021/jul/18/what-is-pegasus-spyware-and-how-does-it-hack-phones)
of [NSO Group](https://www.nsogroup.com/about-us/), which is an Israeli
surveillance company. According to [Jon
Gerberg](https://www.washingtonpost.com/investigations/interactive/2021/nso-spyware-pegasus-cellphones/),
a Washington Post reporter, NSO is dedicated "to make malicious software
that governments use to target your smartphone and gather data out of
it, and they sell this to governments all over the world." [Peter
O’Brien](https://www.france24.com/en/video/20210719-pegasus-spyware-how-does-it-work),
from France24, characterizes Pegasus as "easily installed, almost
impossible to detect and even harder to get rid of." In this sense,
there could be a point of comparison with
[Lazarus](../lazarus-malware-cyberattack/). But differently from Lazarus
governmental engagement, NSO, as a private company, works for whoever
they choose and who has enough money to pay them. They are [not
responsible for](https://www.nsogroup.com/Newses/enough-is-enough/) what
their clients do with the program they are selling.

Pegasus can infect almost every smartphone in the world (Android and
iOS) nearly without being noticed. [BGR
India](https://www.youtube.com/watch?v=opYd4LE0G5U) explains that it
became public in 2016 after the UAE human rights activist Ahmad Mansoor
sent a mysterious text message he got with a link to researchers. The
message alerted him about tortured prisoners in the country. He was
trying to verify the integrity of that information when the researchers
that examined that text told him it was a [smishing](../smishing/)
attack leading to malware. In fact, "[after the investigation, it was
found out that the links were linked back to the infrastructure
belonging to the NSO
group](https://www.youtube.com/watch?v=opYd4LE0G5U)."

## What is new with Pegasus?

Every spyware that allows remotely controlling a device must "enter" the
mobile phone somehow. From the time Pegasus was discovered in 2016 to
the present, the entry system into victims' phones has varied, but their
functions are practically identical. At first, Pegasus was known as [Q
Suite and
Trident](https://www.ndtv.com/india-news/what-is-pegasus-spyware-explained-2489195),
and its entry mode to the system was through classic
[phishing](../phishing/), [smishing](../smishing/) or
[spoofing](../spoofing/) methods. However, they have perfectionated
their entry techniques and now it is almost perfect (better than
Specter’s nearly unmatched modus operandi, another cyber threat we
[already talked about](../spectre/)).

Pegasus’s entry mode is known as **zero-click attack**. It allows the
attacker to access the device using a technique that "[relies on
exploiting software which receives data before the device can determine
if the data is coming from a trustworthy source or
not](https://www.youtube.com/watch?v=opYd4LE0G5U)." According to
[ZecOps](https://www.zdnet.com/article/apple-investigating-report-of-a-new-ios-exploit-being-used-in-the-wild/),
several Apple devices had a vulnerability in the Mail app that had not
been patched. Through it, [attackers could remotely access to infect a
machine](https://indianexpress.com/article/explained/zero-click-attacks-pegasus-spyware-7411302/).
The vulnerability was fixed, but that hasn’t stopped attackers from
figuring out ways to remotely access devices. In Android, the attackers
were targeting "[a vulnerability in the graphics library of the phone,
running version android 4.4.4 and
above](https://www.youtube.com/watch?v=opYd4LE0G5U)."

Other ways in which the zero-click attack can be performed are through
"[security bug in voice calls made through apps like
WhatsApp](https://www.youtube.com/watch?v=m2XR3W8QQFM)." If this weren’t
enough, the most sinister version of zero-click attacks removes all
traces of the entry attempt. Attackers can perform a miss call on the
victim, "[once the software is installed, it would delete the call log
entry so that the user wouldn’t even know about them as
called](https://www.youtube.com/watch?v=m2XR3W8QQFM)." This makes it a
perilous threat because **it is not based on social engineering**.
Attackers don’t have to wait for the victim to make a mistake. People
can handle their devices with the utmost care, and still, Pegasus can
get access to them.

<div class="imgblock">

![ clients and  tracked people. Taken from .](https://res.cloudinary.com/fluid-attacks/image/upload/v1627306951/blog/pegasus-spyware-cyberthreat/nso-clients-and-tracked-people_d2kl80.webp)

<div class="title">

Figure 2. **NSO Group** clients and **Pegasus** tracked people. Taken from
[The Guardian](https://www.theguardian.com/news/video/2021/jul/19/pegasus-the-spyware-technology-that-threatens-democracy-video).

</div>

</div>

## What can Pegasus do?

When installed on a device, "[the attacker can virtually control any
path of the phone](https://www.youtube.com/watch?v=m2XR3W8QQFM)."
Controllers can check all the media stored on the device: photos,
videos, messages, emails, credentials, passwords, etc. They can track
the GPS to have a detailed minute-by-minute map about the user’s
location. They can access the calendar to see what plans have been
scheduled. And the most spine-chilling thing of all is that at any time,
they can [turn on the microphone or camera to
record](https://www.france24.com/en/video/20210719-pegasus-spyware-how-does-it-work).
As long as a device is susceptible to being attacked by Pegasus, there
is no safe place.

All this occurs in such discreet, disguised and seemingly normal
circumstances that it is almost impossible to determine whether a device
has been infected with Pegasus. According to [Peter
O’Brien](https://www.france24.com/en/video/20210719-pegasus-spyware-how-does-it-work):
"The phone wouldn’t show any sign of being infected besides the finest
traces of abnormal software processes." As if all this were not enough,
even if a victim overcomes every obstacle to discover that she has been
affected by Pegasus, she cannot remove it from her system. It is not an
application. There is no software to restore the system to a pre-Pegasus
version. To top it off, " [the malware can stay even after a factory
reset](https://www.france24.com/en/video/20210719-pegasus-spyware-how-does-it-work)."

## Now what?

So, what can we do to protect ourselves from such a threat?\
Usually, I would give you advice such as "*be careful not to open
suspicious links*," "*if you see that there is something that should not
be on your cell phone, report it to the authorities immediately*."
However, none of these interim measures work with the all-mighty
Pegasus. It’s too powerful to be stopped by tricks of that nature.
Perhaps the only thing that could mitigate the opportunity for them to
enter your device is to have no device at all.

Don’t you think that’s good advice?\
Okay then…​ Here’s a genuine recommendation: **always keep your system
up to date**. Just as happened with the Mail vulnerability in iOS or
with that of the graphics card of Android systems, the related companies
were given the task of patch vulnerabilities spotted. That doesn’t
guarantee they won’t attack you, but it could minimize the risks.

We hope you have enjoyed this post!\
At `Fluid Attacks`, we look forward to hearing from you.\
[Contact us](../../contact-us/)!
