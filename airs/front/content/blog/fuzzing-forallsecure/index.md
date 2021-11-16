---
slug: fuzzing-forallsecure/
title: Continuous Search for the Unknown
date: 2020-03-31
subtitle: ForAllSecure on the Next-Generation fuzzing
category: opinions
tags: fuzzing, cybersecurity, security-testing, hacking,
  vulnerability, business
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330878/blog/fuzzing-forallsecure/cover_vfq8ht.webp
alt: Photo by David Kovalenko on Unsplash
description: "This post is based on the information given on February 11th
  by Brumley (ForAllSecure) in his webinar 'Continuous Fuzzing:
  The Trending Security Technique.'"
keywords: Fuzzing, Cybersecurity, Security Testing, Hacking, Vulnerability,
  Business, Pentesting, Ethical Hacking
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/G85VuTpw6jg
---

First of all, we give you the links where you can find [the webinar
video](https://www.brighttalk.com/webcast/17668/385891/continuous-fuzzing-the-trending-security-technique)
and [the copy of the
document](https://go.forallsecure.com/hubfs/Content/Whitepapers/FY19%20WP%20What%20is%20NGF%20v5.0.pdf)
—both from ForAllSecure. Almost everything expressed below is based on
both sources.

In the field of software security, the aim is always to deploy code that
is free of vulnerabilities. Mainly since malicious attackers often
target such program and system failures.

A company’s software can be entirely trustworthy because of the security
methods that are employed in that company. That is something Google can
be proud of, for example, with their Chrome browser.

According to Brumley, Google and Microsoft are among the organizations
that practice a new security testing methodology. They act within a new
generation scheme, following a process similar to that which a real
hacker would follow.

But before we make an overview of this process, let’s put it in context.

Security tests tend to be thought of as being carried out at specific
times. For example, as soon as a program has been developed and before
it is available to users. What the use of testing is intended to find is
the presence of vulnerabilities.

Vulnerabilities may correspond to mistakes that developers made in their
work with code. These vulnerabilities can be classified as *known*,
*unknown*, and *zero-day*.

*Known* vulnerabilities are those that have already been disclosed to
the security communities and software vendors. *Unknown* vulnerabilities
are those that have not been discovered by anyone. And *zero-day*
vulnerabilities have already been found by some subjects, but have not
been disclosed to vendors or communities.

Vulnerability detection can be done with `SAST`, `DAST`, or a mixture of
both techniques (*grey-box* testing).

If we take the first one, we’re referring to **Static Analysis Security
Testing**. This form of *white-box* testing uncovers vulnerabilities
through an analysis of the source code when the software is in a
non-running state.

The second technique is the **Dynamic Analysis Security Testing**, which
corresponds to a form of *black-box* testing that uncovers
vulnerabilities by analyzing software in a running state without
accessing the source code.

Almost all static and dynamic analysis tools search for known
vulnerabilities or test for known attack patterns. For the discovery of
unknown or zero-day vulnerabilities, it is necessary to perform negative
testing.

**Negative testing** is a form of verification and validation testing
(process to guarantee that apps operate as expected). Contrary to
positive testing, in this process, an invalid set of inputs is sent to
the application. In this instance, it must be verified that the app
remains stable in the face of unexpected use. Combinations of invalid
inputs can be almost infinite, so testing them all before deploying the
application may be unlikely.

It is here that the use of **continuous hacking** appears as
recommended, a process that goes beyond one-pass checks. While people
use the software and hackers try to find the vulnerabilities, continuous
hacking is conducted as a security testing, and it is performed as the
software evolves.

Concerning the negative testing, we can then mention **continuous
fuzzing**. As [Ispoglou et al.
(2019)](https://nebelwelt.net/files/20SEC.pdf), from Google, share:
"Fuzzing is a testing technique to discover unknown vulnerabilities in
software."

Microsoft and Google are using a **"Next-Generation fuzzing,"** a
dynamic analysis technique (really under grey-box testing category) that
can look for unknown vulnerabilities, and that following Brumley is
located in the last quadrant, we can see here in Figure 1:

<div class="imgblock">

![taken from ](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330877/blog/fuzzing-forallsecure/corners_rlubyg.webp)

<div class="title">

Figure 1. taken from [the PDF of the
webinar](http://public2.brighttalk.com/resource/core/253964/2019---isaca-presentation-v21-brighttalk_558794.pdf)

</div>

</div>

Fuzzing can also detect known and zero-day vulnerabilities. With the use
of invalid inputs, *fuzzers* are intended to provoke anomalous behaviors
in the software, such as memory leaks, infinite loops, and crashes.
These behaviors may be linked in some way to underlying vulnerabilities.

There are four categories in which we can divide fuzzing:

- In **Random** fuzzing, random inputs are sent to an application.
  Many of the inputs fail to penetrate the app, so there is low code
  coverage.

- In **Template** fuzzing, customized inputs are employed, and they
  are modified to include the irregularities. Within this category,
  compared to the previous one, the penetration to an application is
  more probable. However, the fuzzing process is limited to the scope
  of the template.

- For the **Generational** fuzzing, engineers develop lots of test
  cases written to resemble a valid input. Some *fuzzers* of this type
  can prioritize test cases based on feedback from the target, which
  can increase the chances of penetration and of triggering anomalous
  behavior.

- In **Evolutionary** fuzzing, the *fuzzers* are intelligent. They
  have the ability to monitor and leverage the behavior of the target
  for the automatic generation of new custom test cases during the
  process. Besides, they don’t get test cases to begin with.

More in line with this last category, the **Next-Generation fuzzing**
works with random guessing, and the *fuzzer* learns as it automatically
runs the program. The *fuzzer* tries to explore all paths, and never
repeat any of them twice, always moving on to a new one. The automatic
generation of new test cases, thanks to feedback on the target’s
reactions, can help in the discovery of more defects and new code edges.

That process can be quite useful in finding the vulnerabilities before
the attackers do. And that is something that many organizations are
currently requesting.

For the sake of improving their cybersecurity, companies should
understand that simple tests and scans, with predetermined paths, and at
specific times, may limit the findings of vulnerabilities. Companies
must be aware that: whether through automatic systems or manual work,
continuous hacking will always mean more depth and thoroughness in the
search for vulnerabilities.

Would you like to know about `Fluid Attacks` [continuous
hacking](../../services/continuous-hacking/) services? [Contact
us](../../contact-us/).
