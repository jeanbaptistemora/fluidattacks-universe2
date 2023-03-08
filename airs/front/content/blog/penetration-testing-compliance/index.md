---
slug: penetration-testing-compliance/
title: Penetration Testing Compliance
date: 2023-01-19
subtitle: For which security standards is pentesting a must-have?
category: politics
tags: pentesting, compliance, cybersecurity, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1674158363/blog/penetration-testing-compliance/cover_compliance.webp
alt: Photo by Nik Shuliahin on Unsplash
description: "We present whether penetration testing is required for compliance with these security standards: GDPR, GLBA, HIPAA, ISO 27001, PCI DSS, SOC 2 and SWIFT CSCF."
keywords: Soc 2 Penetration Testing, Iso Penetration Testing, Glba Penetration Testing, Gdpr Penetration Testing, Hipaa Penetration Testing, Pci Dss Penetration Testing, Compliance, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/JOzv_pAkcMk
---

The need to protect sensitive information has resulted in regulations
in every industry.
Some of such regulations require conducting [penetration testing](../what-is-manual-penetration-testing/).
This offensive approach,
which mimics the behavior of malicious attackers,
can yield very accurate security testing results.
In this blog post,
we present whether penetration testing is required
by the international standards about which most people have this question.
However,
we stress the importance of going beyond basic compliance.

## What is penetration testing?

Penetration testing (or “manual” penetration testing)
is an approach to security assessment
that consists in simulating updated attack scenarios
to check the defenses of information technology systems.
Such an approach is possible only with human intervention,
where security professionals,
ethical hackers,
are the ones who know how malicious threat actors operate.
Thus,
pen testing goes beyond vulnerability assessments
(aka vulnerability scanning or vulnerability analysis)
done by tools only.
Leveraging automation alone leads to high rates of false positives
and false negatives,
which adds administrative burden to organizations' technical teams.
So,
when it comes to accuracy and cost saving,
pen testing has the upper hand.

## Penetration testing for regulatory compliance

### Is GDPR penetration testing compliance a thing?

The [General Data Protection Regulation](https://gdpr-info.eu/) (GDPR)
lays down rules relating to the protection of natural persons' data and privacy
within the European Union (EU) and the European Economic Area (EEA).
This applies even to companies
that,
operating outside those territories,
store, process or transfer personal information of EU and EEA citizens.

This standard requires firms to implement technical and organizational measures
to ensure a level of data security appropriate to the risks.
Further,
it mandates the testing of the effectiveness of such measures regularly.
Although penetration testing is not mandatory per GDPR,
it is an approach that,
simulating real-world attacks,
can accurately assess the confidentiality,
integrity, availability and resilience of systems.
For example,
some basic system requirements,
such as specifying the purpose of data collection
and respecting tracking preferences,
are not validated by automated tools.

At Fluid Attacks,
we check that your systems comply with security requirements
mapped to the [GDPR](https://docs.fluidattacks.com/criteria/compliance/gdpr).
These include effective data handling and privacy controls.

### Is GLBA penetration testing compliance a thing?

[Since December 2022](https://www.federalregister.gov/documents/2021/12/09/2021-25736/standards-for-safeguarding-customer-information),
**financial institutions are required
to conduct penetration testing** annually.
This is according to the U.S. Federal Trade Commission's final rule
on the Standards for Safeguarding Customer Information.
The Commission established these standards
as required by the Gramm Leach Bliley Act (GLBA),
which aims to regulate the privacy and data security practices of institutions
in the finance industry.

As the name of the Standards suggests,
institutions are required especially
to prove that their controls to safeguard customer information are effective.
One thing worth mentioning is
that the definition of information systems in the Standards
includes physical systems and employees.
Thus,
pen testers should use techniques such as [social engineering](../social-engineering/)
and [phishing](../phishing/) to test organizations' cybersecurity.

We help you with [GLBA compliance](https://docs.fluidattacks.com/criteria/compliance/glba)
by checking that your systems specify the purpose of data collection,
request user consent
and allow users to opt-out,
among other requirements.

### Is HIPAA penetration testing compliance a thing?

[HIPAA](https://www.hhs.gov/hipaa/for-professionals/index.html)
is a federal law,
according to which,
standards must be created
that regulate
and improve how entities handle Protected Health Information (PHI).
This kind of information refers to that which could be used
to identify a patient.
PHI can be lab results,
hospital visits,
prescriptions
and vaccination records.
Healthcare institutions,
and clearly every company that has patient data,
should ensure the confidentiality and security of the information
using proper administrative,
physical
and technical safeguards.

The use of penetration testing is advisable but not mandatory.
It is worth noting,
though,
that every organization benefits from testing their systems
against simulations of the behavior of malicious threat actors.
In this case,
we are talking about an industry
that has attractive attributes in the eyes of adversaries.
One of the main motivations
for attackers targeting healthcare institutions
is the high value for patient data.
A contributing factor may be the fact
that these entities often use legacy systems.
We know
that unpatched systems are easy targets,
since their vulnerabilities are probably known
and therefore exploited constantly by opportunistic threat actors.

We check
that your systems comply with [HIPAA](https://docs.fluidattacks.com/criteria/compliance/hipaa)-related
security requirements.
Among them are those concerning authentication,
authorization
and cryptography.

### Is ISO penetration testing compliance a thing?

[ISO/IEC 27001](https://www.iso.org/obp/ui/#iso:std:iso-iec:27001:ed-3:v1:en)
(or just "ISO 27001")
is developed by the ISO (International Organization for Standardization)
and the IEC (International Electrotechnical Commission).
It provides requirements for establishing,
implementing,
maintaining
and continually improving an information security management system (ISMS).
This ISO document is officially a standard
that can be used worldwide as the basis for formal compliance assessment
by accredited certification auditors.

The security controls that may be regarded as most relevant vary markedly
across industries adopting the ISO 27001.
So there is no one-size-fits-all set of controls to validate,
although there are items explicitly required for certification.
In this regard,
there _are_ clauses
that can justify the use of pentesting as the preferred approach.
One refers to the organization
determining its information risk assessment process.
The other,
refers to providing evidence of the monitoring
and measurement of information security.
We recommend penetration testing as an extremely suitable approach
to test organizations' defenses
against attacks that could realistically appear given their threat landscape.

Fluid Attacks tests compliance with several security requirements
mapped to the [ISO/IEC 27001](https://docs.fluidattacks.com/criteria/compliance/iso27001/).
They include legal,
privacy,
data handling,
source code
and network security requirements,
among others.

<cta-banner
  buttontxt="Read more"
  link="/solutions/penetration-testing/"
  title="Get started with Fluid Attacks' Penetration Testing solution
  right now"
/>

### Is PCI penetration testing compliance a thing?

The [Payment Card Industry Data Security Standard](https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0.pdf)
(PCI DSS)
is global and well known.
Its purpose is to prevent data theft
and fraud by securing debit and credit card transactions.
Basically,
every company that accepts,
processes,
stores
or transmits debit and credit card information
should achieve PCI DSS compliance.
Further,
certifying and communicating
that a company complies with this standard assures customers
that they can trust the company's application with their data.

**PCI DSS penetration testing compliance consists in performing external
and internal penetration testing regularly.**
Additionally,
the specific requirement asks companies
to correct the exploitable vulnerabilities and security weaknesses found.
And what does it mean by "regularly"?
That's conducting penetration testing at least once every year.
However,
service providers are required to prove
that their systems are assessed "at least once every six months
and after any changes to segmentation controls/methods."
This is because they generally have access
to greater volumes of cardholder information
or can be an entry point to compromise multiple other entities.

Fluid Attacks checks
that systems comply with security requirements
mapped to the [PCI DSS](https://docs.fluidattacks.com/criteria/compliance/pci).
These are related to data handling,
cryptography
and secure source code,
among others.

### Is SOC 2 penetration testing compliance a thing?

The American Institute of Certified Public Accountants (AICPA)
created the [System and Organization Controls](https://www.aicpa.org/resources/landing/system-and-organization-controls-soc-suite-of-services)
(SOC, aka service organizations controls)
to refer to reports produced during an audit.
SOC 2 shows the result of the evaluation of service organizations
based on five trust service criteria:
security,
availability,
processing integrity,
confidentiality
and privacy.
This standard is relevant to technology companies (e.g., SaaS companies)
that provide information systems as a service to other organizations.

Auditors checking compliance with the trust service criteria
are instructed by this standard to validate
whether the service organization assesses its systems' controls constantly
or on separate occasions.
Further,
the standard names penetration testing
as one acceptable type of such assessments.
Although SOC 2 penetration testing requirements are not clear
on the right frequency with which assessments should be conducted,
we recommend they are done continuously,
mimicking the constant flux of cyber threats.

We check security requirements
related to [SOC 2](https://docs.fluidattacks.com/criteria/compliance/soc2)
criteria in your systems.
These requirements include data handling,
device security,
authentication
and authorization controls,
among others.

### Is SWIFT CSCF penetration testing compliance a thing?

The [SWIFT Customer Security Controls Framework](https://www.swift.com/myswift/customer-security-programme-csp/security-controls)
(CSCF)
establishes mandatory and advisory security controls
to promote the security of the SWIFT interbank communications system.
SWIFT stands for "Society for Worldwide Interbank Financial Telecommunication,"
which enables financial transactions and payments between banks.

**This standard explicitly requires financial institutions
to perform penetration testing.**
This security approach is requested
to fulfill a specific control objective
of validating the operational security configuration
and identifying security gaps.
(You can download this standard's self-attestation form,
which mentions the need of performing pentesting,
by following this [link](https://www.swift.com/swift-resource/239601/download).)

We check your systems
for compliance with requirements related to the [SWIFT CSCF](https://docs.fluidattacks.com/criteria/compliance/swiftcsc).
These include the ones about authorization,
authentication
and third-party components,
among others.

## Do I need penetration testing compliance?

The fact of the matter is that if you are in an industry
that deals with sensitive client data,
you are required to conduct security testing.
Regardless of whether or not it is mandatory in your industry
to conduct penetration testing specifically,
you should know how selecting this approach is more sensible
than running vulnerability scanning _solely_.
Moreover,
we recommend
that you subject your systems to security testing continuously,
not just regularly.
Remember that threats are constantly evolving,
so,
during the time you are not testing,
you are most vulnerable to being breached.

If you were looking for a standard that is not in this blog post,
it probably is in our [Documentation](https://docs.fluidattacks.com/criteria/compliance/).
Feel free to [contact us](../../contact-us/)
if you have any compliance-related questions.

## How we help you with penetration testing compliance

Fluid Attacks performs continuous penetration testing
from the beginning and throughout the software development lifecycle.
Our [Penetration Testing solution](../../solutions/penetration-testing/)
is part of our all-in-one service,
[Continuous Hacking](../../services/continuous-hacking/).
In our assessments,
we check
that the target systems comply with several renowned international standards.
We help our clients go beyond compliance
by performing penetration tests continuously,
checking every version of their systems.
Our clients know
it's not enough to have just one penetration test per year or quarterly,
because they make changes everyday
and the threat landscape is also in perpetual evolution.

Continuous Hacking includes access
to our [Attack Resistance Management](../../platform/) (ARM) platform.
There,
users can see how well they comply with several standards.
Start your [**21-day free trial**](https://app.fluidattacks.com/SignUp)
to leverage our automated security testing
and explore the platform.
You can upgrade to include penetration testing.
