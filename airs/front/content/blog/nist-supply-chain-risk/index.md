---
slug: nist-supply-chain-risk/
title: Advice From the NIST SP 800-161
date: 2022-05-16
subtitle: Key practices for managing cyber supply chain risk
category: politics
tags: compliance, cybersecurity, risk, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1652708289/blog/nist-supply-chain-risk/cover_nist.webp
alt: Photo by Jonathan Cosens Photography on Unsplash
description: In this blog post, we summarize some of the NIST's suggested key practices to manage cybersecurity supply chain risk.
keywords: Standard, Nist, Supply Chain Risk, Key Practices, Guidelines, Policy, Software Composition Analysis, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/TNTx5XKzcjg
---

One year ago,
the U.S. President's [Executive Order 14028](https://www.federalregister.gov/documents/2021/05/17/2021-10460/improving-the-nations-cybersecurity)
on improving the nation's cybersecurity
included enhancing software supply chain security as one of its items.
The directive followed the [SolarWinds](../solarwinds-attack/)
and [Microsoft Exchange Server](../exchange-server-hack/) incidents.
But the threat of supply chain attacks still holds to this day,
mainly for managed service providers (MSP).
These firms deliver,
operate
or manage information
and communications technology (ICT) services to other firms.
In fact,
last week,
the Cybersecurity and Infrastructure Security Agency (CISA),
along with other cyber intelligence agencies of the U.S.,
Canada,
the U.K.,
Australia and New Zealand,
[posted](https://www.cisa.gov/news/2022/05/11/joint-cybersecurity-advisory-protect-msp-providers-and-customers)
actions that MSPs should take
to improve resilience of the global supply chain.

In the Executive Order,
the National Institute of Standards and Technology (NIST)
was asked to solicit input from different sectors,
like government agencies,
private firms
and academia,
to identify practices
that could enhance the security of the software supply chain.
What is more,
it was responsible for issuing preliminary guidelines,
which it did in November last year.
And early this month,
it issued an update
on the *Cybersecurity Supply Chain Risk Management Practices
for Systems and Organizations*
([*NIST Special Publication 800-161 Revision 1*](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-161r1.pdf)).

Let's consider the supplier relationship:
How one supplier gets components for their solution
from other suppliers,
and so on.
We can tell that each acquiring organization loses visibility,
understanding and control of its supply chain.
As they rely more and more on third-party components
to build their technology,
they need to become aware of the risk
and assess the security of each of their system components.
So,
in this blog post,
we will give you some of the key takeaways from the NIST publication.

<div class="imgblock">

![Reduced visibility of the supply chain](https://res.cloudinary.com/fluid-attacks/image/upload/v1652708733/blog/nist-supply-chain-risk/nist-reduced-visibility.webp)

<div class="title">

The NIST's depiction of an organization's reduced visibility,
understanding and control of its supply chain.
Taken from [nvlpubs.nist.gov](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-161r1.pdf).

</div>

</div>

## A matter entwined with enterprise risk management

One major step
that every organization must take
is to place cybersecurity on the boardroom agenda.
This will make it possible
for cybersecurity supply chain risk management (C-SCRM)
to be effectively addressed.
Indeed,
one of the challenges is to put the issue,
responsibilities and activities
in terms that are understandable for everyone.
The NIST aims to do this in the introduction
by suggesting what sections personnel at the executive,
management or practitioner level should read.

The contribution of some personnel to C-SCRM is expected.
For example,
developers are responsible
for identifying issues in software
and fixing them at early stages,
and engineers for designing products
and understanding requirements for open-source components.
But
the publication recommends
that everyone be aware of the supply chain risk
and linked policies and receive C-SCRM-related training.

In addition to trying to reach out to a vast public,
this publication acknowledges
that C-SCRM is a big issue to solve
which affects the entire enterprise.
And that is why
the NIST maps it to the overall enterprise risk management function.
Then,
the supply chain risk needs to be monitored,
quantitatively measured
and also be included in the firm's [incident response plan](../incident-response-plan/).

And one more important piece of advice in this publication
is for organizations to have policies
on acquiring systems from the supply chain
into their production environment.
For this,
they need to have steering committees for C-SCRM
to decide what is acceptable.
What different committees,
who could be on them
and what they would be responsible for can be defined
drawing inspiration from Table 2-1 in the publication.
It shows the generic stakeholders at each level and their activities.

## NIST supply chain key practices

Now,
on to the actual key practices
that the NIST describes in their publication.
They are broken down into three categories
and arranged in ascending order
according to their level of maturity.
Here,
we summarize a few selected items
that connect to the previously mentioned highlights.
However,
you can find all the practices in the publication
in section 3.4.

### Foundational practices

At a base level,
we have actions
that aim towards building a C-SCRM practicing capability.
They include the following:

- Obtaining senior leadership support for establishing C-SCRM.

- Implementing a risk management hierarchy and process.

- Developing a process to measure
  the criticality of the organization's suppliers,
  products and services.

- Integrating C-SCRM into products and services acquisition policies.

- Using supplier risk-assessment processes and threat
  and vulnerability analyses.

- Monitoring components of embedded software.

- Implementing quality assurance and quality control processes.

- Establishing internal checks
  to ensure compliance with security requirements.

- Implementing an incident response plan.

### Sustaining practices

These are more advanced actions
that revolve around how organizations can mature processes
mentioned in the previous segment.
The practices at this level include the following:

- Assessing the supplier's security capabilities
  and practices by looking at formal certifications
  (e.g., [ISO27001](https://docs.fluidattacks.com/criteria/compliance/iso27001/)),
  among other things.

- Continuously monitoring changes
  to the risk profile of the supplied products
  and services
  and the supply chain itself.

- Integrating C-SCRM requirements into contractual agreements
  with suppliers, developers, MSPs, etc.

- Involving critical suppliers in the incident response plan.

- Engaging with various agents,
  like suppliers and stakeholders,
  to improve their cybersecurity practices.

- Collecting C-SCRM metrics.

### Enhancing practices

These actions basically refer to the use of automation.
They include the following:

- Automating C-SCRM processes.

- Analyzing risk quantitatively with probabilistic approaches
  to find out the likelihood and impact of cybersecurity issues
  throughout the supply chain.

## Know what's in your software

Additionally to the practices summarized above,
our advice at `Fluid Attacks` is to search for vulnerabilities
in your software third-party components
and your own code
throughout the entire software development lifecycle.
Our automated and manual [Software Composition Analysis](../../categories/sca/)
helps you identify issues
that you can fix to prevent falling victim to supply chain attacks.
Want to know more?
[Contact us](../../contact-us/).

<caution-box>

**Caution:**
Many major details from the NIST publication are missing in this blog post.
Having read this post in no way substitutes
for careful reading of the NIST SP 800-161r1.
For a thorough understanding of the guidelines,
we recommend reading the
[original text](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-161r1.pdf).

</caution-box>