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

![Vulnerability Table First Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1667322248/docs/web/groups/vulnerabilities/vulnerability_view.png)

In total,
we have thirteen columns which are
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
  which is Open if at least
  one vulnerability has not
  yet been remediated;
  otherwise,
  it is Closed.
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

There is also a downward-facing
arrow on the left of the Type column,
which,
upon click,
you will find the information that
the column filter offers you.

![Vulnerability Table Second Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1667322709/docs/web/groups/vulnerabilities/downward_facing_arrow.png)

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

![Filtering Columns](https://res.cloudinary.com/fluid-attacks/image/upload/v1667330341/docs/web/groups/vulnerabilities/columns_filter_vulne.png)
### Filters

The other way of filtering is
by clicking the **Filters button**.
Here you will have the activated
filters that you have at the same
time activated in the column filter.

![Filters Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1667330719/docs/web/groups/vulnerabilities/filter_vulne.png)

Lastly,
the option called
**Release date (range)** offers
two fields to set a date range
by which to filter the types of
vulnerabilities that were
reported within that time
at least once.

## Tracking tab

Knowing what happened with each
vulnerability is quite important.
So, it is essential for your team to
obtain information such as dates, users
and justifications for each change in
the history of your security vulnerabilities.
For this purpose, there’s the
**Tracking tab** in the ARM.
This tab gives you detailed information
about each vulnerability in your
software and the treatment each has
received over time.

You can find the **Tracking tab** in
two different places.
One is in each specific vulnerability
type, where you can have a global overview.

![First Tracking Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1643990395/docs/web/groups/vulnerabilities/vulner_first_tracking_tab.png)

The second **Tracking tab** can be accessed
by first clicking on the **Locations** tab
in a vulnerability type and then clicking
on a specific location where the
vulnerability was found.
There you can find the tab, which will show
you individual details on the file you chose.

![Second Tracking Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1643990394/docs/web/groups/vulnerabilities/vulner_second_tracking_tab.png)
