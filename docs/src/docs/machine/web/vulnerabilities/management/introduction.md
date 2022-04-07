---
id: introduction
title: Introduction
sidebar_label: Introduction
slug: /machine/web/vulnerabilities/management
---

With Fluid Attacks ASM you will
be able to visualize all the
details you need about your
reported vulnerabilities and
manage them effectively.
In the **Vulnerabilities** section,
you can select a specific type
of vulnerability and see in detail
how it is affecting your group.
At a glance you will be able to
tell **Where** in the
[ToE](/about/glossary#toe "Target of Evaluation")
is the vulnerability along with
a more specific location.

![Vulnerability Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1645455490/docs/web/vulnerabilities/management/managmt_vuln_section.png)

## Header of the type of vulnerability

In the **header** there are
useful global information.
Above the header, as a title,
you find the name of the type
of vulnerability you selected.
There are many kinds of errors
or problems that can exist in
a given software, as well as
many ways to exploit them.
All of these types of vulnerabilities
have specific names, and you
can access [a vast list](/criteria/vulnerabilities/)
that we are constantly updating on our
[Documentation](https://docs.fluidattacks.com/).

![Vulnerability Example](https://res.cloudinary.com/fluid-attacks/image/upload/v1645455490/docs/web/vulnerabilities/management/managmt_vul_example.png)

The first thing you see below
the title, on the far left, is
the **severity** level of that
type of vulnerability.
Specifically, it shows you a
number and its corresponding
qualitative rating.
The number is a score based on
the renowned Common Vulnerability
Scoring System (CVSS), an open
standard for assessing the
severity of security vulnerabilities
in IT systems.
CVSS scores go from 0.1 to 10.0.
The qualitative rating depends on
those scores: **low** from 0.1 to
3.9, **medium** from 4.0 to 6.9,
**high** from 7.0 to 8.9 and
**critical** from 9.0 to 10.0.

![Vulnerability Severity Level High](https://res.cloudinary.com/fluid-attacks/image/upload/v1645455489/docs/web/vulnerabilities/management/managmt_severity_lvl_high.png)

![Vulnerability Severity Level Medium](https://res.cloudinary.com/fluid-attacks/image/upload/v1645455489/docs/web/vulnerabilities/management/managmt_severity_lvl_medium.png)

![Vulnerability Severity Level Low](https://res.cloudinary.com/fluid-attacks/image/upload/v1645455489/docs/web/vulnerabilities/management/managmt_severity_lvl_low.png)

To the right of the severity,
you find the **status** of that
type of vulnerability.
It can simply be **open** or **closed**.
Open means that at least one of
the locations where we reported
that type of vulnerability has it
without being fixed.
On the other hand, closed means
that you remediated that security
issue in all those locations.

![Vulnerability Status](https://res.cloudinary.com/fluid-attacks/image/upload/v1645455490/docs/web/vulnerabilities/management/managmt_vuln_status.png)

Then, continuing from left
to right, you discover the number
of **open vulnerabilities**.
This number corresponds to how
many locations in your system still
have that type of vulnerability.
In the table below, you can precisely
find which files and code lines
are affected.

![Number Of Open Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1645455489/docs/web/vulnerabilities/management/managmt_numbr_open_vuln.png)

Next, you can see the
**discovery date**.
This is simply the year, month,
and day we first identified and
reported that type of vulnerability
for the group in question.

![Discovery Date](https://res.cloudinary.com/fluid-attacks/image/upload/v1645455489/docs/web/vulnerabilities/management/managmt_discovery_date.png)

The last item in the header is
the **MMTR (Mean Time to Repair)**
this represents the average time
needed to fix a vulnerability.
In our ASM is known as
**estimated remediation time**.
This indicator shows the number
of hours that, through our
calculations, we estimate it will
take you to remediate the selected
type of vulnerability.
This estimate can undoubtedly be
helpful for you to have an idea
of how much time you would have
to invest in the future in the
remediation task.

![Estimated Remediation Time](https://res.cloudinary.com/fluid-attacks/image/upload/v1645455490/docs/web/vulnerabilities/management/managmt_estimated_remed_time.png)

Besides this there are other
useful functionalities you can
do here that enable efficient
management of your vulnerabilities:

- Define a treatment for each
  vulnerability.
- Request that a vulnerability
  be reattacked.
- Request a zero risk treatment
  for a vulnerability.
- Check what information was
  compromised by this type of
  vulnerability, if applicable.
- Look at a script that replicates
  the exploitation process of
  the vulnerability, if applicable.
- Look at a timeline that describes
  how this type of vulnerability
  has evolved over time
