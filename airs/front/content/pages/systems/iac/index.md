---
slug: systems/iac/
title: Infrastructure as Code (IaC)
description: Infrastructure as code is among the systems that we at Fluid Attacks help you evaluate to detect security vulnerabilities that you can subsequently remediate.
keywords: Fluid Attacks, Infrastructure As Code, Iac, Infrastructure, Cloud, Terraform, Continuous Hacking, Ethical Hacking, Pentesting
banner: bg-systems
template: system
---

<div class="paragraph fw3 f5 lh-2">

Infrastructure as code refers to configuration files
as editable scripts
that allow us to automatically provision and manage infrastructure resources,
such as those of public clouds.
Thanks to IaC,
we do not depend on manual configuration
of discrete hardware or operating systems,
as was previously the custom.
These scripts are built with high-level or declarative programming languages,
which,
rather than specifying how to do something,
say what needs to be done
or what the expected result is.
IaC ends up being a programmable infrastructure
that can be seen as an application
that runs on specific IaC tools.

</div>

<div class="paragraph fw3 f5 lh-2">

Public cloud providers such as Amazon,
Google and Microsoft have their own IaC tools
for provisioning and managing their resources.
There are also widely used tools,
such as HashiCorp Terraform,
which are compatible with many providers' services.
Using tools such as these,
necessary for the implementation of declarations
that are inside infrastructure as code files,
can lead to bugs.
Development teams viewing and acting on the IaC
as another piece of software
can experience difficulties in configuration tasks
that may result in security vulnerabilities.
However,
the positive side is that version control,
iterative testing and exhaustive security testing
can be performed on this,
as on any other software,
in a CI/CD pipeline before approval to go to production.

</div>

<div class="paragraph fw3 f5 lh-2">

Precisely,
at `Fluid Attacks`,
following the DevSecOps approach,
we integrate security from the beginning
and for the entire software development lifecycle,
including the development of IaC.
We continuously assess your IaC files
with techniques such as SAST
to detect bugs and security vulnerabilities
before these files move to live cloud environments.
Such security issues may include,
for example,
granting roles excessive permissions,
i.e., not following the principle of least privilege,
as well as problems in the configuration of encryption
and backup controls.
Our tests are based on compliance with multiple requirements
taken from international standards
(e.g., PCI DSS, HIPAA).
The details of the findings for IaC,
as well as for code,
open source components,
containers and other systems in your cloud usage,
are delivered to you in a single platform,
our ARM.
There we provide you with evidence and recommendations
so that your development team can quickly fix security issues
and your company does not face deployment failures
and even major troubles such as data breaches.

</div>