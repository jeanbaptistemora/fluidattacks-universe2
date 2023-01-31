---
id: vulnerabilities
title: Vulnerabilities
sidebar_label: Vulnerabilities
slug: /machine/web/groups/vulnerabilities
---

The **Vulnerabilities** section is
the first one you see when clicking
on one of your group's names.

## Vulnerabilities Table

In the Vulnerabilities section,
you will find a table containing
all the [types of vulnerabilities](/criteria/vulnerabilities/)
reported in the selected group.
This table includes different columns,
which you can activate or deactivate
according to the information you want
to see using the [columns filter](/machine/web/groups/vulnerabilities/#filtering-your-vulnerabilities-table)
button.

![Vulnerability Table First Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1675162266/docs/web/groups/vulnerabilities/vulnerabilities.png)

In total,
we have fourteen columns which are
described below:

- **Type:** The name of the
  type of vulnerability from
  our [standardized set](/criteria/vulnerabilities/)
  whose characteristics are met by
  the vulnerability found in
  your system.
- **Age:** The number of days
  elapsed since the type of
  vulnerability was found in
  your system for the first
  time.
- **Last report:** The number
  of days elapsed since
  we found a vulnerability
  of that specific type,
  regardless of its open
  or closed status.
- **Status:** The condition of
  the type of vulnerability,
  which is Vulnerable if at least
  one vulnerability has not
  yet been remediated;
  otherwise,
  it is Safe.
- **Severity:** The CVSS
  (Common Vulnerability Scoring
  System) base score given to
  the type of vulnerability.
- **Open vulnerabilities:**
  The number of files where
  the type of vulnerability
  was found and is still
  open; that is,
  not yet remediated.
- **Remediation %:**
  The percentage of closed
  vulnerabilities of that type.
- **Locations:** The name of
  one specific file where the
  type of vulnerability was found.
  (However,
  if this type was found
  in several files,
  you should click on it
  to see a complete locations
  table.)
- **Reattack:** The status of
  the reattacks for the type
  of vulnerability,
  which is Pending if at least
  one requested reattack is
  due to one of the vulnerabilities
  of this type; otherwise,
  it is just a hyphen.
- **Assignees:**
  The name of the assignees the
  specific vulnerability type.
- **Release Date:**
  Date when the typology was reported.
- **Treatment:**
  List the treatments that this
  typology has.
- **Description:**
  A definition of the type of
  vulnerability.
- **% Risk Exposure:**
  Represents how much the vulnerability
  to exposure (CVSSF)
  of the group is contributing.

There is also a downward-facing
arrow on the left of the Type column,
which,
upon click,
you will find the information that
the column filter offers you.

![Vulnerability Table Second Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1675162531/docs/web/groups/vulnerabilities/down_row.png)

## Functionalities

### Columns filter

One way of filtering the
table is by hiding or
showing columns.
To do this,
you need to click the
Columns button.
This will cause a pop-up
window to appear,
from which you can enable
and disable columns.

![Filtering Columns](https://res.cloudinary.com/fluid-attacks/image/upload/v1673907259/docs/web/groups/vulnerabilities/columns_filter.png)
### Filters

The other way of filtering is
by clicking the **Filters button**.
Here you will have the activated
filters that you have at the same
time activated in the column filter.

![Filters Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1675162726/docs/web/groups/vulnerabilities/filters.png)

Remember that you can see the filters you
have applied in the table.

![Filters applied](https://res.cloudinary.com/fluid-attacks/image/upload/v1675164134/docs/web/groups/vulnerabilities/filters_aplied.png)

> **Note:** These applied filters will be
> kept in the vulnerability view in the
> different groups of the same or another organization.

### Search bar

The search bar filters the information
contained in the columns of the table.

:::note
You can also find in the vulnerability
view how to generate reports.
Click [here](/machine/web/groups/reports)
if you want to know more.
:::
