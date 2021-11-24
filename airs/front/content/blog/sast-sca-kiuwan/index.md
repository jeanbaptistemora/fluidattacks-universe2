---
slug: sast-sca-kiuwan/
title: Are SAST and SCA Enough for You?
date: 2020-04-13
subtitle: An automatic process that could prove to be limited
category: opinions
tags: cybersecurity, application, software, security-testing, cloud,
  ethical-hacking
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331072/blog/sast-sca-kiuwan/cover_tuhbnl.webp
alt: Photo by Geran de Klerk on Unsplash
description: This blog post is based on the webinar 'Audit your App with
  Kiuwan Local Analyzer' by Sebastian Revuelta, Customer Manager at Kiuwan.
keywords: Cybersecurity, Application, Software, Security Testing, Cloud,
  Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/ADUiP4nJwds
---

[Sebastián Revuelta’s
webinar](https://www.youtube.com/watch?v=zWKq6n4ZoRY&feature=youtu.be)
is a kind of practical conference in which the author presents one of
the applications created and used in his organization. We will take and
present some of the information that is relevant to us.

Revuelta opens with the question **“why do we need security analysis?”**
In view of this, he gives an account of how the number of
vulnerabilities has been increasing in recent years, which can be
explored and used by hackers to do damage to organizations' systems.
Hence, the answer to the question ends up being: security analysis is
necessary to find security flaws in the system and prevent attacks by
malicious hackers ASAP.

There are different software analysis techniques that we can employ to
find vulnerabilities. In a [previous post](../fuzzing-forallsecure/)
focused on fuzzing, we had already mentioned `SAST` (Static Application
Security Testing) and `DAST` (Dynamic Application Security Testing)
techniques. The former, as Felipe Gómez (LATAM Manager of `Fluid
Attacks`) suggests in a webinar, is the one we can apply from the moment
our software developer releases the first line of code. The latter
technique is the one we can apply when the developer has already built a
functional environment with the code.

At this time, we include another technique called `IAST` (Interactive
Application Security Testing), which as a main difference with the two
previous ones, has its activity or operation [within the
application](https://www.ptsecurity.com/ww-en/analytics/knowledge-base/sast-dast-iast-and-rasp-how-to-choose/).
In this technique, the code is analyzed while the application is being
executed. With `IAST`, we can interact with the functionality of the
application, either manually or automatically.

Additionally, there’s a technique called `SCA` (Software Composition
Analysis). This is nothing more than an extension of previous
techniques, which [Rafael Ballestas](../stand-shoulders-giants/) had
already told us about, and which is aimed at Free and Open Source
Software (`FOSS`), specifically at the elements of this type that are
part of a particular application. This is an [automated
process](https://www.g2.com/categories/software-composition-analysis)
for reviewing policy and license compliance, version updates, and
security risks.

**Parenthesis**: When we talk about
[`FOSS`](https://en.wikipedia.org/wiki/Free_and_open-source_software),
we mean software shared openly on the Internet that can be used and
altered in its code in any way by anyone.

For the handling of all the aforementioned types of analysis, Revuelta
refers to an Application Security Testing Orchestration (`ASTO`) to be
performed on a single platform. However, within his company, the `ASTO`
is only oriented to the management of `SAST` and `SCA` techniques and
their results, referring to the security status of the software in
evaluation.

With the application presented by Revuelta —the Kiuwan Local Analyzer—
the client’s source code is analyzed locally, on his company’s network.
Then, the encrypted results are sent to the Kiuwan cloud.

Once the client runs the Kiuwan app on his system, he can choose one by
one the applications to be analyzed. `SAST` and `SCA` can be performed
individually or together. The program can be opened several times at the
same time to make analyses of different applications since the interface
scans one at a time. Within the options, the client can also delimit the
language or languages to be analyzed according to the files under
evaluation. The analysis, it should be noted, is an automatic process of
the software.

Kiuwan’s app also has the option to delimit an "analysis scope," which
can be: 1) baseline, 2) complete delivery, or 3) partial delivery.
Baselines and deliveries are described as two different types of
analysis. The baseline analysis is run when we want to get an image of a
software version. We can make a comparison between a new version of the
software and the previous versions. We can see whether or not we have
improved the security of the software. We can tell whether or not we
have repaired the defects. With this analysis, we obtain an evolutionary
record, positive or negative, of the software in question.

Once the developer has made some minimal changes to the software to be
analyzed, the recommended security analysis for this case ends up being
the delivery one. The Kiuwan application will tell us if that delivery
is accepted or rejected, according to some security gates or checkpoints
previously configured, to be integrated into the baseline or the master
version. The results of all analyses are presented to users on the
Kiuwan website.

All the analysis processes mentioned so far with Kiuwan’s application
can also be performed from the command-line interface. However, in this
blog post, we are not interested in an in-depth description of its
process.

We think it’s important at this point to highlight a couple of things:

Maintaining only the `SAST` type analysis process (or just combined with
`SCA`), and only in automatic, can be problematic. `SAST` often models
the behavior of the code
[inaccurately](https://www.ptsecurity.com/ww-en/analytics/knowledge-base/sast-dast-iast-and-rasp-how-to-choose/)
and therefore tends to lead to high rates of false positives and false
negatives.

`SAST` should be a part of a complementary process. Besides, `SAST`
should not be performed just from a tool. The automatic procedures must
act very well, but only in what we define as 'deterministic'.

At `Fluid Attacks`, we don’t just stick with `SAST` and `SCA`. Here we
also perform `DAST` and `IAST`. Furthermore, it is not that we hand over
the work to an application or a tool that can be useful for any type of
technique. At `Fluid Attacks`, we extract the best possible from
automatic and manual work.

The ethical hacking service at `Fluid Attacks` uses the techniques we
have mentioned, through a team of experts supported by automated tools.
As Kevin Amado —one of the hackers inside `Fluid Attacks`— shares with
us, the tools automatically search and report. The expert helps at first
a little by directing the tool. What the tool cannot find, is in turn
sought and found through human cleverness.

Also, following what Kevin reports, “*tools find a percentage of the
total, but in the end, it’s the human being who decides whether the tool
is right or wrong.*” The analysis tools save work, and although they
tell lies many times, it becomes easier to determine those lies, than to
look for the total vulnerabilities by hand, according to Kevin.

Other tools, not oriented to the search for vulnerabilities, serve
instead for other system inspections. They are used for surveys, flow
analysis, or preliminary scans. And other tools are also used to make
the closing exploits; to express whether or not the vulnerabilities in a
system have been remediated, and from that to allow or not the transfer
to production.

The `ASTO` process —which at Kiuwan comprises `SAST` and `SCA`— at Fluid
Attacks comprises `SAST`, `DAST`, `IAST`, and `SCA`, and is carried out
on our Attack Surface Manager (`ASM`). At `Fluid Attacks`, to keep false
positive and false negative records near `ZERO`, we go beyond the use of
automatic tools and employ human acumen and sagacity.

We invite you to approach us to learn more about our
[services](../../services/continuous-hacking/). [Contact
us\!](../../contact-us/)
