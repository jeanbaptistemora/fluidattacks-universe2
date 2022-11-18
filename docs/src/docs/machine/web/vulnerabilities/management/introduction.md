---
id: introduction
title: Introduction
sidebar_label: Introduction
slug: /machine/web/vulnerabilities/management
---

With `Fluid Attacks` ARM you will
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

![Vulnerability Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1668771723/docs/web/vulnerabilities/management/locations_vieew.png)

In this section,
you will find the following subsections:

- Locations.
- Description.
- Severity.
- Evidence.
- Tracking.
- Records.
- Consulting.

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
In our ARM is known as
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
