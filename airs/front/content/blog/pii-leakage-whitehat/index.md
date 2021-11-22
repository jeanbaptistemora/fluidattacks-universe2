---
slug: pii-leakage-whitehat/
title: Have You Noticed the PII Leakage?
date: 2020-04-03
subtitle: 'WhiteHat: the more you collect, the higher the risk'
category: opinions
tags: vulnerability, application, software, information,
  cybersecurity, business
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330974/blog/pii-leakage-whitehat/cover_dupvh1.webp
alt: Photo by Tyler Nix on Unsplash
description: 'This blog post is based on the webinar ''Mobile Security
  App-titude: Best Practices for Secure App Design and Data Privacy''
  by Eduardo Cervantes from WhiteHat.'
keywords: Vulnerability, Mobile, Application, Software, Information,
  Cybersecurity, Business, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/yKalliZTaQU
---

I want to start with this sentence that Khare gave us days before the
webinar (which you can access
[here](https://www.brighttalk.com/webcast/11691/387589)) in a blog post
(link
[here](https://www.whitehatsec.com/blog/mobile-security-app-titude-best-practices-for-secure-app-design-and-data-privacy/)):
“Mobile app owners and developers are receiving a failing grade on due
diligence to protecting consumer data.”

There are different means by which information can be collected today to
identify a particular individual. People are continually registering for
various programs and applications. For this, we are providing a lot of
private data that can easily be used by other subjects for multiple
purposes.

At `Fluid Attacks`, we are always attached to a security-oriented
context. This time, in this post, we focus on the part of the mobile app
security. Cybercriminals see mobile devices as desirable sources of
information, especially sensitive information that we store on these
devices.

Such sensitive information can also be categorized as personally
identifiable information or `PII`. This information may include the real
name, alias, account name, actual address, IP address, email address,
social security number, passport, driver’s license number, and some
other data.

Each of these data being part of an aggregate can contribute to the
identification of a particular individual. The attacker may be able to
distinguish the person and perhaps trace it back to committing some
fraud, such as identity theft. Many of us innocently believe that what
we enter into a specific software is known only to us and no one else.

Much of what we deliver or do in the applications can indeed be shared,
sold, or used by third parties for analysis, marketing, and advertising
purposes. They may begin to know our interests and preferences and from
that make *the most appropriate* offerings, or improve our experience
within the application and deliver a better service.

Business leaders are often not honest about how they are handling and
protecting customer data. The information collected can be used in a
business from a competitive framework to gain an *unfair* advantage.
Others have gone a little further, and have sought to influence users
within political campaigns. Such was the case of **Cambridge
Analytica**, a British political consulting firm, which accessed private
data from millions of **Facebook** users to influence elections.

<div class="imgblock">

![Owners](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330973/blog/pii-leakage-whitehat/owners_q12qom.webp)

<div class="title">

Figure 1. taken from [here](https://i.redd.it/uyg05brl56ky.png)

</div>

</div>

The attackers are always going to be lurking, even when we think we’re
safe. The applications that we believe are the most secure, because of
their popularity, also come to mean high risks for the privacy of our
information. Cervantes and Khare told us, concerning data breaches and
data sharing, and from one of their recent company reports:

- “**70%** of the **350** popular Android apps leak sensitive personal
  data.”

- “**82%** of retail apps leaked sensitive data.”

- “**67%** of travel apps leaked sensitive data.”

- “**50%** of finance and insurance apps leaked sensitive data.”

If we are creators of mobile apps, we must look for the best ways to
deal with the possible risk of data breaches, always trying to guarantee
the privacy of our users and keep their data safe. One of the biggest
risks comes from the simple fact of collecting too much information from
the users of our applications. From there, the risk increases because of
the ways of sharing, and in itself the traffic that this information
has.

## Recommendations

It is then indicated as recommended for risk reduction with user data
and to prevent mobile app security intrusions, the following:

On the one hand, it has to be defined what information is required; what
information is needed for the application. Distinguish which of it is
part of the sensitive data or `PII`. Within the `GDPR` ([General Data
Protection Regulation](https://gdpr-info.eu/)), privacy by design is an
essential requirement, so the applications we develop must maintain,
process, and share with external sources the *necessary* user data. But
what information is classified as *necessary*, and who defines that?
—Something to consult later.

On the other hand, it is crucial to establish how long it is *necessary*
(this concept again) to store the data and in which places this storage
will be done. Certainly, data encryption can always be a useful tool
(although some know how to decrypt). However, it is recommended that
sensitive data is transmitted and displayed but does not persist in the
memories; that closing the application means the disappearance of that
information.

With the transit and hosting of information through the networks,
appropriate validation and certification processes must be ensured.
Also, the background of the third-party providers on how they handle the
data collected must be known.

It remains ideal that the data is stored in a secure system. Here we
rely heavily on the developers and their knowledge of secure coding
practices. These practices should be in place prior to the design and
development of software. The central idea is to make the code little or
not vulnerable at all. However, always bearing in mind that everything
generated can be hacked. Hence the need to maintain a constant
evaluation of the system, even in the middle of development.

We come back to something that is continuously repeated in the area of
cybersecurity. In essence, sometimes the developers don’t know, or
sometimes they don’t pay attention to it and the subsequent risks, and
they are not building secure code when creating software. Sometimes they
don’t even know how or don’t have the tools to address a vulnerability
before it becomes a problem. Besides, enterprise managers may request
application development for quick commitment to their customers without
fully considering the value of cybersecurity assessment and
implementation.

Is your company prepared for the implications that an application
security breach may have? Always keep mobile application security
testing as an option, so that the application in question is attacked,
and vulnerabilities that give access to external people or systems to
the private information of the mobile application user are identified.
Again, this is something to be done periodically; at least it is what we
recommend.

It would indeed be prudent to stop collecting so much information to
reduce the risks. How willing would application developers be to do
this? Leaving that extraordinary possibility aside, we recommend keeping
as a priority the proper securing of other people’s information on any
kind of system.

Would you like to know about `Fluid Attacks` [continuous
hacking](../../services/continuous-hacking/) services? [Contact
us](../../contact-us/).
