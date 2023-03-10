---
slug: casa-approved-static-scanning/
title: Our CASA-Approved Static Scanning
date: 2022-12-23
subtitle: Our CLI is an approved AST tool to secure cloud apps
category: politics
tags: cybersecurity, security-testing, software, cloud, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1671827428/blog/casa-approved-static-scanning/cover_casa.webp
alt: Photo by Kostiantyn Li on Unsplash
description: Fluid Attacks' automated tool is recommended by the App Defense Alliance for static scanning under the Cloud Application Security Assessment (CASA) framework.
keywords: Application Security, Security Testing, Cloud Application Security Assessment, Casa, Static Scanning, Machine, App Defense Alliance, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/NDJPAIKrTEE
---

The App Defense Alliance added Fluid Attacks' CLI application
as an approved tool for application security testing (AST).
The Alliance is a partnership between Google et al.
formed to ensure that Android applications are secure for users.
Our [open-source offering](https://docs.fluidattacks.com/machine/scanner/plans/foss)
is free to use for static scanning
and has been officially accepted to validate tier 2 requirements
of the Alliance's Cloud Application Security Assessment (CASA) framework.

## The purpose of the App Defense Alliance

The App Defense Alliance (ADA) [emerged in 2019](https://security.googleblog.com/2022/12/app-defense-alliance-expansion.html).
Its members are Google,
ESET, Lookout, Zimperium and,
more recently,
McAfee and Trend Micro.
This partnership is committed to ensuring applications available in Google Play
are not ridden with vulnerabilities.

To fulfill its purpose,
the ADA requires developers to verify
that their applications comply
with industry standards for application security.
In the case of mobile apps,
the ADA launched [Mobile Application Security Assessment](https://appdefensealliance.dev/masa)
(MASA).
While for cloud applications,
it established [Cloud Application Security Assessment](https://appdefensealliance.dev/casa)
(CASA).

The MASA framework validates that apps have the security controls
defined in the OWASP [Mobile Application Security Verification Standard](https://docs.fluidattacks.com/criteria/compliance/owaspmasvs/)
(MASVS).
(By the way,
we've listed [elsewhere](../what-is-mast/) the top risks to mobile apps
and defined the role of mobile application security testing (MAST),
which,
if you [leverage with us](../../product/mast/),
can check your compliance with MASVS and beyond.)

We are, however,
focusing on the CASA framework in this post.
So let us explain it a bit more deeply.

## Cloud Application Security Assessment (CASA)

The ADA created CASA as an initiative for Android apps
to comply with the controls
proposed by the [OWASP Application Security Verification Standard](https://docs.fluidattacks.com/criteria/compliance/asvs)
(ASVS).
Its main purpose with this project is
to enable secure cloud-to-cloud integrations
and boost their extensibility and inclusiveness.

Now,
applications differ in things like the sensitivity of the data they access,
the amount of users per type of data accessed
and their creating company's risk tolerance level.
For that reason,
the framework is adapted to have a risk-based,
multi-tier approach.
To put it plainly,
the tiers (1, 2 and 3) communicate
how strictly security requirements should be followed.

Framework users,
such as Google,
ask developers to verify their compliance with CASA standards.
It's the former,
not devs,
who determine the tier.
Sure,
devs [can decide](https://appdefensealliance.dev/casa/casa-self-start)
to initiate the assessment without having been contacted,
but in this modality only passing the tier 3 assessment
would get them a valid CASA verification.
This tier requires devs to choose an authorized assessor,
who would then test the security of the application for a cost.

Teams needing tiers 1
and 2 assessments can use [CASA-recommended scanning tools](https://appdefensealliance.dev/casa/tier-2/tooling-matrix)
to check their applications for common vulnerabilities.
And here's where we've got news!

**We are listed under the [**static scanning procedures**](https://appdefensealliance.dev/casa/tier-2/ast-guide/static-scan).**
You can use our CASA-approved,
open-source CLI application without cost
to perform [static application security testing](../../product/sast/)
(SAST).

## Our CLI app can be leveraged for vulnerability scanning

**Fluid Attacks' Machine** is our CLI application
that [devs can configure](https://docs.fluidattacks.com/machine/scanner/plans/foss/)
to run source code analysis
and assess web applications and other attack surfaces.
It performs vulnerability scanning
and reports the names of identified vulnerabilities
(according to Fluid Attacks' own [standardized set](https://docs.fluidattacks.com/criteria/vulnerabilities/))
along with their CWE IDs and location in your source code.
To learn how to configure
and use our CLI tool as a vulnerability scanner,
follow [our guide](https://docs.fluidattacks.com/development/skims#using-skims).

If a CASA Framework User requests you pass the tier 2 assurance level,
be sure to follow the [process](https://appdefensealliance.dev/casa/tier-2/tier2-overview)
described by the ADA.
Use Machine to scan your application
as the Alliance shows in [its website](https://appdefensealliance.dev/casa/tier-2/ast-guide/static-scan).

You'll be requested to revalidate your application once every year.
Remember,
though,
that it's not like during that time security is not a concern.
You should think about it always,
with every change to your application.
By conducting security testing [all the time](../../solutions/devsecops/),
you can be aware of and fix common vulnerabilities.
We can help you with this.

<cta-banner
  buttontxt="Read more"
  link="/solutions/security-testing/"
  title="Get started with Fluid Attacks' Security Testing solution right now"
/>

## Secure your applications with Fluid Attacks

We offer [Continuous Hacking](../../services/continuous-hacking/),
which involves performing AST throughout your software development lifecycle
(SDLC).
We configure Machine
to detect your application's vulnerabilities with accuracy.
You can see every finding and several details,
including recommendations for fixing the security issues,
on our [Attack Resistance Management (ARM) platform](../../platform/).
There you can also contact us for support via live chat.

Among the benefits of Continuous Hacking are

- securing every deployment without delaying your time-to-market;
- ensuring compliance with several international
  [standards](https://docs.fluidattacks.com/criteria/compliance/) (e.g.,
  PCI DSS, GDPR, CCPA),
  and
- enabling your [cloud DevSecOps](../why-is-cloud-devsecops-important/)
  implementation.

You can choose between [two paid plans](../../plans/):
Machine and Squad.
Machine Plan offers continuous
[static application security testing](../../product/sast/) (SAST),
[dynamic application security testing](../../product/dast/) (DAST)
and [software composition analysis](../../product/sca/) (SCA)
with our scanning tool only.
Squad Plan adds AI prioritization
and continuous [manual penetration testing](../../solutions/penetration-testing/).
Our ethical hackers find the vulnerabilities
that represent the most risk to applications.
That's why we recommend you go beyond automation
and favor security testing done through the eyes of attackers.

If you'd like a taste of our solution,
start your [21-day free trial](https://app.fluidattacks.com/SignUp)
of Machine Plan
and upgrade to Squad Plan whenever you want.
