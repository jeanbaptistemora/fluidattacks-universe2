---
slug: solarwinds-attack/
title: SolarWinds Supply Chain Attack
date: 2021-01-21
subtitle: A concise summary of the SolarWinds security fiasco
category: attacks
tags: cybersecurity, software, vulnerability, hacking, application, discovery
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331098/blog/solarwinds-attack/cover_bvibqb.webp
alt: Photo by Daniel Joshua on Unsplash
description: This post outlines the SolarWinds supply chain attack that
  has affected multiple companies and federal agencies in recent months.
keywords: Malware, SolarWinds, Supply Chain Attack, Network, Update,
  Cybersecurity, Hacking, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/p3CqjxHAJJs
---

[**SolarWinds**](https://en.wikipedia.org/wiki/SolarWinds), an American
software company with nearly **300,000** clients, including almost all
*Fortune 500* companies and multiple federal agencies, received a
critical, remarkable and surreptitious cyberattack. Incredibly, it was
detected only in mid-December 2020, several months after its start. I’m
referring to a 'supply chain attack' which, by its nature, still causes
trouble nowadays. Let’s summarize what has happened so far.

SolarWinds is a company focused on developing software for organizations
to help manage their systems, networks, and infrastructure. Among its
clients are the US Treasury and Commerce departments, which, as reported
in
[Reuters](https://www.reuters.com/article/us-usa-cyber-amazon-com-exclsuive-idUSKBN28N0PG)
on **December 13**, had been victims of internal email traffic
monitoring by, apparently, a group of Russian hackers. Some people
involved then said that that event was related to the hack reported a
few days ago by [FireEye](https://www.fireeye.com/), a worldwide
distinguished cybersecurity company.

[FireEye
emphasized](https://www.zdnet.com/article/fireeye-one-of-the-worlds-largest-security-firms-discloses-security-breach/)
a 'highly sophisticated' attack where the actors accessed their internal
network, looked for data about their government clients, and even stole
some of their pentesting tools. It was striking that they talked about
observing a novel combination of techniques in this attack. Some sources
associated it with the group **APT29** or [**Cozy
Bear**](https://en.wikipedia.org/wiki/Cozy_Bear), linked to the Russian
Foreign Intelligence Service (SVR). However, FireEye preferred to be
neutral and used the codename **UNC2452**. An official investigation by
[CISA](https://www.cisa.gov/) and the FBI began because some individuals
affected were seeing this whole incident as a cyberespionage campaign.

All of this was part of the sizable SolarWinds breach, which seemed to
have started several months ago. [The deployment of a malware-laced
update](https://www.zdnet.com/article/microsoft-fireeye-confirm-solarwinds-supply-chain-attack/)
of the software [**Orion**](https://www.solarwinds.com/solutions/orion)
(SolarWinds' platform for monitoring and managing enterprise networks)
had infected many companies and government agencies' systems and
networks. It corresponded to a 'supply chain attack,' where hackers hide
a malicious code within a legitimate software update provided to the
target by a third party. This kind of attack takes advantage of trust
relationships, in this case, specifically the communication between
machines for the software updating mechanism that users typically
perceive as reliable. [SolarWinds confirmed
that](https://www.zdnet.com/article/microsoft-fireeye-confirm-solarwinds-supply-chain-attack/)
Orion update versions **2019.4** through **2020.2.1**, released in the
first half of 2020, had been contaminated with a malware that FireEye
called 'Sunburst' and Microsoft 'Solorigate.' Then, as a corrective
measure, SolarWinds proposed to have ready by **December 15** the new
update **2020.2.1 HF2** as a replacement with security improvements.

At that time, it was known that
*SolarWinds.Orion.Core.BusinessLayer.dll* was the Orion plug-in that
hackers modified and distributed with the updates. [It was digitally
signed](https://www.csoonline.com/article/3601508/solarwinds-supply-chain-attack-explained-why-organizations-were-not-prepared.html)
and had a backdoor for communication with third-party servers managed by
them. After a few weeks of inactivity, it executed commands that enabled
the use and transfer of files, the disabling of services, as well as
other operations on the system. [Attackers
knew](https://www.csoonline.com/article/3601508/solarwinds-supply-chain-attack-explained-why-organizations-were-not-prepared.html)
how to avoid detection properly. Inside the target system, they made
modifications to legitimate utilities with their malware, executed them,
and then returned them to their normal state.

Later, on **December 17**, [Microsoft
reported](https://blogs.microsoft.com/on-the-issues/2020/12/17/cyberattacks-cybersecurity-solarwinds-fireeye/)
they had distinguished more than **40** of their clients (**80%** of
these companies located in the US) with Orion’s infected versions and
intrusions of second-stage payloads to escalate attacks. Besides, they
admitted that they were among the victims and that the attack was
open-ended, although it was already public and different organizations
had taken various protection measures. On the other hand, [SolarWinds
acknowledged](https://www.zdnet.com/article/microsoft-says-it-identified-40-victims-of-the-solarwinds-hack/)
to the [SEC](https://www.sec.gov/) that approximately **18,000** of its
customers (government and private networks) had installed the
'trojanized' Orion updates.

[On **December
21**](https://www.zdnet.com/article/a-second-hacking-group-has-targeted-solarwinds-systems/),
security researchers discovered a second actor threatening SolarWinds
with 'Supernova' and 'CosmicGale' malware. Presumably, it was unrelated
to Sunburst’s Russian hackers because of its unsophisticated methods.
Also, at that time, the next step in escalation after Sunburst’s
activity became clearer. As [Cimpanu for ZDNet
said](https://www.zdnet.com/article/a-second-hacking-group-has-targeted-solarwinds-systems/),
"On infected networks, the malware would ping its creators and then
download a second stage-phase backdoor trojan named Teardrop that
allowed attackers to start a hands-on-keyboard session \[or\]
human-operated attack." The spying powers of hackers were thus expanded,
and they could even impersonate legitimate accounts. Regarding their
case, [Microsoft
said](https://msrc-blog.microsoft.com/2020/12/31/microsoft-internal-solorigate-investigation-update/)
that hackers were even able to see, but 'not modify,' part of their
source code. Well, this occurrence certainly gave us plenty to ponder
over.

[By **December
24**](https://www.businessinsider.com/solarwinds-hack-explained-government-agencies-cyber-security-2020-12),
the media mentioned prominent victims in three groups: (1) US agencies,
like the Pentagon, the State Department, and the National Nuclear
Security Administration, (2) companies, such as Cisco and Intel, and (3)
other organizations, like Kent State University. Days later, at the
beginning of 2021, [the media
reported](https://www.theverge.com/2021/1/2/22210667/solarwinds-hack-worse-government-microsoft-cybersecurity)
**250** federal agencies and businesses affected, and the list keeps
growing. Data, users, passwords, and source code are the elements to
which agents involved may be having access.

<div class="imgblock">

![SpiderSun](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331098/blog/solarwinds-attack/spidersun_o69dv8.webp)

<div class="title">

Figure 1. Photo by Duncan Sanchez on
[Unsplash](https://unsplash.com/photos/QnT6nCctSz0).

</div>

</div>

[Vaughan-Nichols for
ZDNet](https://www.zdnet.com/article/solarwinds-the-more-we-learn-the-worse-it-looks/)
was right on the button when he said, "While you’ve been distracted by
the holidays, coronavirus, and politics, the more we learn about the
SolarWinds security fiasco, the worse it looks." He didn’t mince his
words, further suggesting, instead of an enhanced Orion update, to dump
that software promptly and investigate "the SolarWinds' mediocre
security record."

[On **January
5**](https://www.zdnet.com/article/us-government-formally-blames-russia-for-solarwinds-hack/),
a [joint
statement](https://www.cisa.gov/news/2021/01/05/joint-statement-federal-bureau-investigation-fbi-cybersecurity-and-infrastructure)
from the FBI, CISA, ODNI, and NSA officially ascribed the threat
(labeled "an intelligence gathering effort") to an author "likely
Russian in origin." [The next
day](https://www.zdnet.com/article/solarwinds-fallout-doj-says-hackers-accessed-its-microsoft-o365-email-server/),
the [US Department of Justice
confirmed](https://www.justice.gov/opa/pr/department-justice-statement-solarwinds-update)
that the hackers involved in this case had access to some of its
employees' email accounts. [On **January
8**](https://www.zdnet.com/article/cisa-solarwinds-hackers-also-used-password-guessing-to-breach-targets/),
as another curious fact, CISA said these hackers also used [brute
force](../pass-cracking/) attacks to breach targets, not always relying
on the trojanized update as the first attack vector.

[The following
week](https://www.zdnet.com/article/third-malware-strain-discovered-in-solarwinds-supply-chain-attack/),
CrowdStrike detected a third malware strain, named 'Sunspot.'
Surprisingly, this was the first malware used by malicious hackers in
this supply chain attack, back in September 2019 (the time when their
tests began). So —adding more details to the process—, Sunspot was
installed on the build server to watch it for build commands that
assembled Orion. Then, it replaced source code files inside the app to
make way for Sunburst’s injection and the subsequent collection of data
from internal networks. Depending on the importance of the target, the
attackers decided whether to proceed using the robust Teardrop.

Moreover, [on **January
19**](https://www.zdnet.com/article/fourth-malware-strain-discovered-in-solarwinds-incident/),
Symantec reported a fourth malware called 'Raindrop' (similar to
Teardrop), which appeared in the last stages of intrusion into exclusive
networks. Undeniably, this SolarWinds issue doesn’t end here. And
[senior writers like
Constantin](https://www.csoonline.com/article/3601508/solarwinds-supply-chain-attack-explained-why-organizations-were-not-prepared.html)
warn of a possible increase in the number of software supply chain
attacks. In this advanced digital age, it seems that many organizations
hadn’t paid heed to this as a threat model.

[Investigations and
countermeasures](https://www.zdnet.com/article/fireeye-releases-tool-for-auditing-networks-for-techniques-used-by-solarwinds-hackers/)
continue in several organizations; even the incoming Biden government in
the US is [already committed
to](https://www.csoonline.com/article/3603519/solarwinds-hack-is-quickly-reshaping-congress-s-cybersecurity-agenda.html)
making cybersecurity a top priority and investing in a "Rescue Plan."
Beyond this extraordinary impact on systems and networks, confidence in
cybersecurity has been widely affected without any doubt. In the midst
of so much uncertainty about what lies ahead, the only thing that is
clear for now is that much effort will be required to revitalize such
confidence.

Do you know about the [`Fluid Attacks`
service](../../services/continuous-hacking/) for comprehensive testing
of your systems' cybersecurity? [Get in touch with our
team\!](../../contact-us/)
