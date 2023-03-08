---
slug: secure-code-review/
title: Do You Apply Secure Code Review?
date: 2022-09-02
subtitle: Yes, you, who think your app is immune to cyberattacks
category: philosophy
tags: cybersecurity, security-testing, software, company, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1662160860/blog/secure-code-review/cover_secure_code_review.webp
alt: Photo by Edi Libedinsky on Unsplash
description: In this blog post, we focus on secure code review and the benefits of applying it early and consistently in your software development lifecycles.
keywords: Secure Code Review, Software, Application, Benefits, Best Practices, Vulnerabilities, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/1bhp9zBPHVE
---

"If code has not been reviewed for security holes,
the likelihood that the application has problems is virtually 100%."
This is a shrewd message
on the first pages of the [OWASP Code Review Guide](https://owasp.org/www-pdf-archive/OWASP_Code_Review_Guide_v2.pdf).
An organization that does not put the code it uses and develops under review
is irresponsible with its assets
and those of its customers or users.
Security problems in its products can be exploited by cybercriminals,
leading to data breaches or disruption of operations
and consequent fines and loss of clients and reputation.
To help prevent all of this,
it's prudent to match software development from the outset
with a [secure code review](../../solutions/secure-code-review/).

## What is secure code review?

Secure code review is the examination of an application's source code
to identify security flaws or vulnerabilities.
These appear in the software development lifecycle (SDLC)
and must be closed or fixed to strengthen the security of the code.
Secure code review can take place at any point in the SDLC,
but within [the DevSecOps culture](../devsecops-concept/),
it is most valuable to use it from the early stages.
This is a procedure
that can be performed either manually or automatically.

The manual secure code review is conducted with great attention to detail.
One or more security analysts scrutinize each line of code,
understanding what they are evaluating,
keeping in mind its use and context,
the developer's intentions,
and the business logic.
On the other hand,
the automated secure source code review is a process
in which more code is examined in less time
but in which the above factors are not considered.
The tools work with a predefined set of rules,
are restricted to certain types of vulnerabilities
and suffer,
some more than others,
from the defect of reporting false positives
(saying that something is a vulnerability when it is not).
Among the most commonly used methods in secure code review
are [Static Application Security Testing](../../product/sast/)
(SAST)
and [Software Composition Analysis](../../product/sca/)
(SCA).
(Understand in [this previous blog post](../differences-between-sast-sca-dast/)
how one differs from the other.)

The best option for achieving a robust and secure code review
is to take manual and automated reviews
and merge them to leverage their particular capabilities.
Automated secure code review tools,
with their quick and "superficial" assessment of the attack surface,
make it easier for security analysts
to focus on identifying more complex and business-critical vulnerabilities.
Experts,
especially [ethical hackers](../../solutions/ethical-hacking/),
from the threat actors' perspective,
can review code to recognize the security issues
that contribute most to the risk exposure of the target of evaluation.
(For example,
in our latest annual [State of Attacks report](https://try.fluidattacks.tech/state-of-attacks-2022/),
we shared that **67.4%** of the total risk exposure
in the assessed systems
was reported by the manual method).
This makes it possible for vulnerability remediation,
an action that should always be connected to the code review,
to follow a prioritization.
Ultimately,
the idea is to reduce the number of flaws
that go into production
as much as possible
but continually repair the most dangerous first.

A successful development team,
committed to the security of its products,
always has secure code review as a pillar.
Any organization that develops software should have it
among its constant practices,
from the early stages of the SDLC,
paying attention to the small changes
that the members of its team gradually make to the code.
Security in general
and common weaknesses in software and their exploitation
are not usually taught to developers in their academies and workplaces.
And even the most experienced developers,
due to factors such as burnout or carelessness,
can make coding mistakes
and end up generating vulnerabilities
such as those listed in the [OWASP Top 10](https://docs.fluidattacks.com/criteria/compliance/owasp10)
and [CWE Top 25](https://docs.fluidattacks.com/criteria/compliance/cwe25).
For reasons such as these,
source code should usually remain under review
by security experts.

Secure code review identifies the absence of safe coding practices,
lack of appropriate security controls,
and violation of compliance standards
such as [PCI DSS](https://docs.fluidattacks.com/criteria/compliance/pci)
and [HIPAA](https://docs.fluidattacks.com/criteria/compliance/hipaa).
Secure code review providers may find,
for instance,
missing or erroneous validation of inputs
(verification that they comply with specific characteristics)
coming from different sources
that interact with the application
(e.g., users, files, data feeds).
They may discover that
a developer made the mistake of leaving confidential information
(e.g., tokens, credentials)
inside the code,
having forgotten to remove it
after putting it there without reasonable justification.
They may see that information
that does need to be stored and transferred
doesn't pass through proper encryption algorithms.
Likewise,
they may find that user authentication processes are pretty weak,
requiring, for example, short passwords
with little variety in their characters.
And that authorization controls are poor
and end up giving unnecessary access to any user
without requesting permission.

An important issue often discovered within secure code review
(with the help of, for example, the SCA method)
is vulnerabilities within third-party and open-source software components.
Application development today heavily depends on such components,
which are imported from various sources
and serve as support for what is intended to be built,
which often turns out to have little originality.
The dependency also exists between some components with others.
So when using one of them,
the developer may not be aware of the relation of this one with the others.
Cybercriminals have among their desired targets
these dependencies and components
to look for vulnerabilities to exploit.
This is such a frequent problem that,
in fact,
as we reported in [State of Attacks](https://try.fluidattacks.tech/state-of-attacks-2022/),
the most common security issue
among the evaluated systems
was "[Use of software with known vulnerabilities](https://docs.fluidattacks.com/criteria/vulnerabilities/011),"
and the requirement whose violation amounted to the highest total exposure
was "[Verify third-party components](https://docs.fluidattacks.com/criteria/requirements/262)."

For secure coding practices,
we recommend you review the [OWASP Code Review Guide](https://owasp.org/www-pdf-archive/OWASP_Code_Review_Guide_v2.pdf)
with your development team.

<cta-banner
  buttontxt="Read more"
  link="/solutions/secure-code-review/"
  title="Get started with Fluid Attacks' Secure Code Review solution right now"
/>

## What are the benefits of secure code review?

Secure code review is part of a preventive approach,
which should be addressed first,
rather than a reactive approach.
Applying this method as soon as the first lines of code are written
makes it possible to identify and remediate vulnerabilities
before going into production
so as not to patch the application continuously.
Staying one step ahead of malicious hackers
and blocking in the code any possible entry for improper uses,
even simple shenanigans,
is undoubtedly a very effective strategy
to reduce the likelihood of catastrophes caused by cyberattacks.

Secure code review allows the number of errors or vulnerabilities
found in the final stages of the SDLC,
through procedures such as [manual penetration testing](../../solutions/penetration-testing/),
to be lower.
Therefore,
the time developers have to spend on remediation processes
in these stages can also be reduced.
Fixing a large number of vulnerabilities shortly before going into production
becomes a thorn on the developers' side.
Always keep in mind that
it is easier and less expensive
to do code fixes in the development environment than in production.
With a continuous secure code review,
you are closer to the cause of the problem
and can fix it immediately,
avoiding any buildup.

Thanks to an early secure code review,
developers can start to assume a commitment
not only to remedy the security issues identified in their products
but also to make their results better every day.
This can be a chain process.
Certain groups of developers,
with the help of the security teams and their tests or reviews,
can pass on knowledge,
inspire others to improve their practices and productivity
and make the transition to a mindset
in which everyone in the organization is responsible for security.
Those security missteps that so often gave rise to vulnerabilities
can become less frequent over time.

Organizations that decide to implement secure code review
in their software development processes
recognize the responsibility
to comply with established standards in their industries.
They seek to offer products and services
that guarantee security for their operations,
data and other resources,
mainly those of their customers or users.
In this way,
they succeed in generating trust and reflecting commitment and quality.
This positively affects their competitiveness
and helps them to maintain a strong reputation.

## Fluid Attacks' Secure Code Review solution

While a team of developers can do their own code reviews,
such as when a developer asks a teammate to peer review their build
to avoid logical or stylistic errors,
it is recommended that,
in security issues,
experts in the field be involved.
Review by an external agent can ensure that all flaws are reported
while maintaining an unbiased view.

At `Fluid Attacks`,
we offer our [Secure Code Review solution](../../solutions/secure-code-review/)
as a comprehensive and accurate review of your software source code,
combining manual and automatic procedures
based on methods such as [SAST](../../product/sast/)
and [SCA](../../product/sca/).
With us,
you can apply secure code review from the earliest stages of your SDLC
in a continuous manner.
You can solve your security issues promptly
(prioritizing those that represent the highest risk exposure)
in favor of your development team's productivity
and the security of your products.

We support around **40** programming languages,
including C, C#, C++, HTML, Java, JavaScript,
PHP, Python, Ruby and Swift.
We have among our review requirements
those present in more than **60** international [security standards](https://docs.fluidattacks.com/criteria/compliance/),
including CERT, CVE, CWE, HIPAA, NIST, OWASP and PCI DSS.
And we adjust to specific requirements for your application and business logic,
all constantly reviewed and updated.
We integrate our DevSecOps agent into your CI/CD pipelines
to break the build when there are policy violations and open vulnerabilities.
And we report everything to you
in our [Attack Resistance Management platform](https://app.fluidattacks.com/)
(ARM),
where you can thoroughly understand and analyze your security issues,
as well as receive recommendations and manage remediation processes.
All this is part of our [Continuous Hacking](../../services/continuous-hacking/)
service,
which also integrates security testing methods such as [DAST](../../product/dast/),
[manual penetration testing](../../solutions/penetration-testing/)
and [reverse engineering](../../product/re/).

Do not hesitate to [contact us](../../contact-us/)
if you want more information about our Secure Code Review
and other solutions in our Continuous Hacking service.
[Click here](https://app.fluidattacks.com/SignUp)
to try our Continuous Hacking Machine Plan free for **21 days**.
