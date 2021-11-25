---
slug: tribe-of-hackers-1/
title: Tribe of Hackers Red Team 1.0
date: 2020-07-17
subtitle: Learning from the Red Team Expert Marcus J. Carey
category: opinions
tags: cybersecurity, red-team, hacking, pentesting, ethical-hacking, blue-team
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331129/blog/tribe-of-hackers-1/cover_yosoni.webp
alt: Photo by Lucas Benjamin on Unsplash
description: This post is based on the book 'Tribe of Hackers Red Team'
  by Carey and Jin. Here we share an introduction and some
  of the highlights of the first interview.
keywords: Cybersecurity, Red Team, Hacking, Pentesting, Ethical Hacking,
  Blue Team, Knowledge, Tribe
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/R79qkPYvrcM
---

[*Tribe of Hackers Red
Team:*](https://www.amazon.com/gp/product/B07VWHCQMR/ref=dbs_a_def_rwt_bibl_vppi_i2)
*Tribal Knowledge from the Best in Offensive Cybersecurity* by Marcus J.
Carey and Jennifer Jin (2019) belongs to the *Tribe of Hackers*
cybersecurity book series. It was recently shared with me here at `Fluid
Attacks`, and now I would like to share with you some of the highlights
that I selected for this post. Maybe there’s something that will pique
your curiosity.

[Marcus J. Carey](https://www.linkedin.com/in/marcuscarey/) is an
American hacker with more than **25** years of experience in
cybersecurity. He’s someone who describes himself as an inquiring,
curious person since he was a child. He never denied himself the
possibility of generating and raising questions to expand his knowledge
on various subjects. Hungry minds are what we usually count on, or
rather, something that characterizes us as humans regardless of the
information we pursue. That hungry mind of Marcus made it possible to
give birth to this book that I currently hold in my hands.

Let’s take a look at what we can learn from these almost **300** pages.
In the beginning, Marcus says: "You probably picked up this book to
learn from the best in red teams." Yeah, we’re indeed interested in [red
teams](../red-team-exercise/). It is also true that, as in many branches
of knowledge, the information shared by 'the best' is usually valuable.
Here, the questions, formulated with the support of a cybersecurity
community on Twitter, are addressed to hackers specialized in offensive
security, aka red teaming. That sounds great\!

- \- - - - - - - - - - - - - - - - - - - - -

### Parenthesis

At `Fluid Attacks`, we work purely as a *red team*, which means we are
continually testing or attacking infrastructures, applications, and
source code to find vulnerabilities that can pose risks for both owners
and users of those systems. On the other hand, a *blue team* is
responsible for defending the systems to ensure "that the
confidentiality, integrity, and availability of all assets are not
affected," Marcus says. In other words, the red team, with its cannon,
verifies how effective the blue team’s work has been in establishing the
wall. Then, when we refer to the combination of both sides, implemented
in some organizations, we talk about a [purple team](../purple-team/).

- \- - - - - - - - - - - - - - - - - - - - -

Specifically, Marcus and Jennifer (his collaborator) asked the same
**21** questions to **47** experts in red teaming to shape this book. Of
course, the first to answer them is Marcus himself. We are going to
focus on some of his opinions in this post; possibly the first one of a
series focused on *Tribe of Hackers Red Team*.

<div class="imgblock">

![Marcus J. Carey](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331128/blog/tribe-of-hackers-1/marcus_wvbmtg.webp)

<div class="title">

Figure 1. Marcus’s photo taken from
[LinkedIn](https://www.linkedin.com/pulse/im-unemployed-i-am-hiring-marcus-carey?articleId=6202227092038365184#comments-6202227092038365184&trk=public_profile_article_view)

</div>

</div>

According to Marcus, "it is uncommon for people to start directly into
red team jobs." (Well, it’s noteworthy that most hackers at `Fluid
Attacks` began working as red teamers and never were part of blue teams,
as I was informed.) He says that the best way to get a red team job is
to start working for a blue team and gain cybersecurity skills as a
software engineer, systems administrator, or related roles. Once there,
you can get more involved in cybersecurity
[events](../../about-us/events/) and networks, and also prepare and seek
to obtain some [certification](../../about-us/certifications/) from
those related to red teaming. Besides, you can download virtual machines
and web applications with vulnerabilities if you want to start
practicing by yourself. Of course, to avoid problems with the law, keep
in mind that it’s prudent to exploit only systems that are either your
own or have explicit permission for this type of activity.

From an organization standpoint, one of Marcus’s phrase is quite
remarkable: "I believe that everyone in information technology and
software engineering should know how to build, secure and hack anything
they are in charge of." Although it may certainly sound excessive, this
comment reflects a suggestion of skills integration. And this is partly
what many companies have achieved by allowing the formation of purple
teams. However, on the other side are the companies that have opened
their doors to pentesting only for compliance and have kept it quite
limited. That should be concerning for them\!

For one of the questions referring to the most important control to
prevent a system from being compromised, Marcus chose "restricting
administrative privileges for end users" as an answer. He mentions this
as something easy to implement and scale in any organization. It is
something simple but it yields significant results. This is also the
case for "two-factor/two-step authentication, password length, and
automatic updates." All this is linked to his other suggestion on the
general defense of systems against attacks: put policies in place and
follow them. By the way, have you heard about our
[Rules](https://docs.fluidattacks.com/development/stack/commitlint/syntax/commit#rules),
`Fluid Attacks'` compilation of security requirements? Check them out to
get an idea of how we do this\!

As Marcus’s suggestion regarding teamwork, communication should be
highlighted as the most significant element. Besides, it should be
accompanied by a high degree of trust among team members. They need not
be afraid to seek help from their peers when required. In addition,
Marcus suggests transparency, which means the possibility that all other
members can see everything that each team member does and documents.
That’s something allowed by the use of collaborative tools. As I read
these recommendations, I am pleased to acknowledge that they are
faithfully followed at `Fluid Attacks`.

Now, if you’re working as a red teamer, and you have to debrief and
support an external or internal blue team after completing an operation,
you should act as a professional. What does that mean? "Always let them
know you are on the same team as far as the big mission goes," Marcus
advises. At the same time, don’t get upset and help them if their plan
to correct the issues you discovered doesn’t work or is not applied
correctly. Besides, as a relevant recommendation for useful reports,
don’t dismiss the idea of using [CVSS](https://www.first.org/cvss/),
[MITRE ATT\&CK](https://attack.mitre.org/), or
[NIST](https://nvd.nist.gov/general) as references. Use publicly shared
knowledge, don’t try to reinvent what is already stated, and
consequently gain ease of information transmission and credibility.

Marcus highlights how crucial empathy can be for a red teamer. He says:
"Put yourself in the other person’s shoes and don’t be a jerk."
Therefore, he proposes this human characteristic as one to consider when
recruiting red team members. Nonetheless, I think it is necessary to
clarify that empathy is common in people (leaving aside atypical cases),
although its level of expression is variable. It is true that some of us
*show more empathy* than others, but it’s also true that it is something
we can improve.

Finally, and perhaps as a return to what he mentioned about himself
initially, Marcus refers to the hunger for knowledge as an essential
factor of an excellent red teamer. This person would be someone
motivated to study, to learn how things work. They would be willing to
improve some skills and always ready to help others. Precisely, Marcus
and the other red teamers interviewed in his book are helping us.
They’re sharing their knowledge with us. And if it turns out that we
already knew all this, well, it doesn’t hurt to remember it. Maybe they
can even say words that motivate us, and that’s good on its own.
