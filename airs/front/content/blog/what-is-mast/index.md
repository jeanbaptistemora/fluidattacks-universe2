---
slug: what-is-mast/
title: What's Mobile App Security Testing?
date: 2022-08-18
subtitle: Take care of your apps from cybercriminals on the prowl
category: philosophy
tags: cybersecurity, security-testing, hacking, company, risk
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1660857426/blog/what-is-mast/cover_mast.webp
alt: Photo by Agê Barros on Unsplash
description: Here we talk about mobile apps and some of their possible security risks, as well as what MAST is and how it can contribute to app security.
keywords: Mobile Apps, Mast, Applications, Security Testing, Application Security, Sast, Dast, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/fKAjOxgZNPg
---

Every morning when I wake up,
the first thing I do is grab my phone
to check what new messages I have received.
It's a deep-rooted habit.
For many of us,
the use of the capabilities of these devices is part of our daily routine.
As you no doubt have witnessed,
we are crowded with [mobile applications](../../systems/mobile-apps/).
We use them to manage our money,
order transportation services and food,
play games, set goals and track our physical activity,
and for loads and loads of other stuff.
There are even apps as bizarre and funny
as [the one that tells you](https://runpee.com/)
which are the appropriate moments in a movie
you're watching in the theater
to go urinate and not miss the most pivotal scenes.
Apparently,
at the beginning of this decade,
the number of mobile apps was already around [8.9 million](http://www.forbes.com/sites/johnkoetsier/2020/02/28/there-are-now-89-million-mobile-apps-and-china-is-40-of-mobile-app-spending/).

Beyond the personal use we make of mobile phones,
there is the use we now make of them in our workplaces
to fulfill business operations.
More and more employees are working from these devices.
This may have been influenced by the growth in remote working
due to the pandemic.
Increasingly,
data from organizations is being managed on mobile phones,
which in many ways have replaced computers.
Likewise,
mobile apps are now the mainstay of multiple companies
that depend on them to conduct their day-to-day business.
Enabled by them,
companies can have a place and participation in the online market
and connect with their customers or users
in different places around the world.

Competition in the mobile apps arena is incredibly fierce.
DevOps teams are tasked with building and releasing apps
at an accelerated pace
to gain traction among consumer groups
and with frequently updating them to cut the mustard.
However,
the rush should not translate into launching insecure apps.
Many apps have access to vast amounts of user information,
some of which is sensitive data that must be protected.
Mobile phones and their apps have aroused a lively hunger in cybercriminals,
who know that there,
as in any other IT system,
they can find vulnerabilities to exploit.

## Mobile application risks

Mobile apps and devices often do not achieve the same security level
as desktop apps and PCs.
The most common operating systems for mobile apps today are Android and iOS.
These systems have security controls
that help software developers to some extent to build secure apps.
Nevertheless,
it is often up to developers to choose between multiple security options,
and many times their decisions are not the best.

Mobile apps lacking proper controls can end up revealing sensitive data
to other apps on the devices.
Weak authentication,
authorization and data entry checks can be easily bypassed
by malicious users and malware.
On the other hand,
the absence of robust encryption
for data storage and transmission
is quite hazardous.
All these weaknesses are due to ignorance and mistakes
in the development process.
In this regard,
rookie developers
(although experts may commit these errors too)
can also innocently embed usernames and passwords
directly in their source codes.
Furthermore,
they can copy and paste code snippets
or download libraries and frameworks
without a second thought
and thus end up building and delivering vulnerable apps.

Risks such as the above are presented in the [OWASP Mobile Top 10](https://docs.fluidattacks.com/criteria/compliance/owaspm10),
part of the [OWASP Mobile Security Project](https://owasp.org/www-project-mobile-security/).
This project aims to provide software developers and security teams
with guidance resources for creating and maintaining secure mobile apps.
The standard offered in this project is the [OWASP MASVS](https://docs.fluidattacks.com/criteria/compliance/owaspmasvs)
(Mobile Application Security Verification Standard).
Linked to this standard is a guide,
the [OWASP MSTG](https://owasp.org/www-project-mobile-security-testing-guide/)
(Mobile Security Testing Guide),
which describes processes for testing the controls included in MASVS.

The latest OWASP Mobile Top 10,
[the 2016 list](https://owasp.org/www-project-mobile-top-10/2016-risks/),
presents the following risks:

1. **Improper Platform Usage:**
   The platform's features are not used correctly
   or its security controls are not implemented.

2. **Insecure Data Storage:**
   Data is not adequately protected
   and can be easily accessed by malicious users or malware.

3. **Insecure Communication:**
   There is no proper protection for network traffic
   and data is exposed to interception in transmissions.

4. **Insecure Authentication:**
   No or weak authentication schemes are used,
   allowing attackers to access private functions and data.

5. **Insufficient Cryptography:**
   Weak encryption algorithms or flawed encryption processes are used,
   allowing attackers to successfully revert sensitive data or code
   to their original form.

6. **Insecure Authorization:**
   Poor authentication schemes are used,
   allowing attackers to execute functionalities
   that must be intended for high privileged users.

7. **Client (Poor) Code Quality:**
   Poor coding practices were carried out
   so external users could enter code into the app for execution.

8. **Code Tampering:**
   Modifications in the code,
   in the system APIs,
   or in the data and resources of the app,
   whose behavior can be altered by attackers,
   are not detected.

9. **Reverse Engineering:**
   There is no effective code obfuscation
   to help prevent the conversion back into readable source code
   and the disclosure of internal information of the app.

10. **Extraneous Functionality:**
    Development leaves hidden features or test code within the app
    that can be exploited by the attacker.

As in other contexts,
cybercriminals targeting mobile apps aim to go undetected
and steal sensitive information,
including intellectual property,
alter app functionality,
redistribute it illegally,
infiltrate users' devices
and affect the reputation of app developers and owners.
Responsible companies that develop their mobile apps
or develop them for others
and that are part of the DevSecOps culture
choose to keep the security of their products under continuous assessment
to prevent cyberattacks and consequential losses.

<cta-banner
  buttontxt="Read more"
  link="/solutions/devsecops/"
  title="Get started with Fluid Attacks' DevSecOps solution right now"
/>

## This is where MAST comes in

Mobile application security testing
(MAST) analyzes these apps
during or after their development
to identify security issues in them
according to the mobile platform on which they run
and the frameworks in which they are developed.
MAST starts with an understanding of the business purpose of each app,
the intended users and the types of data it stores,
handles and transmits.
Identifying vulnerabilities during MAST
must be quickly followed by their remediation
to reduce the attack surface
and thus protect organizations and their users or customers
from threat actors.

The most commonly used evaluation techniques in MAST
for vulnerability detection
are static application security testing ([SAST](../../product/sast/))
and dynamic application security testing ([DAST](../../product/dast/)).
[The former is](../sastisfying-app-security/) the one
that accesses the internal structure of the app
while it's not running
to evaluate its source, byte or binary code.
It doesn't flag problems related to data in transition or at rest.
The latter is the one that,
without access to the structure,
analyzes the app's functionality while it's running.
It simulates attacks against the app and checks its reactions
(the effectiveness of its security controls).

Implementing one or even both of these techniques,
relying on automation alone,
is insufficient for a holistic assessment of a mobile app.
The automatic tools can be constantly updated
according to databases and new versions of mobile platforms,
but they are focused on detecting some known vulnerabilities.
For better coverage in MAST,
continuous [manual penetration testing](../../solutions/penetration-testing/)
should be included.
This procedure by security experts increases accuracy,
reducing false positive rates
and not missing more complex and severe vulnerabilities,
even zero-days.

When an organization requests this service,
it seeks to prevent the exploitation of vulnerabilities
in the apps it employs or offers to its users.
It seeks to ensure that the app's security controls are working properly
and thus protect the integrity and confidentiality of their
and their users' information.
When using digital distribution services,
such as the Google Play Store or Apple App Store,
organizations familiar with MAST
know that these providers do not fully review their apps.
(Neither Google nor Apple will conduct dynamic assessments, for example.)
They know that it is their own duty
to get comprehensive analyses of their software.

## MAST with Fluid Attacks

It doesn't matter if your company is small or large.
While the latter tend to be more sought after by cybercriminals,
the former can also become victims of cyberattacks through their apps.
At `Fluid Attacks`,
we offer MAST,
integrating SAST, DAST and manual penetration testing
to identify vulnerabilities in your [mobile apps](../../systems/mobile-apps/).
(Our ethical hackers have certifications such as [eMAPT](../../certifications/emapt/)
to evaluate the security of mobile apps
and many other credentials that [you can see here](../../certifications/)).
We easily introduce our tests into your software development lifecycle
to continuously analyze your code and configurations
to identify security issues
so you can remediate them before moving your apps to production.
Furthermore,
you might not restrict our tests to your apps
but also request them to check many other systems.
We remind you that within our analysis techniques,
we also have [SCA](../../product/sca/)
for detecting security issues
in your open source or third-party components.

You can [contact us](../../contact-us/)
to get more information about MAST at `Fluid Attacks`
and its capabilities.
And if you want to start enjoying our automatic tests,
you can request the 21-day free trial
of our [Continuous Hacking Machine Plan here](../../free-trial).
