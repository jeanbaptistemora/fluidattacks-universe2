---
slug: secdevops-security-champions/
title: Discovering Security Champions
date: 2020-05-21
subtitle: Six recommendations for SecDevOps from Carnegie Mellon
category: philosophy
tags: security, devops, software, information, web, cloud
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331091/blog/secdevops-security-champions/cover_nkri6h.webp
alt: Photo by Ingo Stiller on Unsplash
description: Here you'll learn about Security Champions. But first, we give
  you five recommendations if you're considering the implementation
  of security in your business.
keywords: Security, Champions, Devops, Secdevops, Software, Information, Web,
  Cloud, Ethical Hacking, Pentesting, Devsecops
author: Felipe Ruiz
writer: fruiz
:name: Felipe Ruiz
:about1: Cybersecurity Editor
:source: https://unsplash.com/photos/3tkxfe2GocY
---

I recently attended a webcast from Carnegie Mellon University entitled
"[At What Point Does DevSecOps Become Too Risky for the
Business?](https://www.youtube.com/watch?v=n0FRNpoqYT0&feature=youtu.be)"
(I’m not sure if this was the appropriate title, but I don’t pretend to
criticize that). This webcast was presented by Hasan Yasar, Technical
Director at Software Engineering Institute at Carnegie Mellon, and Altaz
Valani, Director of Research at Security Compass. When I watched it, I
found some similarities with the information that I shared in [a post on
DevSecOps/SecDevOps](../devsecops-concept/). However, these authors
spoke on a broader sense, considering the business risks of companies
offering software. I want to recap some of their ideas, grouped here
into five general recommendations, and expand a little on another one (a
sixth recommendation): the Security Champions. This last section is
supported by a SAFECode.org paper called "[Software Security Takes a
Champion,](http://safecode.org/wp-content/uploads/2019/02/Security-Champions-2019-.pdf)"
in which Altaz Valani also participated.

## General recommendations

### 1. Insert security into your processes asap

Many companies reflect an urgency for the rapid deployment of new
features in their apps without considering security. Is software
security being omitted because it’s assumed to be an obstacle? And in a
broader context, what about business security? Is business risk
management being ignored? Within the SecDevOps culture, it’s expected
that both speed and security are included from the beginning. Don’t
start building and deploying apps continuously from your company if you
haven’t assessed the business risks and how they can be avoided.

### 2. Set security requirements from the beginning

Companies can manage risk from different perspectives. For example, the
"cyber-resiliency perspective" and the "compliance perspective." In the
former, considering possible impacts due to future vulnerabilities being
attacked, the main concern is to find rapid solutions to those problems
every time. In the latter, usually from a highly regulated environment,
more thought is given to the evaluation of compliance with rules. It’s
recommended to work from this compliance perspective and set
requirements based on public security standards such as
[GDPR](../../compliance/gdpr/), [HIPAA](../../compliance/hipaa/), and
[PCI DSS](../../compliance/pci/) from the beginning (see our compilation
called [**Criteria**](https://docs.fluidattacks.com/criteria/)). These
requirements must be adjusted to the structure and functionality of the
software developed in your business. Besides, some must mean translating
your business risks to technical language.

### 3. Keep the security requirements as obligatory

The security requirements may indeed be in constant remodeling. But be
aware that if you define requirements to be met in your company, which
can be re-evaluated, the idea is that they should be obligatory. If at
any point they haven’t been met, then any workflow before the software
deployment must be stopped. Later, you should ask questions such as: Did
the developer not understand something? Does he need training? Is it a
false positive by the tool? Is this an appropriate tool? Also, ensure
that reports of non-compliance reach each interested audience in a
language suitable for their understanding.

### 4. Use the right tools for your business

Maintaining secure infrastructures and products is a challenge,
especially when there are constant changes in their architecture.
Therefore, security testing must also be continuous. Automation in
processes such as SAST and DAST will depend on some tools; you must be
careful concerning them. It’s not a question of acquiring tools because
they’re offered as new, or because the competition uses this and that,
or because they are supposed to be useful in your security testing
processes. "What tools are essential for our business?" This is a
question you can answer with the help of your developers with security
expertise (Security Champions?).

### 5. Look at security from technical and business perspectives

What is highly recommended in approaches such as SecDevOps is the
integration of groups. With security already in place, besides a
'technical approach' from software engineering, it should have a
'business approach' from business risk management. Therefore, it’s
recommended to include the business group in SecDevOps with its security
viewpoint. With this, it’s expected that the mindset of many will change
towards the framework in which security is seen as indispensable for the
maintenance of production and income generation. It’s important to
emphasize that the information to be transferred between groups must be
clear and complete. On the one hand, the developers of your company must
understand whether or not their work is contributing to managing
business risks. On the other hand, those in charge of your business'
security must understand what the technical team is communicating to
them (e.g., challenges, issues, needs).

## 'Security Champions' (a sixth recommendation)

<div class="imgblock">

![Security Champions](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331090/blog/secdevops-security-champions/lions_lqcl1b.webp)

<div class="title">

Figure 1. [Photo](https://unsplash.com/photos/1pdp-PGplss) by [A P on
Unsplash](https://unsplash.com/@windogram)

</div>

</div>

The integration of teams can be favored by the presence of 'champions'
of each area. In the inclusion of security in software engineering for
business, having one or more 'Security Champions' (SC) can be quite
useful.

### What is a Security Champion, and what does he or she do?

In short, the SC is a software developer who possesses and applies
extensive security knowledge within a development team. The SC is
responsible for identifying and solving security problems early in the
SDLC so as not to slow down processes. The SC assists with verification
that security requirements are met during the development process.
Additionally, he translates technical information from the DevOps group
to the security and business management groups, and vice versa.
Therefore, the SC interacts closely with these groups, gets along with
the experts on each side, and builds a bridge between them.

The SC can prioritize security issues based on business risks, of which
she has a full understanding. She also assists in the selection and use
of assessment tools and the interpretation of results. As an outcome of
education at universities, there are usually few security-educated
software engineers with extensive knowledge of "[both internal and
customer-related security (and regulatory)
needs.](http://safecode.org/wp-content/uploads/2019/02/Security-Champions-2019-.pdf)"
With SC’s help, a formal, contextualized, and well-defined support for
the security training of developers and other members can be established
within a company. The SC can conduct activities with the developers to
expand their knowledge and motivate them to become security experts.
Also, the SC can help ensure that members of a company’s security team
are no longer seen as 'bad cops' and that developers don’t see them as
adversaries to avoid.

### What knowledge should the SC possess?

First of all, the SC should be a person with knowledge of software
engineering. Especially about tools and methods for the development and
deployment of secure software. This person should know about threat
identification and mitigation, risk analysis, and attack path analysis.
Also, this individual should know the multiplicity of existing
vulnerabilities, the lists that group them, and how they’re classified
(quite exciting topics that we hope to review soon). He should have
skills in the discussion and presentation of information. And finally,
the SC should be able to resolve conflicts, motivate people, and be kind
and attentive to others.

Companies that develop and offer software as a product or service may
employ different strategies to become part of a culture in which
security plays an essential role. It’s one thing for these companies to
have paid tools and services for their protection. It’s undoubtedly
another thing to have developers in their staff who, without being
forced, want to acquire and apply security knowledge. Among them,
possibly, there will be emerging Security Champions, who will certainly
bring them significant benefits.

So, have you already discovered at least one SC among your team members?
