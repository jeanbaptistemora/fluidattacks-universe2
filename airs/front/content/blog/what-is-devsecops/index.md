---
slug: what-is-devsecops/
title: What Is DevSecOps?
date: 2022-05-06
subtitle: Best practices and a description of the basics
category: philosophy
tags: security, devops, software, training, company, cybersecurity
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1651863001/blog/what-is-devsecops/cover_devsecops.webp
alt: Photo by SIMON LEE on Unsplash
description: Learn about what DevSecOps is, its importance, how it differs from DevOps, and its advantages on IT security for continuous delivery, testing and deployment.
keywords: Devsecops Meaning, Devops Vs Devsecops, Shift Left Security, Devsecops Best Practices, Devsecops Automation, Security Testing, Software Development Lifecycle, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/J-Fr6LalosU
---

You have probably noticed
that seemingly everyone is jumping on the [DevSecOps](../../solutions/devsecops/)
bandwagon.
Just last year,
about 36% of respondents
in GitLab's worldwide
[DevSecOps survey study](https://learn.gitlab.com/c/2021-devsecops-report?x=u5RjB_)
said their teams develop software using DevOps or DevSecOps.
And you'd probably very much like to know
just what the meaning of DevSecOps is.

Broadly speaking,
DevSecOps is a methodology
that incorporates security into the development (Dev)
and operations (Ops) processes.
In simple terms,
it means that the security of technology is assessed during its development,
but also that [security is everybody's business](../devsecops-concept/).

## DevOps vs DevSecOps

DevSecOps [has been called](https://www.infoq.com/articles/evolve-devops-devsecops/)
"the natural extension of DevOps."
So,
we need to explain
what is the difference between DevOps and DevSecOps.

Perhaps as famous a concept as DevSecOps,
[DevOps](../devops-concept/) is defined as a development methodology
whose aim is to bridge the gap between development and operations.
It accomplishes this
by stressing communication between developers and operators
and shared responsibility in quality assurance.

What's considered a main feature of DevOps is velocity.
Indeed,
here's where two processes shine,
for they are hardly absent when talking about DevOps.
One is continuous integration (CI).
This refers to the process of developers
integrating the code they work on into a shared repository
several times during the day,
every day.
Along with CI is continuous delivery (CD),
which means moving software to the production environment,
providing swift response to modifications and constant feedback.
Here's a positive outcome:
In GitLab's aforementioned
[2021 survey](https://learn.gitlab.com/c/2021-devsecops-report?x=u5RjB_),
almost 60% of developers said
they released code twice as fast thanks to DevOps.

Great as DevOps may sound,
there's no point in releasing fast
if the product might be riddled with bugs.
Teams attempt to prevent this
by implementing DevSecOps, meaning
they assess their code with security testing automated tools
or manual tecniques.
They do this during the entire development lifecycle.
That's right: from its beginning to its end.

## Benefits of DevSecOps

Forrester's report last year
on the state of application security
[showed](https://securityboulevard.com/2021/04/forresters-state-of-application-security-report-2021-key-takeaways/)
that 30% of security decision-makers surveyed in 2020
whose companies were breached
said the attack was possible because of software vulnerabilities.
DevSecOps aims to avoid this.
As changes to code are tested for vulnerabilities,
it's possible to get ahold of them
before the end-user gets a buggy software handed to them.

Yet another [worrying trend](../cybersecurity-trends-2021/)
is supply chain attacks.
Teams use third-party components
more often than not
to develop their software.
Also,
if they built the components themselves,
other teams will probably use them.
If attackers find a vulnerability
that allows them to mess with code,
components,
cloud services,
etc.,
common to various software projects,
they end up compromising the whole supply chain.
DevSecOps practices aim to secure software from upstream risk
and prevent teams from generating downstream risk.

And as we mention further below,
DevSecOps may also enable your team to save on remediation costs.

## How to evolve DevOps to DevSecOps

"Well, sign me up! How can I start?"
It's good that you ask!
Fortunately,
[there is some advice](https://www.infoq.com/articles/evolve-devops-devsecops/)
on evolving DevOps to DevSecOps.
You may start
by deciding to **expand shared responsibility and ownership**
of the software
to encompass its security also.
For the most part,
this is achieved by creating the possibility of collaboration
between the development,
operations and security teams.
Make no mistake:
[Everyone is responsible for "sec."](../devsecops-concept/)

You may also move on
to **specify the security checks**
in need of implementation into your DevOps processes.
Ideally,
most of them should be automated.
However,
an effort needs to be made to train developers on secure coding,
reviewing code for vulnerabilities as soon as a change is done.
Moreover,
it doesn't matter if they are not developers,
engineers or whatever;
every one of the employees must be aware
of any newly established security requirements
and know how to implement them in their daily work.

## DevSecOps best practices

We believe that best practices can be extracted
from items used in GitLab's
[DevSecOps Methodology Assessment](https://learn.gitlab.com/c/devsecops-assessment?x=u5RjB_).
Thus, we offer the following:

- **Culture:**
  Regularly informing employees about company-wide security policies;
  educating them to incorporate security practices
  (e.g., testing and code review)
  into their daily work;
  and holding them accountable
  "for assessing and maintaining the security of their work."

- **Velocity:**
  Launching small code changes quickly and securely.

- **Shift-left testing:**
  Having security scans built into the developers' workflow
  at the early stages of development
  to search for known vulnerabilities in the code they've just written;
  this way they can fix them
  before the security team reviews the scan results.

- **Collaboration:**
  Encouraging prompt communication
  and making it possible for the entire project team
  to find out where the vulnerabilities are in the code,
  who introduced them,
  what's been done about them
  and their remediation status.

- **Automation:**
  Successfully integrating security into the CI/CD pipelines,
  so that every change in the code is automatically scanned,
  and automatically creating issues/tickets
  or breaking the build
  (whichever is the organization policy)
  in case a vulnerability is found.

- **Security standards:**
  Automating the use of security standards,
  evaluated and set by the security team,
  and regularly evaluating compliance.

## Shift-left security

We can't stress enough
the importance of starting security testing from the very beginning.
Visualize the software development lifecycle across a straight horizontal line,
project planning on the leftmost point
and production deployment on the rightmost point:
We're asking you to move security testing ever to the left.

The whole idea concerning shift-left testing is to identify
and address security issues in software
from the early stages of development.
That is,
not well into the traditional testing stage
of the software development lifecycle
but much earlier,
even when defining its requirements
(e.g., what it should do and the resources needed).

Shifting testing to the left may help you
produce more secure software and save money.
It has been argued
that remediation at the early stages of development
[is less costly](https://landing.fluidattacks.com/us/ebook/)
than at the production deployment stage.

## DevSecOps automation

As we mentioned earlier,
it's ideal to have automated security checks.
This includes essential things
like implementing multi-factor authentication
and having automated security testing tools
(e.g., [SAST](../../categories/sast/),
[DAST](../../categories/dast/))
running in your CI pipelines.
However,
these tools may generate false positives
and false negatives,
so an even better strategy is to have actual people use manual techniques
(e.g., manual SAST, DAST
and [pentesting](../../solutions/penetration-testing/))
to find vulnerabilities in your software.
In fact,
our ethical hackers [found about 81%](https://try.fluidattacks.com/report/state-of-attacks-2021/)
of the high and critical severity vulnerabilities reported
in systems over an analysis period in 2020.

We at `Fluid Attacks` help you enact your DevSecOps practices:
You can integrate our [DevSecOps agent](https://docs.fluidattacks.com/machine/agent)
into your pipelines
and configure it to [break the build](../../solutions/devsecops/)
if our SAST or DAST tools find a vulnerability in your code.
Moreover,
you can ask us about our [Squad Plan](../../plans/),
which involves ethical hackers assessing the security of your technology.
To learn more,
[contact us](../../contact-us/)\!
