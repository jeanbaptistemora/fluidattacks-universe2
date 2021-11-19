---
slug: jbs-revil-cyberattack/
title: 'A Global Attack: JBS Case'
date: 2021-06-08
subtitle: '"A cyberattack on one is an attack on us all"'
category: attacks
tags: cybersecurity, company, trends, risk, technology, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1627389786/blog/jbs-revil-cyberattack/cover-jbs-revil-cyberattack_t9s8bc.webp
alt: Photo by NASA on Unsplash
description: FBI stated REvil as a global threat after confirming their
  attack on the IT architecture of the world's largest
  meat-producing company, JBS.
keywords: Ransomware, Attack, Vulnerability, Software, Cybersecurity,
  Ethical Hacking, Revil, Pentesting
author: Felipe Zárate
writer: fzarate
name: Felipe Zárate
about1: Cybersecurity Editor
source: https://unsplash.com/photos/yZygONrUBe8
---

## What happened?

The world’s largest meat producer was attacked by **REvil** on May 31.
After the attack, it had to shut down multiple processing plants around
the world. In Canada, the United States, and Australia, [some
facilities](https://cutt.ly/XnE9cvF) had to close. Especially, "[JBS
shut down operations at its Dinmore Australia facility — the biggest
beef plant in the southern hemisphere.](https://cutt.ly/XnE9cvF)"

**JBS** [did not publicly confirm](https://cutt.ly/InE9sOX) what kind of
attack it was. They also [refrained from pointing
out](https://cutt.ly/HnE9hxU) any responsibility. The world’s press
accessed this information thanks to a White House [press briefing on
June 1](https://cutt.ly/hnE9f9W). There, Ms. Karine Jean-Pierre, the
White House Principal Deputy Press Secretary, revealed that it was a
[ransomware attack](../ransomware). And, it was
[Bloomberg](https://www.bloomberg.com/news/articles/2021-06-02/hacking-outfit-linked-to-russia-is-behind-jbs-cyberattack)
who revealed that it was an attack perpetrated by REvil.

At `Fluid Attacks`, we have already talked about
[**ransomware**](../ransomware) and [**Ransomware as a Service
(RaaS)**](../ransomware-as-a-service). So it is enough to summarize that
this attack consists of installing “[malware that encrypts its target’s
systems](https://cutt.ly/InE9sOX).” Its purpose is to ask for money to
decrypt that data or to prevent it from being published.

## Who are those involved?

The **victim** is JBS, a company that, according to its [official
website](https://jbsfoodsgroup.com/our-business), is the \#1 global beef
producer, \#1 global poultry producer, \#2 global pork producer. They
also own [Primo](https://primo.com.au/), "Australia’s largest provider
of ham, bacon, salami, and deli meats."

The perpetrator is
[REvil](https://www.bbc.com/news/world-us-canada-57338896), "a criminal
network of ransomware hackers that first came to prominence in 2019."
This group is also [known as **Sodinokibi**](https://cutt.ly/PnE3yt0)
and appeared in [April 2019](https://cutt.ly/mnE3rGG). Since then, REvil
has incorporated into its criminal portfolio cyberattack methods such as
"[malicious spam campaigns and RDP attacks](https://cutt.ly/PnE3yt0),”
but always having ransomware as its main attack.

In our [last post](../ransomware-as-a-service/), we pointed out that the
[GandCrab gang ended operations](https://cutt.ly/WnE3isA) after a year
of trading with exorbitant profits. Some of the gang members would
presumably be [linked to REvil](https://cutt.ly/inE3p0o), a gang that
uses an attack model known as RaaS (see Figure 1). According to the [FBI
statement](https://cutt.ly/0nE9o2c) they are the main suspect of the JBS
cyberattack.

<div class="imgblock">

![REvil Timeline](https://res.cloudinary.com/fluid-attacks/image/upload/v1623159152/blog/jbs-revil-cyberattack/figure1_j9ezca.webp)

<div class="title">

Figure 1. [REvil
Timeline](https://www.secureworks.com/blog/REvil-the-gandcrab-connection)

</div>

</div>

In October 2020, "UNKN", one of the REvil ransomware syndicates, took an
interview that was published on the Russian-speaking tech Youtube
channel "[Russian OSINT](https://www.youtube.com/watch?v=ZyQCQ1VZp8s)."
It was posted on the official website of [Advanced
Intelligence](https://cutt.ly/rnE0RRY), where it was argued that the
name evokes the Resident Evil franchise. In the same interview, REvil
claimed to make a revenue of $100M in 2019; a year with the goal of
achieving at least $1B, ideally $2B. This is consistent with the figure
estimated by the [IBM Security X-Force report](https://cutt.ly/mnE9u4a)
published in September 2020. According to SecurityIntelligence, in "our
conservative estimate for Sodinokibi ransomware profits in 2020 is at
least $81 million." Besides, UNKN announced that among the most
profitable attack victims [the agriculture
sector](https://cutt.ly/rnE0RRY) is one of the best future targets.
This, of course, did not remain an empty promise.

## REvil’s modus operandi

UNKN noted that REvil’s developer team is [made up of less than ten
individuals](https://cutt.ly/rnE0RRY). The team is so small precisely
because they don’t perpetrate most of their attacks. Since they operate
as RaaS, most of their attacks "[are conducted by the affiliates or
adverts who disseminate the payload and navigate the victim’s
networks](https://cutt.ly/rnE0RRY)." They are the ones responsible for
infecting the systems of their victims with the virus that "[encrypts
files after infection and discards a ransom request
message](https://cutt.ly/XnE9rVV)."

REvil affiliates often apply "[mass-spread attacks using exploit-kits
and
phishing-campaigns](https://www.infradata.com/resources/what-is-revil-ransomware/)"
to distribute their malware. But the most commonly used attack vector,
according to UNKN, is [brute-force](../pass-cracking/) Remote Desktop
Protocol
([RDP](https://www.paubox.com/blog/what-is-remote-desktop-protocol-attack/)).
This is very efficient for criminals, because "[brute force attacks are
usually automated, so it doesn’t cost the attacker a lot of time or
energy](https://cutt.ly/dnE29W2)."

## A worldwide attack

JBS is headquartered in Brazil and [has facilities in 20
countries](https://cutt.ly/LnE200M), though fifty percent of its
"[overall revenue](https://cutt.ly/TnE3fHA)" corresponds to the United
States. Therefore, and given the multiple outsourcing processes of the
company, the attack made on JBS servers has required an international
effort to solve it. In particular, Andre Nogueira, Chief Executive
Officer of the Brazilian company, thanked the [joint work of the United
States, Canada, and Australia](https://cutt.ly/4nE2MNh).

Today, a cyberattack not only affects the company and its employees but
can become a global threat. This case is a magnificent example because
it [affected countries everywhere](https://cutt.ly/znE2Nd6): in North
America, South America, Oceania, and Europe. Everything happened
precisely when the pandemic hit the food sector the hardest. The Food
and Agriculture Organization of the United Nations (FAO) published its
[report on food
prices](http://www.fao.org/news/story/en/item/1403339/icode/) on
Tuesday, June 1. The bottom line is that in May food prices have
increased so rapidly that they have reached their highest peak since
September 2011. If we add to that a cyberattack that paralyzed the meat
production company for three days, then the outlook doesn’t seem very
encouraging for June (see Figure 3).

<div class="imgblock">

![FAO](https://res.cloudinary.com/fluid-attacks/image/upload/v1623159152/blog/jbs-revil-cyberattack/FAO_xitvis.webp)

<div class="title">

Figure 2. Graphic by [FAO](http://www.fao.org/worldfoodsituation/foodpricesindex/en/)

</div>

</div>

The attack was particularly worrying in Australia, where the Minister
for Agriculture, Drought, and Emergency Management said on [a local
radio station](https://cutt.ly/qnE2Vaa) that

> "**It’s a global attack**. And we’re working now with international
> partners around trying to trace and then rectify and obviously
> prosecute where possible, who has perpetrated this attack.”

It was the joint effort of different nations that allowed them to face
REvils’s attack. This was also made clear by the FBI in its statement on
the matter, in which they stated: "A cyberattack on one is an attack on
us all." And Russia’s Deputy Foreign Minister Sergei Ryabkov himself
backed the idea of working together with international peers by [stating
that](https://www.bbc.com/news/world-us-canada-57318965) "Biden
administration had been in contact with Moscow to discuss the
cyber-attack."

## How did the attack end?

Unlike the [Colonial Pipeline](../pipeline-ransomware-darkside/) case or
the victims of [Babuk locker](../babuk-locker/), JBS has not confirmed
the payment of the ransom. On [June 3](https://cutt.ly/znE2Z9A), the
company’s CEO said they returned to operation at normal capacity because
the attack did not affect either the central system or the backup data.
And with this, no information about customers, suppliers, or employees
was compromised.

Without doubting the company’s quick reaction, or the efficient
procedures carried out by the White House and the FBI, let me say that I
am still forming my opinion about this outcome. It would sound logical
to stick with the official version and not persist in doubt. However,
not since [REvil has not given any statement](https://cutt.ly/RnE2KMS)
on its [dark web](../dark-web/), and considering what [The Irish Times
has published](https://cutt.ly/nnE3jCJ) about it:

> "ransomware syndicates, as a rule, don’t post about attacks when they
> are in initial negotiations with victims — or if the victims have paid
> a ransom."

Let me leave the door open to whether JBS finally paid the ransom. It
would not be the only company that, without denying having paid the
ransom, resumes activities after an attack of this type (see
[Travelex](https://www.bbc.com/news/business-51017852) case).

At `Fluid Attacks` we are specialized in cybersecurity through
[Pentesting](../../solutions/penetration-testing/) and [Ethical
Hacking](../../solutions/ethical-hacking/).
For more information, don’t hesitate to [contact
us](../../contact-us/)\!
