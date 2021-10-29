---
slug: advisories/policy/
title: Disclosure Policy
description: This Disclosure Policy describes the details referring
  to the parameters used by Fluid Attacks
  on disclosing public vulnerabilities.
keywords: Fluid Attacks, Disclosure, Policy, Vulnerability, CVE, ISO
---

#### *This document was last updated on May 3, 2021*

This disclosure policy ("Policy") describes how `Fluid Attacks` ("Fluid
Attacks", "we", "us" or "our") discloses third-party product
vulnerabilities found by our Offensive Team.

This Policy does not apply to vulnerabilities found for customers as
part of the [Continuous Hacking](../../services/continuous-hacking) and
[One-Shot Hacking](../../services/one-shot-hacking) services, unless
there is explicit approval, as they are covered by a Non-Disclosure
Agreement.

## Goal

`Fluid Attacks'` commitment is to find all vulnerabilities and report
them as soon as possible. In order to accomplish this, we adhere to the
[ISO/IEC 29147:2018](https://www.iso.org/standard/72311.html) and
[ISO/IEC 30111:2019](https://www.iso.org/standard/69725.html) standards,
which describes the accepted responsible disclosure and vulnerability
handling guidelines to ensure the maximum benefit for vendors, customers
and the community in general. This includes:

- Providing the maximum level of detail on the vulnerabilities found
  in a way that the vendors are able to reproduce the problem.

- Ensuring coordinated disclosure of the vulnerabilities with the
  affected vendors, minimizing the damage that can occur with early
  disclosures.

- Releasing the details of the vulnerabilities on our
  [Advisories](../) page, including a risk level score using [CVSS
  v3.1](https://www.first.org/cvss/calculator/3.1) and proof of
  concept artifacts.

This leads to an overall risk reduction for the users.

## Scope

`Fluid Attacks` will apply this Policy to disclose third-party product
vulnerabilities to whom we will issue CVE IDs and that are not in the
scope of another CNA (CVE Numbering Authority).

The vulnerability types that we would process are the ones defined in
our [findings classification](https://docs.fluidattacks.com/types/).
However, vulnerabilities that don’t fit on this classification will be
also reviewed if there is an evidenced risk.

## Disclosure process

`Fluid Attacks` is always looking for vulnerabilities. Once our team
finds a new unpublished vulnerability, we will proceed as follows:

1. An initial report is created with all the details of the
    vulnerability and with any applicable proof of concept.

2. If the vulnerability is found through our [Continuous
    Hacking](../../services/continuous-hacking) or [One-Shot
    Hacking](../../services/one-shot-hacking) services, it will be
    reported only to the affected customer via our Attack Surface
    Manager (ASM).

3. If the vulnerability is found by our Research Team on a third-party
    product, the report will be sent to the affected vendor.

4. A new advisory draft is created on our [Advisories](../) page
    containing only the product affected, the report’s current status
    and the timeline. We will update it at each relevant event around
    the vulnerability (vendor reply, patch availability, proof of
    concept availability, on-wild exploitation indicators, etc.).

5. We will wait up to five (5) days for the vendor to acknowledge the
    report. If there is no response in that time, we will proceed with
    our [Responsible Disclosure](#Responsible_disclosure) process.

6. If the vendor acknowledges the report but there are no updates on
    the issue after fifteen (15) days, we will proceed with our
    [Responsible Disclosure](#Responsible_disclosure) process.

7. Otherwise, we can arrange a coordinated vulnerability disclosure
    with the vendor. We suggest this to be done in no more than ninety
    (90) days after the discovery.

`Fluid Attacks` also reserves the right to disclose the vulnerability at
any time in cases where early disclosure would provide benefits to
stakeholders.

## Responsible disclosure

Vulnerability disclosure is performed according to the parameters
described above. The process is as follows:

1. The advisory draft on [Advisories](../) will be updated with the
    details of the vulnerability and any relevant proof of concept.

2. If necessary, a new CVE will be issued.

3. The advisory will be published to relevant public email lists,
    social media or [blog](../../blog/) posts.

## References

- [ISO/IEC 29147:2018](https://www.iso.org/standard/72311.html)

- [ISO/IEC 30111:2019](https://www.iso.org/standard/69725.html)

### Contact

If you would like to contact us to learn more about this Policy or to
discuss any matter related to it, please send us an email to

<div class="imgblock">

![Help](https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,w_200/v1620228481/airs/advisories/help_usssdq.webp)

</div>
