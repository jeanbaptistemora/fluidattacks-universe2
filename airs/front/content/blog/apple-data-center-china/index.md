---
slug: apple-data-center-china/
title: All That Is Gold Does Not Glitter
date: 2021-06-11
subtitle: Tips for understanding the Apple–China controversy
category: politics
tags: policies, company, trends, information, technology, cloud
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1627389989/blog/apple-data-center-china/cover-apple-data-center-china_lihdpl.webp
alt: Photo by Elisabeth Pieringer on Unsplash
description: In this post, we will understand why the Apple data center
  inaugurated in Guizhou reopened the controversy over data privacy in China.
keywords: Data, Information, Vulnerability, Software, Apple,
  Ethical Hacking, China, Chinese, Pentesting
author: Felipe Zárate
writer: fzarate
name: Felipe Zárate
about1: Cybersecurity Editor
source: https://unsplash.com/photos/9paY25EHOBo
---

[On
May 25](https://appleinsider.com/articles/21/05/27/first-apple-data-center-in-china-officially-commences-operations),
**Apple** opened its first **Data Center (DC)** in the **province of
Guizhou**, southwest of China. This means that from now on, Apple
"[stores the personal data of its Chinese customers on computer servers
run by a state-owned Chinese
firm.](https://www.bangkokpost.com/tech/2117731/censorship-surveillance-and-profits-hard-bargain-for-apple-in-china)"
This has been very controversial given the calls of different
organizations and human rights defenders. As we will see, they report
that Chinese Apple users face potential abuses and intrusions into
privacy by the Chinese government. In this post, we explain why they say
so and what the controversy consists of.

## Hey China, think different!

This Apple-China project has been underway for more than three years, as
[in 2017, Apple signed a
$1B](https://news.cgtn.com/news/2021-05-27/Apple-s-China-data-center-starts-operation-10BTZQKlCWA/index.html)
agreement to build its first DC. Chinese employees are the ones who
[physically
control](https://www.nytimes.com/2021/05/17/technology/apple-china-censorship-data.html)
the computers. The Chinese government will store the digital keys used
"[to unlock the data
stored](https://www.datacenterdynamics.com/en/news/apples-chinese-data-centers-store-encryption-keys-in-same-facility-as-user-data/)."
According to a lengthy [New York Times (NYT)
report](https://www.nytimes.com/2021/05/17/technology/apple-china-censorship-data.html?smid=url-share),
such assignments would imply that "Apple abandoned the encryption
technology it used elsewhere after China would not allow it." In fact,
in their report, NYT insists that "China is making Apple work for the
Chinese government." Apple would be collaborating with censoring
thousands of applications "including foreign news outlets, gay dating
services, and encrypted messaging apps."

<div class="imgblock">

![Figure1](https://res.cloudinary.com/fluid-attacks/image/upload/v1623358302/blog/apple-data-center-china/figure1_tnwmxz.webp)

<div class="title">

Figure 1. Photo by [Marija Zaric](https://unsplash.com/photos/Vdz1YQgDQz8) on Unsplash

</div>

</div>

## What is the matter?

The same NYT report argues that it would be almost impossible to prevent
the [Chinese government from
having](https://www.nytimes.com/2021/05/17/technology/apple-china-censorship-data.html)
"access to the emails, photos, documents, contacts, and locations of
millions of Chinese residents." These signed agreements are coordinated
with the Personal Information Protection Law
([PIPL](https://www.newamerica.org/cybersecurity-initiative/digichina/blog/chinas-draft-personal-information-protection-law-full-translation/)).
[PIPL
regulates](https://www.newamerica.org/cybersecurity-initiative/digichina/blog/how-will-chinas-privacy-law-apply-to-the-chinese-state/)
"the collection, storage, use, processing, transmittal, provision, and
disclosure (collectively, ‘handling’) of personal information by
‘organizations and individuals’" in China.

The problem comes in determining what limits a government should have to
intervene in the storage and collection of information. The [Chinese
government’s
justification](https://www.business-humanrights.org/fr/derni%C3%A8res-actualit%C3%A9s/china-adopts-cyber-security-law-in-face-of-overseas-opposition/)
for intervening in privacy in this way is to protect itself from
"growing threats such as hacking and terrorism." Yet, the implementation
of these policies [is highly
intrusive](https://www.reuters.com/article/us-china-parliament-cyber-idUSKBN132049).
[Human Rights Watch
stated](https://www.hrw.org/news/2016/11/06/china-abusive-cybersecurity-law-set-be-passed)
in one of their latest communiqués that it was "a regressive measure
that strengthens censorship, surveillance, and other controls over the
Internet." But why does opening a DC in a country like China make all
this intervention possible?

The heart of the matter relies on **how data storage works** and whether
a government could access that information by having DC in its
territory.

## Data storage: bits and bytes

Storing digital information means saving a collection of **bits** and
**bytes**. A bit is a binary digit, [the minimum unit of data
measurement](https://www.redhat.com/sysadmin/bits-vs-bytes). All cyber
information is stored and transmitted in bits.
[Bytes](https://kb.iu.edu/d/ackw) are ordered sets of bits: exactly
eight bits (the reason they are eight and no more or fewer bits is more
historical than technical). Those bytes are the minimum unit of data
processed by a computer.

When those bits and bytes, digital information, are collected and
retained, we talk about [data
storage](https://www.redhat.com/en/topics/data-storage). For the storage
process, you need a physical repository or a [memory
cell](https://computer.howstuffworks.com/ram.htm). Physically a memory
cell is the junction of a transistor and a capacitor, but virtually it
represents a bit of data. [Data
Center](https://www.cpisolutions.com/blog/what-is-a-data-center/) (DC)
is a physical facility that stores countless memory cells, hardware
designed to store those bits.

Any company could have its own DC. However, managing and verifying good
maintenance of that equipment is often cumbersome. This is why it is
common for that service to be outsourced. Thus, DCs are usually managed
by specialized companies.

## iCloud

By outsourcing the DCs, companies store their data using cloud storage
(CS). CS is characterized by [the abstraction, pooling, and sharing of
storage resources through the
internet](https://www.redhat.com/en/topics/data-storage/what-is-cloud-storage).
It does not require a direct connection to the storage hardware. Thus,
one company can operate from Colombia, while the hardware that stores
its information remains in the United States. Because it is faster to
[retrieve and store data on a local CPU than over a
network](https://www.redhat.com/sysadmin/bits-vs-bytes), companies with
monetary, human, and technical resources usually have their own DC.
That’s the Apple case.

Apple manages its own DC and offers users its own CS system. Their DC is
called **iCloud**, and Apple manages its security. In this regard, Apple
maintains on its [privacy page](https://www.apple.com/privacy/features/)
that, for example, when a credit card is added or used as a payment
method, "a unique Device Account Number is created, which is encrypted
in a way that Apple can’t decrypt and stored in the Secure Element of
your device."

## Guizhou-Cloud Big Data

Apple can manage all its users’ information on its own servers, except
in China. Specifically, with the launch of its database in Guizhou,
[Apple
asked](https://www.bangkokpost.com/tech/2117731/censorship-surveillance-and-profits-hard-bargain-for-apple-in-china)
its Chinese customers "to accept new iCloud terms and conditions that
list GCBD (Guizhou-Cloud Big Data) as the service provider and Apple as
‘an additional party.’" That is, GCBD "governs your use of the iCloud
product, software, services, and websites."

The primary provider is "[a company owned by the provincial
government](https://global.chinadaily.com.cn/a/201806/07/WS5b1888fba31001b82571e9d1.html),"
in other words, the one in charge of managing Apple users' information
is the Chinese government itself. That same government "[requires
network operators to store select data within China and allows Chinese
authorities to conduct spot-checks on a company’s network
operations](https://thediplomat.com/2017/06/chinas-cybersecurity-law-what-you-need-to-know/)."

## Privacy risk and Apple response

What is worrying is how that information will be managed. In 2016 it was
announced the adoption of the Personal Information Protection Law of the
People’s Republic of China (read the [translation
here](https://www.newamerica.org/cybersecurity-initiative/digichina/blog/chinas-draft-personal-information-protection-law-full-translation/)).
In the face of this type of measure, several rights advocates have
spoken out against it.

Apple’s Chief Executive, Tim Cook, has repeatedly said the [data is
safe](https://www.bangkokpost.com/tech/2117731/censorship-surveillance-and-profits-hard-bargain-for-apple-in-china).
In addition, the company is aware that there are rules that generate
discomfort to the international community and to the company’s own
interests. Still, [Apple
said](https://www.nytimes.com/2017/07/12/business/apple-china-data-center-cybersecurity.html):
"we believe in engaging with governments even when we disagree." At the
beginning of the negotiations with China, Apple [justified the opening
of that
DC](https://www.nytimes.com/2017/07/12/business/apple-china-data-center-cybersecurity.html)
by saying that its construction "will allow us to improve the speed and
reliability of our products and services while also complying with newly
passed regulations."

<div class="imgblock">

![Figure2](https://res.cloudinary.com/fluid-attacks/image/upload/v1623358298/blog/apple-data-center-china/figure2_pmmnob.webp)

<div class="title">

Figure 2. Source: [The New York
Times](https://www.nytimes.com/2020/08/19/technology/apple-2-trillion.html)

</div>

</div>

When considering the economic factor that Apple’s entry into the Asian
giant has represented, the reasons for its pact seem more
straightforward. Following its agreement with China, the country has
accounted for [15% of Apple’s
revenue](https://www.bbc.com/news/business-57395094). That percentage
translates into a bizarre figure when you consider that it is the only
company in the world with a turnover higher [than $2 trillion in
2020](https://www.nytimes.com/2020/08/19/technology/apple-2-trillion.html).
This has made it the company with the highest revenue globally, well
above Google, Microsoft, Amazon, and Facebook, who are vying for the top
5 [according to
Forbes](https://www.forbes.com/the-worlds-most-valuable-brands/#67d38cd7119c).

The controversy can be summed up in Apple’s recognition that its profits
have skyrocketed like never before, thanks to its entry into China.
China has found Apple a great ally in "protecting" its citizens from the
*dangerous cyber world*. While other companies see China’s requests as a
translation of the old saying, **"you shall not pass\!"** Apple
interpreted it as a possibility to strengthen its finances. Only time
will tell us how good the decision was.

We hope you have enjoyed this post\!
At `Fluid Attacks` we look forward to hearing from you.
[Contact us\!](../../contact-us/)
