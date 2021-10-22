---
slug: compliance/owasp/
title: OWASP
category: compliance
description: At Fluid Attacks, through comprehensive analysis,
    we can help you comply with a variety of security standards
    for information technology, including OWASP.
keywords: Fluid Attacks, OWASP, Top 10, Continuous Hacking,
    Security, Standards, Ethical Hacking, Pentesting
banner: bg-compliance-internal
template: compliance
---

<div class="sect2 fw3 f3 lh-2">

### How can Fluid Attacks help with OWASP compliance?

Ensuring compliance with up-to-date security standards
may become a complicated issue
for diverse organizations that use
continually evolving information technology for their businesses.
`Fluid Attacks` recognizes this
and offers you comprehensive testing and analysis
to determine whether your company is effectively complying
with all the corresponding security requirements.

`Fluid Attacks'` [Continuous
Hacking](../../services/continuous-hacking/) service tests
around 200 technical security requirements in each of your projects.
These requirements include preventing
OWASP Top 10 Web Application Security Risks.
We guarantee the detection
of all vulnerabilities in your software associated with such risks.
In addition,
we provide you with reliable reports
so that your team can take the necessary steps
to adjust
and maintain your information systems in line with OWASP requirements.

All our security testing is based on
[Criteria](https://docs.fluidattacks.com/criteria/), which is a set of
security requirements written by us in a comprehensible manner,
using several international standards as a reference.
It allows you to
parameterize the assessments we make to your systems and determine
what your company agrees to comply with
and what would be considered a vulnerability.

</div>

<div class="sect2 fw3 f3 lh-2">

### What is the OWASP?

The Open Web Application Security Project ([OWASP](https://owasp.org/)),
of which `Fluid Attacks` [is a corporate member](https://owasp.org/supporters/list),
is a non-profit foundation
that is committed to improving the security of software
and it does so
by creating awareness through different means of communication.
The OWASP works as an online,
open community
where anyone can contribute to the production of material
in the field of web application security
and also take advantage of the available information.
Their repository is useful for companies
that develop or manage web applications,
since it relies on the knowledge
of many global community members
with extensive experience in cybersecurity.

</div>

<div class="sect2 fw3 f3 lh-2">

### What is the OWASP Top 10?

The OWASP Top 10 refers to a cybersecurity guide
by the OWASP community
that is created as a collaborative effort between experts
and serves both developers
and security professionals in their projects.
This guide,
with a [current version](https://owasp.org/Top10/) from 2021,
lists the ten most common and critical security risks in web applications
and provides practical information for their prevention or remediation.

The idea with this ranking is to help reduce
the presence of flaws in web applications
that can be easily exploited
and generate terrible impact.
Organizations should always be careful
not to bring into production
applications with vulnerabilities related to these security risks,
making sure to pay attention to the most prevalent risks
in their specific industry sector.
Here we show you the current list of risks
with a brief description of each one (for more information see
the [official report](https://owasp.org/Top10/)):

<div class="sect3 owasp-col fl">

#### 1. Broken Access Control

Web applications need to establish limits for access to data
and functions
depending on the type of user.
When that is not done properly,
attackers can [circumvent misconfigured](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
(sometimes simply non-existent) access restrictions
and operate as any user, including administrators.

</div>

<div class="sect3 owasp-col fr">

#### 2. Cryptographic Failures

[This problem](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/) occurs
when applications fail
to protect data with adequate and modern encryption techniques or algorithms,
use weak or predictable encoding for passwords
or do not have sufficient protection for sensitive data (e.g., financial data).
It leaves information assets easily accessible for attackers
that can obtain them for illegal activities.

</div>

<div class="sect3 owasp-col fl">

#### 3. Injection

A code [injection](https://owasp.org/Top10/A03_2021-Injection/) occurs
when an application does not properly validate
or sanitize user-supplied input
and this can be leveraged
to make it process the input as code.

</div>

<div class="sect3 owasp-col fr">

#### 4. Insecure Design

[This risk](https://owasp.org/Top10/A04_2021-Insecure_Design/) refers
to a lack of security controls to defend against attacks
and failure to establish a secure development lifecycle.

</div>

<div class="sect3 owasp-col fl">

#### 5. Security Misconfiguration

[This category](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/) refers
to the inappropriate configuration of the application’s components,
leaving things like default accounts
or unnecessary features enabled
or allowing overly informative error messages to be returned to users.
Attackers can gain access through these accounts or features
or attempt to exploit unpatched flaws
inferred from the information exposed in error messages.

</div>

<div class="sect3 owasp-col fr">

#### 6. Vulnerable and Outdated Components

Web applications commonly use various open-source
and third-party components
in which vulnerabilities are sometimes found
and need to be patched.
[Keeping outdated versions](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/) 
of those components with known vulnerabilities
leads to having an application exposed to exploitation.

</div>

<div class="sect3 owasp-col fl">

#### 7. Identification and Authentication Failures

Attackers can take advantage of [vulnerabilities related to](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) custom authentication schemes,
exposure and reuse of session identifiers,
as well as non-existent password policy
to gain access to user accounts and compromise the system.

</div>

<div class="sect3 owasp-col fr">

#### 8. Software and Data Integrity Failures

[This](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/) occurs
when the software used to develop the application
is not checked to come from a trusted source
and have digital signatures
or when unencrypted serialized data is sent
without some form of integrity check.
This heightens the risk of malicious code or data
being introduced into the software pipeline.

</div>

<div class="sect3 owasp-col fl">

#### 9. Security Logging and Monitoring Failures

When applications [do not sufficiently log](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
issues and events within them
or do not create usable logs
or these logs are not sufficiently monitored,
data breaches might not be detected until months later
when attackers have already done a lot of damage.

</div>

<div class="sect3 owasp-col fr">

#### 10. Server-Side Request Forgery (SSRF)

[These flaws](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/) occur
whenever an application does not validate the user-supplied URL
when fetching a remote resource.
This allows the attacker
to coerce the application
to send a crafted request to an unexpected destination.

</div>

</div>

<div class="sect2 fw3 f3 lh-2">

### OWASP Benchmark Project v1.2

Our SAST tool achieved the best possible result
against the OWASP Benchmark:
A TPR (True Positive Rate) of 100%
and an FPR (False Positive Rate) of 0%.

![OWASP benchmark
clnlip](https://res.cloudinary.com/fluid-attacks/image/upload/v1619725547/airs/compliance/OWASP_benchmark_clnlip.webp)

</div>