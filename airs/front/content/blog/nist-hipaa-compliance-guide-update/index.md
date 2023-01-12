---
slug: nist-hipaa-compliance-guide-update/
title: NIST Updates Its HIPAA Guidance
date: 2022-07-27
subtitle: Advice for firms to comply with the HIPAA Security Rule
category: politics
tags: cybersecurity, compliance, risk
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1658935999/blog/nist-hipaa-compliance-guide-update/cover_hipaa.webp
alt: Photo by Sander Sammy on Unsplash
description: NIST published the second revision draft to its SP 800-66. Learn about the most significant changes that are being introduced.
keywords: Hipaa, Nist, Security Rule, Risk Assessment, Healthcare, Standard, Compliance, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/38Un6Oi5beE
---

On July 21,
the National Institute of Standards and Technology (NIST)
published the draft of a new update to its guidance
for implementing the Security Rule
of the Health Insurance Portability and Accountability Act (HIPAA).
The update is intended to help the healthcare industry enhance its controls
to safeguard the health information of patients.

In this blog post,
we bring you the most significant changes to this standard
with some hints on what you can start implementing
to update your compliance.

## What's NIST guidance for compliance with the HIPAA?

Let's first review what the HIPAA is.
We're talking about a federal law that dates back to 1996.
It requires the creation of standards
that regulate and improve the handling of Protected Health Information (PHI).
This kind of information may be understood as any data
that could be used to identify a patient.
For example,
**lab results**,
**prescriptions**,
**hospital visits**
and **vaccination records**.
Following this legislation would mainly ensure
that PHI is not disclosed without a patient's knowledge or consent,
thus minimizing the risks of theft and further fraud.

The [NIST draft](https://doi.org/10.6028/NIST.SP.800-66r2.ipd)
we're dealing with in this post is for the second revision
to NIST Special Publication (SP) 800-66.
It focuses on compliance with the HIPAA Security Rule.
This rule protects electronic PHI (ePHI) that health plans,
healthcare clearinghouses
and healthcare providers
(henceforth,
"regulated entities")
create,
receive,
maintain
or transmit.
According to the [NIST news](https://www.nist.gov/news-events/news/2022/07/nist-updates-guidance-health-care-cybersecurity),
the idea with this revision is to give **more actionable guidance**.
(Below,
we'll touch on how this is accomplished.)
Further,
the draft gives an **increased emphasis on risk management**.

## What's new in the NIST SP 800-66 Rev. 2 draft?

NIST intends to catch up to its [Cybersecurity Framework](https://doi.org/10.6028/NIST.CSWP.04162018)
(CSF) publication,
which was released years after the first revision to SP 800-66.
The new draft publication **maps the elements of the Security Rule
to NIST CSF subcategories**.
Additionally,
it updates the mapping to controls
in NIST's Security and Privacy Controls for Information Systems
and Organizations ([SP 800-53](https://doi.org/10.6028/NIST.SP.800-53r5)).
This is shown in a comprehensive table in the draft's Appendix E.
As regulated entities are pointed to these further resources,
they can have an even more specific idea
of what security requirements they need to check.

As hinted,
another remarkable feature of this draft is its emphasis
on the assessment of risk to ePHI
as a fundamental process in an entity's compliance with the Security Rule.
The draft **dedicates a section to risk assessment**,
placed strategically just before the risk management guidance,
instead of only an appendix,
as in the previous revision.
Accordingly,
it is more specific in its description of the different steps involved
and provides more resources.
Worthy of note are the several examples of threat events
characterized by tactics,
techniques
and procedures (Appendix C).

Although the names of the steps have changed somewhat,
it is the result of merging or separating them.

<div class="imgblock">

![Comparison between the NIST SP 800-66 rev. 1 and rev. 2](https://res.cloudinary.com/fluid-attacks/image/upload/v1658936600/blog/nist-hipaa-compliance-guide-update/Figure_assessment.webp)

</div>

By the way,
the draft **makes it clear
that the identification of technical vulnerabilities should be done
with an appropriate methodology**.
Bear in mind that assessments carried out
with automated security testing tools alone
fail to detect risk exposure accurately.
In our latest [State of Attacks](https://try.fluidattacks.tech/state-of-attacks-2022/)
report,
we show
that **67.4%** of the risk exposure reported
in the systems we evaluated throughout the last year
was identified only by our [ethical hackers](../what-is-ethical-hacking/).

Another welcome addition is
that this new revision **acknowledges the importance
of continuous risk assessment**.
It's made explicit that,
in order to execute a risk management strategy,
regulated entities should conduct risk assessment as an ongoing task.
We believe this advice is on point.
Systems should be subjected to continuous [security testing](../../solutions/security-testing/)
so that it can be proven whether they can withstand emerging threats.

For the next feature,
it's important to clarify something first.
The Security Rule categorizes actions,
policies
and procedures
to protect the confidentiality,
integrity
and availability of ePHI
into three "Safeguards."
Namely,
Administrative (e.g., periodic reviews),
Physical (e.g., restrictions to access to facilities and software)
and Technical (e.g., PHI encryption) Safeguards.
The NIST draft publication's key activities associated with Safeguards
remain basically the same,
save for the fact
that the draft **gives a richer description of the key activities
and relies more heavily on the risk assessment results**.

What we've described so far —providing many more resources,
placing risk assessment under the spotlight,
keeping up with the trends
and being more exhaustive— makes this guidance a more actionable one
in comparison with the previous revision.

To name a few other changes,
scenarios in the implementation advice have been updated
(e.g., to include telehealth)
and some successful practices are given more emphasis than before
(e.g., NIST is a little more insistent
on implementing multi-factor authentication solutions).
Finally,
the enhancements to the guidance may encourage regulated entities
to set stricter standards
(e.g., defining time frames
and clearer responsibilities regarding the investigation
and reporting of security incidents and breaches).

NIST is receiving comments on its draft publication until September 21.
In the meantime,
you should take a look at the document
and see the actions you can take to step up your cybersecurity game.

At `Fluid Attacks`,
we help you develop technology
that [complies with the HIPAA](../../compliance/hipaa/)
and many more security standards.
Don't hesitate to [contact us](../../contact-us/)\!

<caution-box>

**Caution:**
Many major details from the publication are missing in this blog post.
Having read this post in no way substitutes
for careful reading of the NIST SP 800-66 Rev. 2 (Draft).
If you need to know all the details,
we recommend that you read the
[full text](https://doi.org/10.6028/NIST.SP.800-66r2.ipd).

</caution-box>