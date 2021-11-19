---
slug: iso-iec-30111/
title: And Don't Forget ISO/IEC 30111
date: 2021-02-12
subtitle: Guidelines for the vulnerability handling processes
category: politics
tags: cybersecurity, standard, vulnerability, information, company, challenge
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330932/blog/iso-iec-30111/cover_i6aiku.webp
alt: Photo by Cristofer Jeschke on Unsplash
description: This post is related to vulnerability handling processes
  (ISO/IEC 30111), complementing the previous writing on vulnerability
  disclosure (ISO/IEC 29147).
keywords: Standard, ISO, Vulnerability, Handling, Verification, Remediation,
  Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/8ZfTxdPvNos
---

A few days ago, I brought readers some highlights [on the ISO/IEC
29147:2018 standard](../iso-iec-29147/) that guides us in the
vulnerability disclosure processes. (If you haven’t read that post, I
recommend that you do so before continuing with this one.) These
processes mainly involve receiving security issues reports as a vendor
and releasing repair advisories to all stakeholders. They’re two points,
beginning-ending, of a course of action between which it is necessary to
address the vulnerabilities in your systems. As a vendor, you have to
verify that what the reporter informed you of is a real security issue
and, if so, you need to come up with a solution asap. This is the topic
covered by [the ISO/IEC 30111:2019
standard](https://www.iso.org/standard/69725.html). And I’ll talk about
it in this post.

'Information technology -Security techniques- Vulnerability handling
processes' is the name of this standard. Like [the
ISO/IEC 29147](https://www.iso.org/standard/72311.html), it’s in the ISO
[standards
catalog](https://www.iso.org/standards-catalogue/browse-by-ics.html) in
group **35** '[Information technology](https://www.iso.org/ics/35/x/),'
subgroup **35.030** '[IT Security (including
encryption)](https://www.iso.org/ics/35.030/x/).' As stated in its
intro, it "describes processes for vendors to handle reports of
potential vulnerabilities in products and services." Thus, as may
already be clear, everyone should use it in line with that one of
vulnerability disclosure. Beyond the handling of reports, it also covers
requirements and recommendations for the procedures of examination,
triage, and repair of flaws.

## Policies

As a prior step, vendors should create and maintain **vulnerability
handling policies** for a commitment to the security of their products
or services. Of course, also for the benefit of their customers or
users. ISO suggests that vendors make clear their plans to study and fix
security issues to all interested parties. These policies should be
continuously reviewed, updated, and improved by the managers of each
organization. Part of the policies should be directed to vendors' staff.
This, to give them basic guidelines, roles, and duties in handling
reports and vulnerabilities. It’s of utmost importance that all
concerned people also get caveats to ensure the privacy of data about
flaws prior to repair.

## Organizational scheme

ISO recommends that vendors build their **vulnerability handling
processes**. They should assess them very often to be always ready to
deal with reports and security issues. Every firm should have a file
where all these processes remain faithfully recorded for prospective
replication and possible optimization. Besides, they should always
ponder a proper union of these operations with their other procedures.
They should ensure that the required means for the intended ends are
available all the time.

Firms ready for handling vulnerabilities set authorities to be aware of
the internal processes, goals, and frameworks and make decisions at the
control level. It’s apt for these organizations to have points of
contact for communications with internal departments and external
parties concerned with the issues disclosure and handling processes. Not
to mention being ready to get and respond to questions from customers
and other interested people when info about security weaknesses has
already been made public.

At this point, those units mentioned by ISO as "product security
incident response teams" (PSIRT) stand out. Apart from their activities
as points of contact and supervisors of disclosure procedures, these
teams may help with the vulnerability assessments of vendors' products
and services. Their help should include tracking flaws found in
third-party suppliers' software components that may impact the
operations and assets of the vendors in consideration. In addition,
PSIRT staff should understand the pertinence of maintaining
confidentiality before flaw remediations are carried out and notifying
'product business divisions' for proper action.

Product business divisions, those that give products or services to
vendors' clients, are also responsible parties in vulnerability handling
processes. These divisions get flaw reports from PSIRT and should work
with them in the development of remediations. After these are ready, the
"customer support divisions" are in charge of sending corresponding
advisories to customers and other stakeholders. A matter of
vulnerability disclosure processes, which appears in ISO/IEC 29147.

## Vulnerability handling process

Now, something that can serve as a guide for firms to establish their
vulnerability handling processes. Let’s check what ISO shares for the
phases of verification and repair of flaws.

<div class="imgblock">

![Kovah](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330931/blog/iso-iec-30111/kovah_yh3gmn.webp)

<div class="title">

Figure 1. Photo by
[Kovah](https://unsplash.com/@kovah?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on [Unsplash](https://unsplash.com/photos/MVjTry-e8MQ).

</div>

</div>

### Verification of vulnerabilities

After receiving a report of a potential flaw, the vendor has to verify
it. Here’s where the study begins to confirm the weakness. Also, to
determine the affected product or service, the security issue’s
severity, and the root cause. If it’s necessary, the vendor should
demand further proof from the reporter. When verification shows that the
flaw is a duplicate, has no security implications, or is in an obsolete
or external product, the vulnerability handling process must be broken
off. Of course, if other vendors are compromised, the issue should be
prudently reported to them.

It’s useful ISO’s emphasis on the continuous change in the
exploitability of flaws resulting from advances in attack techniques.
Another vital aspect to consider in verifications, usually when various
vulnerabilities have been reported, corresponds to triage. "Vendors may
consider several factors in determining the relative urgency of
producing a remediation, such as potential impact, likelihood of
exploitation, and the scope of affected users." Finally, after the flaw
verification, reporters should gain data about the results.

### Repair of vulnerabilities

Vendors need to establish either partial or total remediations to the
vulnerabilities they’ve already verified. While the repair is expected
to be generated fast, vendors should keep this in balance with the
amount of testing required to ensure the product’s or service’s high
quality. Quick and temporary remediations usually take place when the
issues show critical or high-risk levels for users. (They should receive
constant assistance.) In association with this, it may be necessary for
vendors to disable at-risk apps for a period of time.

As for the tests to be carried out with the repairs, vendors should
ensure evaluation on the corresponding platforms. Plus, their results
should be enough proof of the absence of new flaws and operational and
quality obstacles in products or services. Repair that doesn’t work is
one that needs to be rethought.

After releasing the vulnerability remediations, vendors should keep
updating them until it’s no longer required. On the other hand, vendors
should check their software and make proper renewals based on the data
gained during the study. All this is in order avoid similar security
flaws in their products or services.

To finish, it’s worth highlighting the **monitoring activity** for the
vulnerability handling processes suggested by ISO. Every firm or vendor
should always keep track of (and be ready to improve) the speed at which
they respond with verifications and repairs. They should also supervise
that their remediations are full and that the results are as expected at
the end of each case. All of this, it’s hoped, should go hand in hand
with a confidential treatment of vulnerability info and individuals' and
organizations' sensitive data.

Would you like to know how [`Fluid Attacks`](../../) can help you in
your vulnerability handling processes? [Don’t hesitate to contact
us\!](../../contact-us/)

**P.S.** Several essential details are missing in this post. If you’re
really interested in vulnerability handling, we recommend that you read
the entire [ISO/IEC 30111:2019](https://www.iso.org/standard/69725.html)
doc.
