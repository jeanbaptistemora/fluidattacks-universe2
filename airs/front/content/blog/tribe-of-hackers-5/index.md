---
slug: tribe-of-hackers-5/
title: Tribe of Hackers Red Team 5.0
date: 2021-03-31
subtitle: Learning from the red team expert Carlos Perez
category: opinions
tags: cybersecurity, red-team, hacking, pentesting, ethical-hacking, blue-team
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331133/blog/tribe-of-hackers-5/cover_lgtcjo.webp
alt: Photo by Jonathan Petersson on Unsplash
description: This post is based on the book 'Tribe of Hackers Red Team'
  by Carey and Jin. Here we share content from the interview with Carlos Perez.
keywords: Cybersecurity, Red Team, Hacking, Pentesting, Ethical Hacking,
  Blue Team, Knowledge, Tribe
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/gQhWMkYh3Yc
---

This post is the fifth in a series based on the book [Tribe of Hackers
Red
Team](https://www.amazon.com/Tribe-Hackers-Red-Team-Cybersecurity/dp/1119643325)
by Carey and Jin (2019). As I mentioned [in the first
entry](../tribe-of-hackers-1/), in this book, we find the answers of 47
red teaming experts to the same 21 questions. In the previous posts, I
referred to the opinions of [(1.0) Carey](../tribe-of-hackers-1/),
[(2.0) Donnelly](../tribe-of-hackers-2/), [(3.0)
Weidman](../tribe-of-hackers-3/), and [(4.0)
Secor](../tribe-of-hackers-4/). For this occasion, I decided to focus on
the answers of Carlos Perez
([Darkoperator](https://twitter.com/carlos_perez?lang=en)), the first
Latin American included in the series, who has been active in
cybersecurity for more than twenty years.

Carlos worked for the government of Puerto Rico, performing pentesting
and helping to secure their networks. Later, he joined Compaq/HP "as a
senior solution architect for the security and networking consulting
practices" for clients in South and Central America and the Caribbean.
He also worked at Tenable as director of reverse engineering and, at the
time of the book’s interview, was the practice leader for research at
TrustedSec. Currently, Carlos is known for his contributions to open
source security tools such as
[DNSRecon](https://github.com/darkoperator/dnsrecon) and
[Metasploit](https://github.com/darkoperator/Metasploit-Plugins).

## For those hoping to be eager beavers on red teams

Carlos begins by recommending specific knowledge, divided into technical
and non-technical, which he believes is necessary for those who want to
be part of a red team. **On the technical side**, he starts with "A
solid base in programming logic," an essential knowledge for the proper
adaptation to diverse scripting languages as well as for the production
and alteration of tools. Then, Carlos suggests a good understanding of
networks because, he says, most actions will cross this type of
environment. Besides, "You will need to understand how systems are
configured, maintained, and secured." And you should keep a method of
constant practice and learning, always aiming to avoid any technical
bias.

**On the non-technical side**, Carlos begins by emphasizing the
significance of knowledge about an organization’s structures,
communication, and teamwork. Precisely, regarding the act of expressing
ideas, he recognizes that many in the field are introverts. However,
without mincing words, Carlos warns: "if you are not able to convey the
risks, mitigation, and supporting information in a manner that
decision-makers can use and comprehend, then you have failed." Finally,
he adds the importance of learning about new trends and best practices
in the IT industry (sometimes ignored by practitioners), for example,
Cloud and DevOps.

Like other experts whose views have been presented in this series,
Carlos reminds us that it is unnecessary to engage in illegal activities
to gain red team skills. "Information, training, and reference material
to learn all aspects of it are available publicly, and all can be
simulated in a lab environment to test and validate concepts." Don’t
make the stupid mistake of playing the bad boy/girl when you can
probably learn the same skills in the process of becoming an ethical
hacker, being an ethical hacker.

## For those already sweating blood on red teams

Let’s start with teamwork. According to Carlos, each member of the red
team should have a clear understanding of the client and systems to be
evaluated. Planning should be carried out precisely as a group. All
members can share their opinions from the beginning, and the team can
discuss them with the intention of reaching agreements. As the project
progresses, regular meetings should be held to review actions. At the
end of an engagement, "a debrief should be done where egos are left
outside and people are honest about what needs improvement."

For Carlos, it is false to say that new techniques and exploits need to
be kept secret, even from clients, to avoid losing advantages in other
engagements. Red teaming is not simply about emulation but also involves
cultivating a relationship with the customer, where critical thinking
can help manage potential risks and improve cybersecurity.

When, for example, in a pentesting or attack simulation exercise, the
client’s security teams succeed to catch you, keep in mind something
that Carlos shares from his experience: It may not necessarily be a
negative thing with your work and your capabilities; it may be that on
the client-side, they have already learned from previous engagements and
have applied the required measures. Following his words, you can remind
yourself that your task is to help them test their security and make
their systems more secure.

<div class="imgblock">

![cpq](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331133/blog/tribe-of-hackers-5/cpq_nti68o.webp)

<div class="title">

Figure 1. (Carlos’s original picture was taken from the referenced book.)

</div>

</div>

## For firms that in security aspire to be on the ball

Regarding the question of when to introduce a red team into an
organization’s security program, Carlos replies (in terms of
conditions): "\[In that organization\] There has to be a culture of
involving security at the start of a process, when it makes sense to
have it, and a willingness to hear alternate critical ideas of plans
when presented." It must be a firm that recognizes the necessity and is
willing to have its projects and systems under evaluation to identify
weaknesses and vulnerabilities in them. But not only that, according to
Carlos, the organization must be prepared to take on efforts to
eliminate and mitigate the risks reported by the red team.

Carlos' judgment is pretty valuable when he suggests that it’s better
not to implement a red team’s services within a company, at least not at
that moment, when their security team is somewhat isolated from the
general decision-making processes. Moreover, for him, it’s not a good
idea to convene the red teams when, rather than a partnership, what
there is between that company’s groups is just competition and conflict.

On the other hand, Carlos warns companies interested in their security
to beware of, from his perspective, the "least bang-for-your-buck
security control" that in many places can be seen implemented. He refers
to tools without metrics, objectives, and training adjusted to the
client company’s particularities, which end up only "providing a placebo
effect for those who signed the check."

Additionally, Carlos mentions an easy and straightforward security
control that a firm can implement now that [phishing](../phishing/) and
malware are so widely employed to compromise networks or systems. It’s a
matter of addressing the most common entry routes first. "Most companies
do not block or control the execution of HTA, Windows Scripting Host, or
Office macros," says the expert. After blocking entry routes, the
security team can begin to profile typical behavior within the
environment to build an automatic detection system for abnormal
behavior.

## That’s all, folks!

Don’t forget that you can access the full interview with Carlos Perez in
[Carey and Jin’s
book](https://www.amazon.com/Tribe-Hackers-Red-Team-Cybersecurity/dp/1119643325).
By the way, keep in mind that if you want to be part of the `Fluid
Attacks'` red team, you can check out [our Careers
page](../../careers/). And if you need information about our
[services](../../services/continuous-hacking/) and
[solutions](../../solutions/) for your organization, you can [click here
to contact us](../../contact-us/).
