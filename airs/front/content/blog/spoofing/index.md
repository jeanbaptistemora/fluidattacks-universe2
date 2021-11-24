---
slug: spoofing/
title: Spoofing, Pokémon & Vulnerability
date: 2021-05-12
subtitle: Why may the fun of some be the danger of others?
category: attacks
tags: cybersecurity, social-engineering, mistake, risk, technology, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620857985/blog/spoofing/cover_tpi466.webp
alt: Photo by Lia Panidara on Unsplash
description: Last April, if you googled for "spoofing," you could find the word
  Pokémon in the top trends. Here's what that has to do with your company's
  vulnerabilities.
keywords: Spoofing, Vulnerability, Software, Cybersecurity, Social Engineering,
  Ethical Hacking, GPS, Pentesting
author: Felipe Zárate
writer: fzarate
name: Felipe Zárate
about1: Cybersecurity Editor
source: https://unsplash.com/photos/xKRv2abDDeg
---

[Spoofing](https://docs.fluidattacks.com/criteria/vulnerabilities/032)
is not the name of any Pokémon (although it might be), but that of a
type of scam. Over the past year, it accounted for more than $216M in
losses in the United States (according to the [FBI
report](https://www.ic3.gov/Media/PDF/AnnualReport/2020_IC3Report.pdf)).
Through an email, phone call, or text message, criminals pretend to be a
reliable source to deceive their victims (see Figure 1).

<div class="imgblock">

![Figure 1](https://res.cloudinary.com/fluid-attacks/image/upload/v1620857980/blog/spoofing/image1_fz39dc.webp)

<div class="title">

Figure 1. [2020 Crime Types by Victim
Loss](https://www.ic3.gov/Media/PDF/AnnualReport/2020_IC3Report.pdf)

</div>

</div>

**Spoofing** has almost a ninth of the victims that
[phishing/vishing/smishing/pharming](../smishing/) have (see Figure 2).
In this regard, spoofing is very dangerous because of the amount of
money stolen in a single transaction and not due to the number of
victims fallen in this ruse. In January of this year, [Washington State
reported](https://www.justice.gov/usao-wdwa/pr/us-attorney-s-office-warns-scammers-are-spoofing-office-phone-number-try-obtain-money)
$777,045 in losses related to this scam. A few days ago in New York
City, the finance department of a clinical trial software firm
[transferred to a criminal account
$4.8M](https://www.forbes.com/sites/tmobile/2021/04/26/what-your-business-should-know-about-email-spoofing/?sh=68afa5e844ed)
due to a spoofed email.

A criminal [could imitate an
email](https://www.investopedia.com/terms/s/spoofing.asp) with the
sender’s name from a forged IP address. Thanks to it, criminals can send
a link to re-addresses a page with a counterfeit **Domain Name System
(DNS)**. [Criminals use to
do](https://www.winknews.com/2021/04/29/scammers-are-stealing-info-of-floridians-whove-claimed-unemployment/)
a two-verification trick and favor that email using phone calls or SMSs
addressed to the company’s financial teams. Financial institutions,
banks, commercial companies, and government entities are the main
targets of this type of deception.

<div class="imgblock">

![Figure 2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620857980/blog/spoofing/image2_vrkc3e.webp)

<div class="title">

Figure 2. [2020 Crime Types by Victim
Count](https://www.ic3.gov/Media/PDF/AnnualReport/2020_IC3Report.pdf)

</div>

</div>

## How does [spoofing](https://terranovasecurity.com/what-is-spoofing/) work?

### ARP-MAC-IP combo

This combo is the perfect trick to divert resources, money, information,
and data. To do this, criminals supplant a set of internet protocols,
that is to say, both the transmitter and the receiver of data between
the connected computers. Think, for example, that you want to send a
gift to a friend who lives far away. For that, you decide that the best
way is to trust a Courier. In this case, both your address and your
friend’s address would be two **Internet Protocol (IP)** addresses. The
[**Address Resolution Protocol
(ARP)**](https://docs.fluidattacks.com/criteria/vulnerabilities/077)
would be the path that the Courier has to travel to send the package.
And the **Media Access Control (MAC)** address would be each one’s ID
number. In this example, the spoofing combo would be like this: a
cybercriminal fakes the ARP (the path) of a local area network that
routes traffic on the web in a different direction. Then, by falsifying
the MAC (your friend ID) address and falsifying the IPs (your friend’s
address), criminals could disguise a device as if it were enrolled in
the target network. By doing so, traditional restriction mechanisms are
not asked to access. From there, all the information could be redirected
to the criminal’s computer. Still, the boldest criminals do not keep all
that information but distort it and send it to the genuine recipient.

### DNS-Website combo

Criminals who know the
[DNS](https://docs.fluidattacks.com/criteria/vulnerabilities/084/) can
assign domains to previously forged IPs. When people access a web page
using standard URLs (Uniform Resource Locators), criminals can store
caches of those DNS for their convenient sides. Once that process is
performed, the victim enters, without notice, into a malicious replica
of the desired domain. Furthermore, that replica is usually updated
according to the original website changes, making it challenging to
identify the farce.

### Email-Phone-SMS combo

This combo may be the one that requires minor work from the criminals'
side. First, they imitate a mail header by changing the mail sender to
look like a legitimate source from the victims' perspective. Then they
send an email with the appearance of being official. In it, they require
victims to make a payment or transaction to an account. Next, a caller
identification is forged to impersonate the person or company from which
the mail was allegedly sent to rectify the email info. If that is not
enough, criminals can use a forgery SMS (short message service) to
double-check what was said by mail. At the same time, they send a false
notification to confirm that the alleged recipient of the transaction
received the money or that the supposedly due invoice was paid.

### GPS

If a criminal could alter geolocation services, he could use them to
disrupt transportation apps used by individuals or companies to guide
their trips. The problem, of course, would be more linked to sabotage
than anything else. Criminals could, for example, cause a person to
reach an unexpected place by resetting the app GPS or send them on
routes that have traffic or road obstacles. Anyway, this type of
spoofing is much more dangerous when used as an extra ingredient in one
of the above combos.

### How can we deal with such scams?

Of course, the best way not to fall into such scams is to be alert to
emails, calls, and SMS. However, prevention will always have better
results than corrective actions. In this case, prevention could include
shielding emails from suspicious accounts. For example, [companies can
add](https://www.forbes.com/sites/tmobile/2021/04/26/what-your-business-should-know-about-email-spoofing/?sh=68afa5e844ed)
"Domain Key Identified Mail (DKIM), Domain-based Message Authentication,
Reporting and Conformance (DMARC), and Sender Policy Framework (SPF)
records to their business’s domain name record." If your company makes
these small changes, it will not regret it, as it will send all
suspicious emails to the junk folder. Once a scam is discovered, it must
be reported. Those who live in the United States and have been scammed
while working in a company can file their complaints on the [Federal
Communications Commission](https://consumercomplaints.fcc.gov/hc/en-us)
official website. They can also go to the [Crime Complaint
Center](https://www.ic3.gov/Home/ComplaintChoice) website or find out
more info [FBI’s
page](https://www.fbi.gov/scams-and-safety/on-the-internet) for this
purpose.

Now, I bet that you’ve heard about **Pikachu**, **Ash Ketchum**, or
**Pokémon**. However, I also bet that you don’t know what links one of
the [most valued franchises in the
world](https://www.gamesindustry.biz/articles/2021-03-02-gotta-cash-em-all-how-pok-mon-became-the-worlds-biggest-games-franchise#:~:text=Quantifying%20Pok%C3%A9mon’s%20success%20is%20tricky,website%20a%20few%20years%20back)
with spoofing. So, to understand it, we have to talk a bit about
Pokémon.

One of the latest hits of this franchise was their collaborative success
with the enterprise Niantic when they decided to launch Pokémon Go. The
goal of this game is to catch Pokémon in real places. So, players must
go outside their houses to catch them all. But recently, with COVID-19
confinements, people have resorted to other ways of walking around the
globe: [altering their GPS
systems](https://www.republicworld.com/technology-news/gaming/how-to-play-pokemon-go-without-moving-learn-about-it-in-this-guide.html).
In other words, players trick the app into believing that they have
somewhere else to make Pokémon appear so that they can catch them.
Seemingly, many people are interested in such uses. So, they’ve googled
how the Pokémon Go app can be spoofed to catch Pokémon. Therefore, those
two words (spoofing and Pokémon) have been linked since 2020 in
search-trading websites (see Figure 3). That’s why we say that each
other’s fun is the danger of others. In seeking to innocently catch more
Pokémon, spoofing has become more popular. In turn, this makes more
people use this type of cyberattack technique, making companies more
vulnerable to being attacked.

<div class="imgblock">

![Figure 3](https://res.cloudinary.com/fluid-attacks/image/upload/v1620857979/blog/spoofing/google_ztrfjg.webp)

<div class="title">

Figure 3. Screenshot [taken in
May 12, 2021](https://trends.google.com/trends/explore?q=spoofing&geo=US)
on Google Trends

</div>

</div>

At `Fluid Attacks` we are specialized in cybersecurity through
[Pentesting](../../solutions/penetration-testing/) and [ethical
hacking](../../solutions/ethical-hacking/). For more information, don’t
hesitate to [contact us\!](../../contact-us/)
