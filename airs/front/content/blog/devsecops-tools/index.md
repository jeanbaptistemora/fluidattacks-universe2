---
slug: devsecops-tools/
title: Our DevSecOps Tools
date: 2022-08-26
subtitle: How we use DevSecOps tools for Continuous Hacking
category: philosophy
tags: cybersecurity, devsecops, security-testing, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1661525496/blog/devsecops-tools/cover_tools.webp
alt: Photo by Syarafina Idris on Unsplash
description: We present the DevSecOps tools that we use in combination with manual security testing in our Continuous Hacking solution.
keywords: Devsecops Tools, What Are Devsecops Tools, Security Testing, Application Security, Sca And Sast, Software Development, Continuous Hacking, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/dCeWUxnIYaM
---

[DevSecOps](../devsecops-concept/)
is a culture
that embeds security into every phase of software development.
As we have said
in [our advice on DevSecOps implementation](../how-to-implement-devsecops/),
there are several tools
that may be used as part of this culture in your organization.
A DevSecOps tool,
which serves as a complement to the work of expert security testers
in this approach,
is that which allows you to perform diverse testing methods automatically
throughout the entire software development lifecycle (SDLC).
The experts perform the security testing methods manually
to identify more complex and higher severity vulnerabilities
and, additionally,
review the reports created by the tools,
which, although fast,
have accuracy shortcomings.
This combined methodology is quite valuable
for the comprehensive integration of security
while moving at DevOps speed.

In this blog post,
we'll talk about the DevSecOps tools
we use at `Fluid Attacks`
and how we have achieved their implementation
in our [Continuous Hacking](../../services/continuous-hacking/) solution.

## What are DevSecOps tools?

Today's software development process is fast paced.
Developers need to deploy software solutions into production
several times a day
to meet consumer demand
and keep up with the trends.
[DevOps](../devops-concept/) traditionally places security
in the testing phase of the SDLC,
hunting for bugs and errors.
But as soon as teams become aware
of how much the threats of cyberattacks can hurt their organization
and customers,
they learn the importance
of making security a part of the SDLC
from the very start.
This is at the heart of a culture called DevSecOps
and is partly achieved
by integrating manual and automated security testing
into the DevOps workflow
to enable security checks across the SDLC.
Of course,
we say "partly" because a few more things need to be achieved
to fully embrace DevSecOps.
(See "[How to implement DevSecOps](../how-to-implement-devsecops/)"
and "[DevSecOps best practices](../devsecops-best-practices/).")

Tools for DevSecOps,
which complement the manual work of security analysts,
allow running some security testing methods automatically.
These tools are used throughout the entire SDLC
and with the guidance of security experts.
In addition to focusing on the vulnerabilities
that represent the most significant risk exposure for a system,
these experts constantly review the result reports by the tools.
Combined manual and automated work yields accurate and faster results.
Below,
you can see a representation of the SDLC.
As we've argued in [another post](../how-to-implement-devsecops/),
organizations
wishing to implement DevSecOps
need to define the moments for security activities.
Some DevSecOps tools are therefore more suitable
from a certain phase onward
but one thing is notable:
Most of them are put into use
before the traditional testing phase.

<div class="imgblock">

![Pipeline DevSecOps Fluid Attacks](https://res.cloudinary.com/fluid-attacks/image/upload/v1661526215/blog/devsecops-tools/pipeline-devsecops-fluid-attacks.webp)

<div class="title">

(Image taken from [here](https://marvel-b1-cdn.bc0a.com/f00000000236551/dt-cdn.net/images/devsecops-image-2000-6557ba1b00.png).)

</div>

</div>

## Fluid Attacks' DevSecOps tools

<br />

### Static application security testing (SAST)

[Static application security testing](../../categories/sast/)
is a method
that can be used continuously
from the code phase of the SDLC onward
to look at vulnerabilities introduced in source code,
byte code
or the application's binaries.
Our automatic SAST analyzes the source code
in your repository
and can help you learn quickly
the severity of vulnerabilities reported in it,
how much risk exposure corresponds to each of them,
where exactly you need to make changes,
what the recommended remediation is,
etc.
Our security analysts conduct manual SAST alongside our tool
to find more complex,
perhaps zero-day,
vulnerabilities
and reduce false positives and false negatives.
As our client organizations' developers work swiftly
on fixing the vulnerabilities we report
and learn how not to introduce them again in the source code,
they all start to become security developers.

<cta-banner
  buttontxt="Read more"
  link="/solutions/devsecops/"
  title="Get started with Fluid Attacks' DevSecOps solution right now"
/>

### Software composition analysis (SCA)

[Software composition analysis](../../categories/sca/)
is a method
that can be introduced in the building phase
and used continuously
to look at the third-party code dependencies,
from which your software may inherit vulnerabilities.
Our automatic SCA does not stop
at finding buggy open-source dependencies
but also identifies the licenses
of all open-source dependencies in your codebase.
To avoid legal risk,
[we advise you](../choosing-open-source/)
to choose open-source with a license
that is compatible with your organization's policies.
As our SCA inventories the open-source dependencies in your software,
it's easy to produce a software bill of materials (SBOM).
In manual SCA,
hackers enrich the results from the tool,
verifying
that all the software dependencies with vulnerable versions are reported.
As you can easily guess,
SCA
and all the methods and tools in this blog post
should be used still in production phases.
For example,
during the monitor phase,
organizations must keep open-source components up to date
and identify any threat due to criminals exploiting zero-days in them.

### Dynamic application security testing (DAST)

[Dynamic application security testing](../../categories/dast/)
is a method
that can be used continuously from the test phase onward.
It is performed
to assess a build artifact
that can be deployed into staging or testing environments.
Why is this?
Because DAST attacks the application while it's running
and analyses its response.
Our automatic DAST assesses,
to name a few things,
whether user authentication
and authorization work well
and looks for vulnerabilities
that would allow attacks such as injection.
By combining automated and manual DAST,
the simulated attacks are more clever,
as our hackers create their own exploits
and use their up-to-date knowledge
of the techniques used by threat actors.
Since DAST has no access to the source code,
manual SAST steps in
to complement the security testing.

### DevSecOps agent

`Fluid Attacks'` [DevSecOps agent](https://docs.fluidattacks.com/machine/agent)
is a component
that can be implemented
from the coding phase onward
and used continuously.
It checks the changes to the repository for noncompliance
with the organization's vulnerability acceptance policies
and **breaks the build**
if it finds anything wrong.
Breaking the build means
preventing a vulnerable version of the system
from being deployed into production.
Therefore, it is among the automated tools
for enforcing secure code development.
It can be deduced that its work is
customizable by every organization for each of their projects.
For instance,
the organization may define
that it will have the agent break the build
only for vulnerabilities whose [CVSS](https://docs.fluidattacks.com/about/glossary/#cvss)
base score is between certain values.
Although our DevSecOps agent works automatically,
it feeds on the results of automated
and manual SAST and DAST,
so that there's no doubt about accuracy.

### Attack Resistance Management platform (ARM)

`Fluid Attacks'` [Attack Resistance Management platform](https://docs.fluidattacks.com/machine/web/arm)
is ready to run nonstop
from the very start of your project,
in every one of the DevSecOps stages.
ARM is where our client organizations map
every one of their digital assets,
get results from every security testing method,
track their risk exposure over time,
receive evidence and guidance from our ethical hackers,
manage vulnerability remediation and stakeholders,
and more.
The fact that ARM not only provides a real-time inventory
of exposed and attackable software
but offers all the above
makes it more complete
than an attack surface management (ASM) platform.

## Leveraging DevSecOps tools for Continuous Hacking

At `Fluid Attacks`,
we integrate DevSecOps tools
into a single solution called [Continuous Hacking](../../services/continuous-hacking/)
throughout all the stages of the DevSecOps cycle.
In our working scheme,
developers deploy micro changes first
on their repositories,
and then our [ethical hackers](../what-is-ethical-hacking/) manually,
together with such automated tools,
seek to detect **all** the security issues in the technology.
In such a way,
we continuously test the latest versions of the repositories
corresponding to our clients' projects.
It's our DevSecOps agent
that we incorporate into the continuous integration
and continuous deployment (CI/CD) pipelines
to ensure that no identified vulnerability is released into production.
Thanks to our security testing scheme,
software development teams deploy technology to production
several times a day
without sacrificing speed and security.

Want to try our DevSecOps tools free for 21 days?
Check out our [free trial](../../free-trial/)
of Continuous Hacking Machine Plan.
If you have any questions,
[contact us](../../contact-us/)\!
