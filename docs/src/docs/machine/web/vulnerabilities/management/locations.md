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

![Vulnerability header](https://res.cloudinary.com/fluid-attacks/image/upload/v1673910324/docs/web/vulnerabilities/management/vul_name.png)

The first thing you see below
the title, on the far left, is
the **Total Risk Exposure (CVSSF)**
represents how much the vulnerability
to exposure of the group is
contributing.

![total risk cvssf](https://res.cloudinary.com/fluid-attacks/image/upload/v1673911339/docs/web/vulnerabilities/management/risk_cvssf.png)

Next is the **Status** information,
where you can see two items of information:
The severity level and the
status.
In **severity** level shows you a
number,
which means it is a score based on
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

![severity level cvss](https://res.cloudinary.com/fluid-attacks/image/upload/v1673911424/docs/web/vulnerabilities/management/severity_level.png)

In **status** of that
type of vulnerability.
It can simply be **Safe** or **Vulnerable**.
Vulnerable means that at least one of
the locations where we reported
that type of vulnerability has it
without being fixed.
On the other hand, Safe means
that you remediated that security
issue in all those locations.

![Vulnerability Status](https://res.cloudinary.com/fluid-attacks/image/upload/v1673911527/docs/web/vulnerabilities/management/status.png)

Then, continuing from left
to right, you discover the number
of **open vulnerabilities**.
This number corresponds to how
many locations in your system still
have that type of vulnerability.
In the table below, you can precisely
find which files and code lines
are affected.

![Number Of Open Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1673911635/docs/web/vulnerabilities/management/opne_vul.png)

Next, you can see the
**discovery date**.
This is simply the year, month,
and day we first identified and
reported that type of vulnerability
for the group in question.

![Discovery Date](https://res.cloudinary.com/fluid-attacks/image/upload/v1673911702/docs/web/vulnerabilities/management/firts_report.png)

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

![Estimated Remediation Time](https://res.cloudinary.com/fluid-attacks/image/upload/v1673911762/docs/web/vulnerabilities/management/mttr.png)

## Locations table

The locations table gives us
the details of the location of
the vulnerability,
giving us a total of 9 columns;
these are described below:

![Locations table explication](https://res.cloudinary.com/fluid-attacks/image/upload/v1673912109/docs/web/vulnerabilities/management/locations_col.png)

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
  Safe (remediated) or
  remains Vulnerable.
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

Note that you can identify when a vulnerability
is new because you will see the tag called **new.**

![New tag location](https://res.cloudinary.com/fluid-attacks/image/upload/v1677668980/docs/web/vulnerabilities/management/new_tag_locations.png)

:::note
You can see a pop-up window with details
by clicking on any location.
For more information,
click [here](/machine/web/vulnerabilities/management/details).
:::

## Functionalities

### Notify button

This feature helps us notify all
open locations of the
specific vulnerability type,
receiving a report of these.
Please note that this feature
will only appear for the
[User manager](/machine/web/groups/roles/#user-manager-role)
and [Vulnerability manager](/machine/web/groups/roles/#vulnerability-manager-role)
roles.

To receive this email,
Click on the **Notify button**.

![Notify button](https://res.cloudinary.com/fluid-attacks/image/upload/v1673913674/docs/web/vulnerabilities/management/notify_button.png)

You will get a confirmation
pop-up window if you want
to receive the notification.

![confirmation window](https://res.cloudinary.com/fluid-attacks/image/upload/v1666213023/docs/web/vulnerabilities/management/confirmation_window.png)

When you click **Notify**,
you will get an email called
Vulnerability Alert,
which has information about
this locations.

### Reattack

In this section,
you can do Reattack;
for more information,
we have an exclusive section
for this action,
you can enter [here](/squad/reattacks)
for more details.

![reattack button](https://res.cloudinary.com/fluid-attacks/image/upload/v1675195283/docs/web/vulnerabilities/management/reattack_location.png)

### Edit button

If you want to edit a vulnerability
(change treatment,
assign,
add tags,
etc.
),
you can do it with the Edit button.
First,
you must select which vulnerability
you want to edit,
followed by clicking on the edit button.

![Edit action](https://res.cloudinary.com/fluid-attacks/image/upload/v1673915918/docs/web/vulnerabilities/management/edit_button.png)

You will get a popup window where
you can edit the vulnerability.
If you want to know more about the
fields of this action,
click [here](/machine/web/vulnerabilities/management/treatments).

![Edit pop-window](https://res.cloudinary.com/fluid-attacks/image/upload/v1669045647/docs/web/vulnerabilities/management/edit_popwindow.png)

To save the changes you have made,
click on the **Confirm button**.

### Filters

In the location section,
there are six options to
filter the information presented
in the table.

![Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1669046275/docs/web/vulnerabilities/management/filters_locations.png)

Remember that you can see the filters you
have applied in the table next to the add
filters button.

![Filters applied](https://res.cloudinary.com/fluid-attacks/image/upload/v1675201153/docs/web/vulnerabilities/management/filters_applied.png)

> **Note:** These applied filters will be
> kept in the vulnerability view in the
> different groups of the same or another
> organization.

### Search bar

The search bar filters the information
contained in the columns of the table.
