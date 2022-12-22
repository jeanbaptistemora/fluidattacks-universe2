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

![Vulnerability header](https://res.cloudinary.com/fluid-attacks/image/upload/v1671719877/docs/web/vulnerabilities/management/header_locations.png)

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
It can simply be **Safe** or **Vulnerable**.
Open means that at least one of
the locations where we reported
that type of vulnerability has it
without being fixed.
On the other hand, closed means
that you remediated that security
issue in all those locations.

![Vulnerability Status](https://res.cloudinary.com/fluid-attacks/image/upload/v1671655380/docs/web/vulnerabilities/management/statuses.png)

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

![Locations table explication](https://res.cloudinary.com/fluid-attacks/image/upload/v1671655220/docs/web/vulnerabilities/management/locations_tables.png)

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

![Notify button](https://res.cloudinary.com/fluid-attacks/image/upload/v1671720194/docs/web/vulnerabilities/management/notification_action.png)

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
you can enter [here](squad/reattacks)
for more details.

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

![Edit action](https://res.cloudinary.com/fluid-attacks/image/upload/v1671720438/docs/web/vulnerabilities/management/edit_action.png)

You will get a popup window where
you can edit the vulnerability.
If you want to know more about the
fields of this action,
click [here](/machine/web/vulnerabilities/management/vulnerability-assignment).

![Edit pop-window](https://res.cloudinary.com/fluid-attacks/image/upload/v1669045647/docs/web/vulnerabilities/management/edit_popwindow.png)

To save the changes you have made,
click on the **Confirm button**.

### Filters

In the location section,
there are six options to
filter the information presented
in the table.

![Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1669046275/docs/web/vulnerabilities/management/filters_locations.png)

### Search bar

The search bar filters the information
contained in the columns of the table.
