---
slug: rules-new-standard/
title: We've Reached a New Standard
date: 2020-04-17
subtitle: More requirements in Rules are firmly supported
category: philosophy
tags: security, cybersecurity, information, documentation, standard,
  ethical-hacking
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331070/blog/rules-new-standard/cover_ch6n0s.webp
alt: Photo by Bradley Feller on Unsplash
description: Here we briefly outline Rules, Fluid Attacks's set of security
  requirements, along with the world-renowned standards that have served as
  a reference for us.
keywords: Security, Cybersecurity, Information, Documentation, Standard,
  Rules, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/lynE-l7F8sY
---

Earlier this month our `CTO`, Rafael Alvarez, informed us: *"We’ve
already finished the synthesis of the `GDPR` standard in Rules*."

What does that mean?

As Danilo Vásquez —Security Analyst at `Fluid Attacks`— explained to us,
different `GDPR` requirements, all of which were considered suitable,
became technical requirements for our company. That is, they were
incorporated into `Rules`.

Let’s clear this up:

`Rules` was born there in **2009** (inspired by [Common
Criteria](https://www.commoncriteriaportal.org/)) from the combination
of knowledge and "*experience in the field of computer security with
various international standards related to this topic*," according to
Oscar Prado —Cybersecurity Analyst - Releaser at `Fluid Attacks`.

`Rules` can be defined —following Danilo— as "*a compendium of
requirements based on the existing security standards*." Not all general
security standards have been covered at this time. Not all of our
requirements are linked to at least one of those standards we have. But
these are things we intend to achieve in the near future.

The technical
[requirements](https://docs.fluidattacks.com/criteria/requirements/),
apart from those that may be "out-of-scope," are linked to what is
verifiable through a technical process in a system. They are those that
can be evaluated with [`DAST`](../fuzzing-forallsecure/), [`SAST`, or
`SCA`](../sast-sca-kiuwan/), techniques that we have already mentioned.

The out-of-scope security requirements, which can focus, for example, on
security training and documentation, in contrast, can only be verified
by audits. And although they are not technical, as Oscar says, "*they
play a key role in a security test. For example, the lack of training of
an employee can allow a [phishing](../phishing/) attack to take place*."
Even some of them may later become technical requirements.

The requirements that we have in `Rules` have kept a consistent and
simple language, easy to understand. They allow to delimit a pentesting
or an ethical hacking process. The delimitation will depend on what each
client wants to test and on the concepts of risk and vulnerability that
he handles. The requirements that are chosen determine the stringency
and extent of pentesting.

Hackers have in `Rules`, as Paula Vélez, Security Architect at `Fluid
Attacks` suggests, "*a performance guide, because if a requirement is
not being satisfied, that means there is a vulnerability to be
reported*." Hacking is made easier; time and effort are saved if the
requirements are found in a single set or single source.

Likewise, clients save time thanks to `Rules`, as they don’t have to
resort to a multiplicity of standards that fit their security needs. In
`Rules`, we synthesize, and we handle homogeneity of expression no
matter the diversity of origins of the base standards.

`Rules`, as a whole, ends up presenting good practices not only to
developers and configurators of products and systems but also to other
members of the organizations that can influence their security. The
requirements serve as a guide from the beginning or in full flow. They
serve to prevent the manifestation or recognize the presence of security
gaps —all this independently of the technology that is being used.

So, we know that many of our requirements are already associated with
one or more reputable standards. But what are these standards that
currently serve us as references? Let’s finish this blog post by
mentioning them.

## Standards

<div class="imgblock">

![standards](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331068/blog/rules-new-standard/standards_efg4ea.webp)

<div class="title">

Figure 1. [Photo by Mathieu Perrier](https://unsplash.com/photos/1wDyL2_NmE4)
on Unsplash

</div>

</div>

1. [`HIPAA`](https://www.hhs.gov/hipaa/index.html)

    Health Insurance Portability and Accountability Act, [enacted by the
    United States Congress
    in 1996](https://en.wikipedia.org/wiki/Health_Insurance_Portability_and_Accountability_Act).
    As we found in [a
    guide](https://www.hipaaguide.net/hipaa-for-dummies/), this
    legislation was created, among other objectives, for the
    modernization of the flow of healthcare information. Besides, it was
    for the stipulation of how the `PII` ([Personally Identifiable
    Information](../pii-leakage-whitehat/)), within the healthcare
    context, should be protected by industries to avoid theft and fraud.
    The `HIPAA` comprises five essential rules, each with different
    requirements. These rules are: **1)** `HIPAA` Privacy Rule, **2)**
    `HIPAA` Security Rule, **3)** Breach Notification Rule, **4)**
    Omnibus Rule, and **5)** Enforcement Rule.

2. [`ASVS`](https://owasp.org/www-project-application-security-verification-standard/)

    The Application Security Verification Standard is a project from the
    Open Web Application Security Project
    ([`OWASP`](https://en.wikipedia.org/wiki/OWASP)), an online
    community for the production of freely-available material in the
    field of web app security. `ASVS`, as we can see on its
    [website](https://owasp.org/www-project-application-security-verification-standard/),
    "*provides a basis for testing web application technical security
    controls*." It also provides developers with requirements oriented
    to secure development, protecting from vulnerabilities in web apps.
    These requirements can also be used by anyone who wants to build and
    test secure apps.

3. [`CWE`](https://cwe.mitre.org/)

    Common Weakness Enumeration, as we found on its
    [website](https://cwe.mitre.org/), "*is a community-developed list
    of common software and hardware security weaknesses*." The `CWE`
    list serves as a support, with a common language, for the
    identification of vulnerabilities. Such identification is essential
    for their subsequent reduction or repair, and also for prevention.
    The `CWE` has an orientation towards the communities of development
    and security professionals. It seeks to help ensure that weaknesses
    in software and hardware are remediated before the delivery of
    products, or that they are prevented to avoid putting organizations
    at risk.

4. [`NIST`](https://www.nist.gov/about-nist)

    The National Institute of Standards and Technology, from the United
    States, has been active for more than a century. `NIST` provides
    different measurements, standards, and technologies to support a
    variety of scientifically based, human-made products and services,
    regardless of their size and complexity. Inside `NIST` is the
    Information Technology Laboratory (`ITL`), and linked to it is the
    National Vulnerability Database
    ([`NVD`](https://nvd.nist.gov/general)). The `NVD`, created in
    **2000**, "*is the `U.S.` government repository of standards based
    vulnerability management data represented using the Security Content
    Automation Protocol (`SCAP`). This data enables automation of
    vulnerability management, security measurement, and compliance*.” At
    `Fluid Attacks`, we are mainly interested in the [`NIST` Special
    Publication 800-53 (Revision 4)](https://nvd.nist.gov/800-53/Rev4).
    It is a database associated with security and privacy controls for
    federal information systems and organizations.

5. [`BSIMM`](https://www.bsimm.com/)

    Building Security In Maturity Model, as expressed on its
    [website](https://www.bsimm.com/), "is a study of existing software
    security initiatives *." It quantifies the security practices of
    many organizations and describes a common ground and variations. It
    is a data-driven model resulting from the analysis of those
    initiatives or "\_application/product security programs*" to face
    the challenge of securing the software. `BSIMM’s` descriptive model
    has evolved in line with advances in the field of security. It has
    also grown by collecting and analyzing new data from new companies
    and those with maturing programs. At `Fluid Attacks`, we use its
    ninth iteration.

6. [`GDPR`](https://gdpr-info.eu/)

    General Data Protection Regulation is a set of rules within the
    European Union (`EU`) and the European Economic Area (`EEA`) [about
    data protection and
    privacy](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation).
    These rules also address the collection, storage, and transfer of
    data from European subjects outside those areas. The `GDPR` enables
    the unification of international regulations for organizations
    processing personal data of European citizens. It also aims to give
    individuals more control over their personal information and its
    treatment. Companies are required to apply data protection
    principles (using those strictly necessary) in processing activities
    and business practices from the initial stages.

Do you want more information about it? [Contact us\!](../../contact-us/)
