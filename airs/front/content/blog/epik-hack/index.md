---
slug: epik-hack/
title: A Breach of Epic Proportions
date: 2021-09-24
subtitle: Anonymous leaks Epik's database of 15M accounts
category: attacks
tags: cybersecurity, vulnerability, flaw, hacking, company, information
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1632518994/blog/epik-hack/cover_epik.webp
alt: Photo by Meriç Dağlı on Unsplash
description: Find out about the recent hack that has compromised the personal
  information of millions of website owners, many of which were
  not even the victim's customers.
keywords: Epik, Anonymous, Information, Cyberattack, Breach, Leak, Whois,
  Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/hAxoLhVMC2A
---

"Who is Epik?" Many website owners have been wondering since they got a
notification last week from the data breach tracking service
[HaveIBeenPwned](https://haveibeenpwned.com/) (HIBP). What happened was
that Epik’s massive database containing very detailed information linked
to millions of accounts had been leaked. Strikingly, not everyone
affected had any relation with Epik.

Let’s look at the details.

## Operation EPIK FAIL successful

First off, [Epik](https://www.epik.com/) is an organization that
provides [domain name
registration](https://encyclopedia2.thefreedictionary.com/Domain+registrar)
and [web
hosting](https://dictionary.cambridge.org/us/dictionary/english/web-hosting).
This means that they are one of the places other companies go to in
order to register a unique domain name on the Internet and that they may
keep and manage these companies' websites on a server. On September
13th, independent journalist Steven Monacelli tweeted a [press
release](https://twitter.com/stevanzetti/status/1437482759241469958) by
Anonymous that was posted on a website dedicated to what they called
"[Operation EPIK FAIL](https://archive.is/Czuu2)." Anonymous claimed
that they were able to obtain a "decade’s worth of data from the
company."

On September 14th, when interrogated by [The
Record](https://therecord.media/anonymous-hacks-and-leaks-data-from-domain-registrar-epik/),
among others, Epik’s spokesperson said that they were "not aware of any
breach." The following day, however, the company finally
[tweeted](https://twitter.com/EpikDotCom/status/1439020408783654917),
confirming that it had been hacked. That day, users got a [vague
email](https://www.dailydot.com/debug/epik-hack-far-right-sites-anonymous/)
from the CEO acknowledging a "security incident."

<div class="imgblock">

![Epik Figure 1](https://res.cloudinary.com/fluid-attacks/image/upload/v1632518994/blog/epik-hack/epik_figure_1.webp)

<div class="title">

Figure 1. [Tweet](https://twitter.com/EpikDotCom/status/1439020408783654917)
by Epik acknowledging the hack.

</div>

</div>

Now, why did Anonymous target Epik? The evidence shows that the
hacktivist group had been motivated due to the fact that Epik has been
hosting websites where
[hate-fueled](https://www.splcenter.org/hatewatch/2019/01/11/problem-epik-proportions)
content thrives, some of which [had been
deplatformed](https://arstechnica.com/tech-policy/2021/09/texas-abortion-snitch-website-kicked-off-godaddy-for-invading-peoples-privacy/?itm_source=parsely-api)
by other mainstream hosts. As evidenced by investigative reporter
Michael Edison Hayden, Epik’s reputation has to do, in part, with its
founder and CEO Robert Monster rubbing elbows with controversial
figures. Some of Epik’s [controversial
clients](https://arstechnica.com/information-technology/2021/09/epik-data-breach-impacts-15-million-users-including-non-customers/)
have included the Republican Party of Texas, Parler, Gab and 8chan.

According to the description of the hack, Anonymous leaked [180
gigabytes](https://ddosecrets.com/wiki/Epik) of data, including account
credentials, domain purchases and payment history. In the
[notice](https://twitter.com/svpndotcom/status/1439456727133474818) sent
to its users, Epik told them to look out for "unusual activity"
involving their "credit card numbers, registered names, user names,
emails, and passwords." The admin of a [Twitter
account](https://twitter.com/epikfailsnippet) dedicated to the hack
[asserted](https://twitter.com/epikfailsnippet/status/1440579325447659526)
that the leaked database is global, containing information of users from
various countries, not only from the US. This tweet also informed that
the website owners' physical addresses and phone numbers were among the
leaked data. How much more specific could it be?

A compressed version of the torrent used to download Epik’s database was
made [readily available](https://ddosecrets.com/wiki/Epik) to everyone.
The Daily Dot downloaded the data and
[contacted](https://www.dailydot.com/debug/epik-hack-far-right-sites-anonymous/)
several individuals listed as running various controversial websites.
They confirmed that the information listed in the breach was accurate.
The Daily Dot also talked to an engineer who conducted an impact
assessment for one of Epik’s users. He said that "with all the data in
the leak \[…​\] any attacker could easily take over the websites of
countless Epik customers."

## WHOIS compromised?

The official information about the breach [posted in
HIBP](https://haveibeenpwned.com/PwnedWebsites) indicates that more than
15M accounts were compromised. We mentioned that many people who are not
Epik’s clients were pwned too. Even HIBP founder, Troy Hunt,
[tweeted](https://twitter.com/troyhunt/status/1439705567400894464) that
he is among the people whose information was leaked. He researched the
situation and concluded that Epik had been
[data-scraping](https://www.targetinternet.com/what-is-data-scraping-and-how-can-you-use-it/),
that is, extracting and harvesting information from people and
organizations who own website domains, even those who are not its
customers. Troy
[informed](https://twitter.com/troyhunt/status/1439007532287082496) that
Epik scraped this information from the global database of domain holders
called [WHOIS directory](https://who.is/). This is a public directory,
meaning the information held there is searchable and available for all
to see, in case there’s any need to contact a domain owner.

<div class="imgblock">

![Epik Figure 2](https://res.cloudinary.com/fluid-attacks/image/upload/v1632518993/blog/epik-hack/epik_figure_2.webp)

<div class="title">

Figure 2. [Tweet](https://twitter.com/troyhunt/status/1439705567400894464)
by Troy Hunt, founder of HaveIBeenPwned.

</div>

</div>

But if WHOIS records can be seen and scraped by anyone, then why are
people who were not Epik’s customers so preoccupied?
[Reportedly](https://arstechnica.com/information-technology/2021/09/epik-data-breach-impacts-15-million-users-including-non-customers/),
these people are concerned that they could be falsely linked with Epik’s
controversial background. We would also argue that malicious hackers may
use the leaked information to try to scam website owners through [social
engineering tactics](../social-engineering/).

Another issue is why they were scraping all these data in the first
place. The possibility [has been
suggested](https://www.itworldcanada.com/article/cyber-security-today-sept-22-2021-epik-breach-has-epic-ramifications-misconfigurations-by-eventbuilder-users-and-phishing-attacks-on-the-aviation-sector/458810)
that Epik saw the database as a source of potential customers and wanted
to pitch them for business. Epik also appeared to be holding on to this
database for a long time. Ars Technica [took a
look](https://arstechnica.com/information-technology/2021/09/epik-data-breach-impacts-15-million-users-including-non-customers/)
at the data and they "noticed WHOIS records for some domains were dated
and contained incorrect information about domain owners—people who no
longer own these assets." It’s not the first time that breaches show
that some organizations hold on to the personal information of
unsuspecting individuals. There was the case of Apollo, a data
aggregator and analytics service. As [reported by
WIRED](https://www.wired.com/story/apollo-breach-linkedin-salesforce-data/),
security researcher Vinny Troia discovered that Apollo contained more
than 200M contact listings at the time of its data leak in summer 2018.
Furthermore, Hunt said about this breach that more than 100M people had
their data leaked and they didn’t even know about Apollo’s existence.

## Could it have been prevented?

According to
[TechCrunch](https://techcrunch.com/2021/09/17/epik-website-bug-hacked/),
security researcher Corben Leo had warned Epik about a security
vulnerability as early as January. Monster acknowledged that he received
the warning message, but he didn’t tell whether or not he acted on it.
Apparently, Anonymous could have actually hacked Epik months ago, in
February, as suggested by the date of the most recent files in the
leaked database.

These final pieces of information remind us of the importance of
watching out for vulnerabilities to prevent data breaches. We at `Fluid
Attacks` use comprehensive [Continuous
Hacking](../../services/continuous-hacking/) to detect your systems'
vulnerabilities before someone else does. [Contact
us](../../contact-us/)\!
