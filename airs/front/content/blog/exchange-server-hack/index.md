---
slug: exchange-server-hack/
title: Microsoft Exchange Server Hack
date: 2021-03-12
subtitle: Hafnium exploits four zero-day vulnerabilities
category: attacks
tags: cybersecurity, software, vulnerability, hacking, application, discovery
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330870/blog/exchange-server-hack/cover_ep44jq.webp
alt: Photo by Alejandro Luengo on Unsplash
description: This post describes the Microsoft Exchange Server hack that
  has affected multiple companies and government agencies recently.
keywords: Microsoft Exchange Server, Software, Attack, Hafnium, Vulnerability,
  Update, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/jL0tMFYOdBM
---

The attention of global media, U.S. federal agencies, and other
organizations is partly shifting from one world power to another this
month. I mean, in the cybersecurity field, the Russians were in the
limelight with the [SolarWinds supply chain
attack](../solarwinds-attack/). Now, the Chinese have taken on the
central role. [Microsoft has attributed
attacks](https://www.microsoft.com/security/blog/2021/03/02/hafnium-targeting-exchange-servers/)
on its Exchange Server to a Chinese state-sponsored group. These
cybercriminals took advantage of four zero-day vulnerabilities in that
software and have exploited them to break into many organizations,
primarily in the United States. In this post, we will examine several
details that are known so far about this incident.

## What is Microsoft Exchange Server?

Microsoft Exchange Server (MES) is a ["software that
provides](https://services.dartmouth.edu/TDClient/1806/Portal/KB/ArticleDet?ID=64504)
the back end to an integrated system for email, calendaring, messaging,
and tasks." (Outlook, instead, is the app installed on your desktop
that, like other email clients, can be synchronized with MES and used to
send and receive emails.) This program is employed worldwide within
large organizations but also small and medium-sized companies.

It turns out that in early January of this year, the cybersecurity
company [Volexity started to
note](https://www.volexity.com/blog/2021/03/02/active-exploitation-of-microsoft-exchange-zero-day-vulnerabilities/)
abnormal activity in the MES servers of two of its clients. That
activity involved large quantities of data sent to IP addresses
apparently not linked to legitimate users. The Danish company [Dubex
also
reported](https://www.dubex.dk/aktuelt/nyheder/please-leave-an-exploit-after-the-beep)
part of the issue the same month. It was not until
[March 2](https://www.microsoft.com/security/blog/2021/03/02/hafnium-targeting-exchange-servers/)
that the situation became public: [Microsoft released
updates](https://techcommunity.microsoft.com/t5/exchange-team-blog/released-march-2021-exchange-server-security-updates/ba-p/2175901)
to remediate **four zero-day** (previously unknown) vulnerabilities
identified in its software.

## What were the alerts?

According to Microsoft, these flaws started to be exploited by a Chinese
state-sponsored APT (advanced persistent threat) group it dubbed
**Hafnium**. [Based on the
procedures](https://www.secureworldexpo.com/industry-news/microsoft-attacks-exchange-servers)
and strategies observed, Microsoft said it is a modern and skilled team
with a history of attacks against Office 365 users. Indeed, it is a
Chinese group but "primarily operates from leased virtual private
servers (VPS) in the United States," [said Tung in
ZDNet](https://www.zdnet.com/article/update-immediately-microsoft-rushes-out-patches-for-exchange-server-zero-day-attacks/).

These attackers could access users' mailboxes, extract content, and
install backdoors on compromised servers for persistent access and
control through such security flaws in the software. Their first
reported attacks impacted higher education and research institutions,
law firms, policy think tanks, defense contractors, and NGOs, mainly in
the United States. The situation looked thornier when the investigation
revealed attacks against the U.S. government agencies. Curiously, these
critical vulnerabilities' exploitation could affect servers running MES
2013, 2016, and 2019 (on-premises products) *but not* Exchange Online
(cloud-hosted service).

Microsoft began to publicly request all companies that were making use
of MES to apply the updates *as soon as possible*. At the same time, [it
reflected
concern](https://blogs.microsoft.com/on-the-issues/2021/03/02/new-nation-state-cyberattacks/)
that other malicious hacker groups beyond Hafnium could also quickly
target unpatched systems. ([It
seems](https://www.zdnet.com/article/everything-you-need-to-know-about-microsoft-exchange-server-hack/)
this has already happened.) On March 3, the U.S. Cybersecurity &
Infrastructure Security Agency (CISA) issued [an emergency
directive](https://cyber.dhs.gov/ed/21-02/) regarding the matter. It
asked all government agencies to comply with the installation of
patches, especially if there were no indicators of compromise in their
networks and systems. Otherwise, they should "disconnect their Microsoft
Exchange on-premises servers and report their findings to CISA for
further investigation," [said Osborne in
ZDNet](https://www.zdnet.com/article/cisa-issues-emergency-directive-to-agencies-deal-with-microsoft-exchange-bugs-now/).

The next day, [CISA updated the
alert](https://us-cert.cisa.gov/ncas/current-activity/2021/03/04/update-alert-mitigating-microsoft-exchange-server-vulnerabilities),
reporting they were "aware of threat actors using open source tools to
search for vulnerable \[MESs\]" and that agencies needed to look for
signs of suspicious behavior from at least September 1, 2020. Then, [on
March 6, CISA
recommended](https://us-cert.cisa.gov/ncas/current-activity/2021/03/06/microsoft-ioc-detection-tool-exchange-server-vulnerabilities)
that agencies urgently run the [script that Microsoft
released](https://github.com/microsoft/CSS-Exchange/tree/main/Security)
at that time to determine if their systems had been compromised. Around
those days, Chris Krebs, who was director of CISA until [Trump fired
him](https://www.cnbc.com/2020/11/17/trump-says-us-cybersecurity-chief-chris-krebs-has-been-terminated.html),
[posted on his Twitter
account](https://twitter.com/C_C_Krebs/status/1368004411545579525) an
intriguing question: "Is this a flex in the early days of the Biden
admin to test their resolve?" In fact, if we go to CNN Politics, we can
find a post titled: ["Biden administration
expected](https://edition.cnn.com/2021/03/06/politics/microsoft-hack-task-force/index.html)
to form \[a\] task force to deal with Microsoft hack linked to China."

<div class="imgblock">

![Photo by ) on
Unsplash.](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330870/blog/exchange-server-hack/four_cvecsh.webp)

<div class="title">

Figure 1. Photo by [Pineapple Supply Co.](https://unsplash.com/@pineapple)
on Unsplash.

</div>

</div>

## What are the four flaws?

The four MES zero-day vulnerabilities involved in this case are
officially tracked as
[CVE-2021-26855](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-26855),
[CVE-2021-26857](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-26857),
[CVE-2021-26858](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-26858),
and
[CVE-2021-27065](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-27065).
The discovery of the first one (also known as
[ProxyLogon](https://proxylogon.com/)) and the last one is attributed to
the researcher "Orange Tsai" of [Devcore](https://devco.re/en/about/), a
team of professionals who in October 2020 started reviewing MES
security.

- **CVE-2021-26855** (CVSS 9.1) is a Server-Side Request Forgery
  (SSRF) vulnerability that allows ["the attacker
  to](https://www.zdnet.com/article/update-immediately-microsoft-rushes-out-patches-for-exchange-server-zero-day-attacks/)
  send arbitrary HTTP requests and authenticate as the Exchange
  server."

- **CVE-2021-26857** (CVSS 7.8) "is an insecure deserialization
  vulnerability in the Unified Messaging service." It allows attackers
  to "run code as SYSTEM on the Exchange server," only if they combine
  it with another flaw or use stolen credentials.

- **CVE-2021-26858** (CVSS 7.8) and **CVE-2021-27065** (CVSS 7.8) are
  post-authentication arbitrary file write vulnerabilities. "If
  Hafnium could authenticate with the Exchange server, then they could
  use \[any of these vulnerabilities\] to write a file to any path on
  the server."

According to several sources, attackers can carry out attacks using one
or more of the above flaws. Therefore, they can write and deploy
backdoor 'web shells' on the servers and have a foothold to execute
further attacks. (Web shells are small, easy-to-use ["scripts that
provide](https://www.zdnet.com/article/update-immediately-microsoft-rushes-out-patches-for-exchange-server-zero-day-attacks/)
a basic interface for remote access to a compromised system.") These can
involve stealing credentials, installing malware ([Kaspersky
mentioned](https://securelist.com/zero-day-vulnerabilities-in-microsoft-exchange-server/101096/)
the high risks of ransomware), stealing full email inboxes, adding rogue
user accounts, among others.

## How worrying is the situation?

The incident with these vulnerabilities [seems to have no
connection](https://www.zdnet.com/article/everything-you-need-to-know-about-microsoft-exchange-server-hack/)
with the SolarWinds supply chain attack that has affected around 18,000
organizations worldwide. In this new indiscriminate attack, it appears
that the number of organizations impacted is approximately 30,000. More
recently, some authors have [even reported
**60**](https://www.bloomberg.com/news/articles/2021-03-07/hackers-breach-thousands-of-microsoft-customers-around-the-world).
In addition to the types of organizations previously mentioned as
victims are ["banks, credit
unions](https://krebsonsecurity.com/2021/03/at-least-30000-u-s-organizations-newly-hacked-via-holes-in-microsofts-email-software/),
non-profits, telecommunications providers, public utilities and police,
fire and rescue units."

It is currently quite worrying how slowly different companies and
government agencies are patching their systems. Some even consider that
there may be more severe results from this hack attributed to the
Chinese than from the one related to SolarWinds. As the cybersecurity
expert [Brian Krebs has
said](https://krebsonsecurity.com/2021/03/at-least-30000-u-s-organizations-newly-hacked-via-holes-in-microsofts-email-software/),
"By all accounts, rooting out these intruders is going to require an
unprecedented and urgent nationwide clean-up effort." But the longer it
takes everyone to remove the backdoors and update their systems, the
longer attackers will continue to prowl their networks and even expand
their access, reach, and damage.

Let’s keep the following in mind: [Last year,
Microsoft](https://www.zdnet.com/article/multiple-nation-state-groups-are-hacking-microsoft-exchange-servers/)
had already warned its MES customers to patch a different critical
vulnerability
([CVE-2020-0688](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2020-0688)).
Nevertheless, months after the first attacks, ["tens of
thousands"](https://www.zdnet.com/article/microsoft-exchange-zero-day-attacks-30000-servers-hit-already-says-report/)
of clients still had their systems not updated with the released patch.
["Microsoft is
concerned](https://www.zdnet.com/article/update-immediately-microsoft-rushes-out-patches-for-exchange-server-zero-day-attacks/)
it could see the same scenario play out again with this set of Exchange
server vulnerabilities." We will see what happens. For now, Microsoft
continues with investigations and offering guidance to its customers on
risk mitigation.
