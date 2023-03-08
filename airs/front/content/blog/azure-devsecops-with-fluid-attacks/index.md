---
slug: azure-devsecops-with-fluid-attacks/
title: How We Support Azure DevSecOps
date: 2022-11-03
subtitle: Continuous manual security tests for going beyond MCSB
category: philosophy
tags: cybersecurity, devsecops, cloud, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1667483115/blog/azure-devsecops-with-fluid-attacks/cover_azure.webp
alt: Photo by Alvan Nee on Unsplash
description: The Microsoft cloud security benchmark recommends regular red teaming and pentesting. We talk about how we help you go beyond that and achieve Azure DevSecOps.
keywords: Devsecops, Azure Devsecops, Azure Devsecops Tools, Cloud Devsecops, Devsecops On Azure, Microsoft Cloud Security Benchmark, Red Teaming, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/ZCHj_2lJP00
---

[Azure](https://azure.microsoft.com/en-us/)
is Microsoft's public cloud computing platform.
A major player,
[it surpassed](https://www.zdnet.com/article/cloud-computing-microsoft-azure-ups-the-pressure-on-aws/)
Amazon Web Services (AWS) and Google Cloud
in adoption growth during 2021.
As such,
Azure offers tools and functionalities,
as well as infrastructure,
storage and processing power.
This allows businesses of all sizes to develop scalable apps
and save on costs.
Since these apps need to be secure,
Azure has services that help users
follow [DevSecOps best practices](../devsecops-best-practices/).

Despite the fact
that some activities in DevSecOps consist of automating security testing
and updates,
tech alone does not cut it.
Azure itself advises
in the [Microsoft cloud security benchmark](https://learn.microsoft.com/en-us/security/benchmark/azure/)
(MCSB)
that manual techniques
such as [**red teaming**](../what-is-red-team-in-cyber-security/)
and [**pentesting**](../what-is-manual-penetration-testing/)
should complement vulnerability scanning to discover risks.
Greater attention should be directed to this,
since our ethical hackers often find insecure configuration of cloud services.
In this blog post,
we talk about how `Fluid Attacks` supports your Azure DevSecOps implementation
with manual techniques
in combination with automated security testing.

## The cloud security shared responsibility model (SRM)

Before we move on to the main subject of this post,
let's first address a relevant topic:
the cloud security [shared responsibility model](../shared-responsibility-model/)
(SRM).
We won't distract you for long.
All you need to remember is that Azure,
as a cloud service provider,
will be responsible for actions
such as maintaining the availability of its services,
the security of physical infrastructure supporting them
and building security features into its solutions.

But we users need to be aware of our responsibilities too.
We have to secure our DevOps environment
and deploy secure apps in the cloud.
So, we will be held accountable
for failing to protect the software supply chain,
conduct continuous security testing,
configure services properly,
and so on.
For the purpose of fulfilling this responsibility,
we users need to turn to [cloud DevSecOps](../why-is-cloud-devsecops-important/).

## DevSecOps on Azure with Fluid Attacks

The [DevSecOps](../devsecops-concept/) culture
seeks to bring the development,
security and operations teams together
since the beginning of software development
in order to build more secure apps.
(We explain elsewhere [how to implement DevSecOps](../how-to-implement-devsecops/).)
In the cloud,
this culture requires teams to pay attention as early as possible
to the proper configuration of cloud services
and conduct continuous security testing
of infrastructure as code (IaC) files and container images,
among other things.
This shift-left security approach makes solving issues easier and cheaper.

In support of its users achieving DevSecOps,
Azure has provided recommendations
for automating security with its products.
Moreover,
it is at the center of the [MCSB](https://learn.microsoft.com/en-us/security/benchmark/azure/)
published in October 2022,
which is a rebrand of the Azure Security Benchmark (ASB).
This resource provides prescriptive controls
that help users improve their multi-cloud environment
and the security of workloads, data and services on Azure.

The controls in the MCSB include activities for protecting data,
networks and access to resources,
gaining visibility of assets and risks to them,
and ensuring clear organizational security strategies, policies and procedures.

There are Azure DevSecOps tools to help implement these controls.
So,
for example,
teams can use the service Azure Pipelines for CI/CD.
This tool allows them to compile and package code in containers,
thus securing the developer environment,
and have version control.
To address the issue of data,
networks and access protection,
Azure offers the service Azure Key Vault to store API keys,
certificates, tokens, passwords and other secrets,
and Azure Active Directory (Azure AD) to manage identity and access control.

<cta-banner
  buttontxt="Read more"
  link="/solutions/devsecops/"
  title="Get started with Fluid Attacks' DevSecOps solution right now"
/>

When it comes to assessing risk,
two domains in the MCSB deserve special attention:
**posture and vulnerability management** and **DevOps security**.
The following are some controls that,
we argue,
sum up the assessment activities in these domains:

- **Secure DevOps infrastructure:**
  Actions like identifying any misconfiguration in core areas of Azure DevOps,
  weak authentication mechanisms and secrets in the source code.

- **Ensure software supply chain security:**
  Actions like ensuring open-source components are up to date
  and free of known vulnerabilities.

- **Integrate static application security testing (SAST)
  into DevOps pipeline:**
  Actions like assessing source code
  and preventing vulnerable code from being deployed into production.

- **Integrate dynamic application security testing (DAST)
  into DevOps pipeline:**
  Actions like testing the runtime application.

- **Enforce security of workload throughout DevOps lifecycle:**
  Actions like managing vulnerabilities in container images
  and dependencies across the entire software development lifecycle (SDLC).

- **Conduct regular red team operations:**
  Actions like complementing the traditional vulnerability scanning approach
  with penetration testing and red teaming.

Azure offers guidance that may tackle some controls in these areas.
So,
it advises scanning container images for vulnerabilities
with Microsoft Defender for Cloud
and also using GitHub automated security testing solutions
to further search for vulnerabilities in proprietary code
(e.g., credentials in source code)
and third-party components (e.g., outdated open-source libraries).

If you consider the last control in the above list,
you can see
that an approach focused merely on using Azure DevOps security tools
and other DevSecOps software falls short.
One strong reason is that automated tools yield results
with significant rates of false positives and false negatives.
Manual work is needed to review results
and identify issues that a tool, say, for SAST or DAST, would not.

Case in point:
In our [2022 State of Attacks](https://try.fluidattacks.tech/state-of-attacks-2022/),
in which we show the analyses of security testing results of our clients
over the span of one year,
we found that it was our ethical hackers only,
not tools,
who detected **all the critical severity vulnerabilities**
reported in the systems.

As experts in pen testing and red teaming,
we now show you
how we can support your DevSecOps implementation with these approaches.

**Penetration testing** is done through simulations of real-world attacks,
e.g., using tailored exploits to bypass defenses.
This is a prime example of functional testing
which demands creativity
and knowledge of the techniques of today's threat actors
that can't be achieved by tools.
(In fact,
[we argue](../what-is-manual-penetration-testing/)
that there is no such thing as "automated" penetration testing.)
But testing the app from the outside is not the only way in pen testing.
There is also manual [secure code review](../../solutions/secure-code-review/)
to find recurrent issues
like credentials in the source code and service misconfiguration.
So, we recommend
that you go beyond the advice of "regular" penetration testing
and **make it a continuous activity** throughout the SDLC.

By using our [Penetration Testing solution](../../solutions/penetration-testing/),
you can enjoy the following benefits:

- A more complete understanding of vulnerabilities
  through the expert support of our ethical hackers.

- A combination of automated and manual security testing
  that guarantees the detection of critical severity vulnerabilities,
  yielding very low rates of false positives and false negatives.

- Up-to-date knowledge about your app's security status,
  by requesting us to do pen testing continuously
  as the cloud-native software evolves,
  which is known as
  [penetration testing as a service](../what-is-ptaas/) (PTaaS).

- The option to request of us to break the build
  so that vulnerable builds that violate your organization's policies
  are prevented from going into production.

- Unlimited reattacks by our hackers without extra charge (i.e.,
  to verify whether vulnerabilities have indeed been remediated).

**Red teaming** is also a simulation of genuine attacks,
but it comes even closer to reality.
For instance,
it does not stop at assessments at the technological level,
but it involves testing at the human level as well.
This is part of a holistic approach
to find out the effectiveness of an organization's attack prevention,
detection and response strategies.
Accordingly,
in red teaming,
the attacks are performed with the executive leadership's consent,
but most people on the incident response team
and employees are not aware of that.
And another feature that makes it more realistic
is that the [red team](../what-is-red-team-in-cyber-security/)
is not focused on finding all the vulnerabilities
but rather set on specific objectives.

By using our [Red Teaming solution](../../solutions/red-teaming/),
in addition to those of our Penetration Testing solution,
you can enjoy the following benefits:

- Attack simulations that are highly realistic,
  as they mimic adversarial actors' tactics, techniques and procedures.

- A broad view of your organization's security
  through the assessments of ethical hackers with advanced
  [certifications](../../certifications/) (OSEE,
  CRTO, CRTE and CARTP).

You get a constantly updating view of all the findings
on our [Attack Resistance Management platform](../../platform/) (ARM).
There,
we map all your organization's digital assets,
and you can track their risk exposure over time.
You can also see the evidence of exploitation of technical vulnerabilities,
assign their remediation to members of your team,
talk to our hackers for guidance,
and many other things.

Now's the time to begin Azure [DevSecOps](../../solutions/devsecops/)
with `Fluid Attacks`.
[Contact us](../../contact-us-demo/)\!

Unsure?
Give our automated security testing a try
for [free for 21 days](https://app.fluidattacks.com/SignUp).
You can upgrade anytime to add manual security testing.
