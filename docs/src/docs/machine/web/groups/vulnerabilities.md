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

In the **Vulnerabilities** section,
you find a table containing all
the types of vulnerabilities
reported in the selected group.
This table has nine columns,
which you can choose to show
and hide as described below in
**Filtering your vulnerabilities table**.

![Vulnerability Table First Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1650984610/docs/web/groups/vulnerabilities/vulns_table_1h_m2j4au.png)

- **Type:** The name of the
  type of vulnerability from
  our standardized set whose
  characteristics are met by
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

There is also a downward-facing
arrow on the left of the
Type column,
which,
upon click,
will unfold the description for
each type of vulnerability
shown in the table,
along with extra information.
Namely,
whether the type of vulnerability
is exploitable and the number of
files grouped by the treatment
option that has been defined
for them.

![Vulnerability Table Second Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1650984611/docs/web/groups/vulnerabilities/vulns_table_2h_s8mag6.png)

### Filtering your vulnerabilities table

Above the table showing your
types of vulnerabilities,
there are three buttons:
two for filtering and one for
[generating reports](/machine/web/groups/reports).

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

![Filtering Columns](https://res.cloudinary.com/fluid-attacks/image/upload/v1650984610/docs/web/groups/vulnerabilities/filtering_columns.png)

The other way of filtering
is accessible after clicking
the **Filters** button.
This action will make several
filter options appear,
corresponding to the variables
that give columns their names.

![Filters Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1650984610/docs/web/groups/vulnerabilities/filtering_button.png)

The field **Last report** lets
you filter by the amount of days
passed since the last time the
type of vulnerability was detected.

![Filter Last Report](https://res.cloudinary.com/fluid-attacks/image/upload/v1650984610/docs/web/groups/vulnerabilities/filtering_last_report.png)

The field **Type** lets you
filter by the type of vulnerability.
The available types are the
ones listed in the table.

![Filters Type](https://res.cloudinary.com/fluid-attacks/image/upload/v1650984610/docs/web/groups/vulnerabilities/filtering_type.png)

The field **Status** lets you
filter vulnerabilities by their
open or closed status.
Last in that first row is the field
[Treatment](/machine/web/vulnerabilities/management/treatments),
which lets you filter by
treatment options,
as shown in the
following screenshot:

![Filters Status](https://res.cloudinary.com/fluid-attacks/image/upload/v1650984611/docs/web/groups/vulnerabilities/filtering_status.png)

The option called
**Severity (range)**
offers two fields,
one for a minimum and the
other for a maximum value,
where you can set a range
of CVSS scores (that go
from 0 to 10) by which to
filter the vulnerabilities.

The field **Age** lets you
filter based on the days
elapsed since the type of
vulnerability was found for
the first time in your system.
Next is the field **Locations**,
which lets you filter by the
names of the exact locations
in the repository where the
vulnerabilities were found.
Another option is to use
the field **Reattack**,
thanks to which you can
filter vulnerabilities to
see only either those that
have a pending reattack or
those that do not.

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
**Tracking tab** in the ASM.
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
