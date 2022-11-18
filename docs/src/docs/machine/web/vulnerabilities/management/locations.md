---
id: locations
title: Locations
sidebar_label: Locations
slug: /machine/web/vulnerabilities/management/locations
---

In locations,
you can view all vulnerabilities
found of that specific type.
In this view,
you can see detailed information
about the specific location.
We will start explaining the
section header.

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

![Vulnerability header](https://res.cloudinary.com/fluid-attacks/image/upload/v1668778565/docs/web/vulnerabilities/management/header.png)

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

![Vulnerability Severity Level critical](https://res.cloudinary.com/fluid-attacks/image/upload/v1668775496/docs/web/vulnerabilities/management/critical.png)

![Vulnerability Severity Level High](https://res.cloudinary.com/fluid-attacks/image/upload/v1668775496/docs/web/vulnerabilities/management/hight.png)

![Vulnerability Severity Level Medium](https://res.cloudinary.com/fluid-attacks/image/upload/v1668775496/docs/web/vulnerabilities/management/medium.png)

![Vulnerability Severity Level Low](https://res.cloudinary.com/fluid-attacks/image/upload/v1668775496/docs/web/vulnerabilities/management/low.png)

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

![Vulnerability Status](https://res.cloudinary.com/fluid-attacks/image/upload/v1668776670/docs/web/vulnerabilities/management/status.png)

Then, continuing from left
to right, you discover the number
of **open vulnerabilities**.
This number corresponds to how
many locations in your system still
have that type of vulnerability.
In the table below, you can precisely
find which files and code lines
are affected.

![Number Of Open Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1668778790/docs/web/vulnerabilities/management/open_vuln.png)

Next, you can see the
**discovery date**.
This is simply the year, month,
and day we first identified and
reported that type of vulnerability
for the group in question.

![Discovery Date](https://res.cloudinary.com/fluid-attacks/image/upload/v1668778886/docs/web/vulnerabilities/management/discover_day.png)

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

![Estimated Remediation Time](https://res.cloudinary.com/fluid-attacks/image/upload/v1668778933/docs/web/vulnerabilities/management/mtr.png)

## Locations table

The locations table gives us
the details of the location of
the vulnerability,
giving us a total of 9 columns;
these are described below:

- **Location:**
  The files where
  this type of vulnerability
  has been reported.
  They can be understood as
  individual vulnerabilities
  of that type.
- **Specific:**
  In what
  lines of code,
  inputs (e.g.,
  password field)
  or ports each
  vulnerability was
  detected.
- **Status:**
  Whether each
  vulnerability has been
  closed (remediated) or
  remains open.
- **Report date:**
  The dates when
  vulnerabilities were reported.
- **Reattack:**
  Whether a
  reattack has been requested
  and is pending,
  is on hold,
  has been verified (open)
  or verified (closed).
  If this cell is blank,
  it should be interpreted
  that a reattack has not
  been requested.
- **Treatment:**
  The defined treatment
  for each vulnerability,
  which could be in progress,
  temporarily accepted,
  permanently accepted or
  zero risk.
- **Tags:**
  Any tags that you
  have given each vulnerability
  to identify it.
- **Treatment Acceptance:**
  The locations that have accepted treatment.
- **Assignees:**
  Locations that have an assigned.

![Locations table explication](https://res.cloudinary.com/fluid-attacks/image/upload/v1668782028/docs/web/vulnerabilities/management/location_table.png)
