---
id: policies
title: Policies
sidebar_label: Policies
slug: /machine/web/organization/policies
---

On the [Attack Surface Manager (ASM)](https://app.fluidattacks.com),
you can set various policies for
acceptance of vulnerabilities in
your organization to help you control
the risks you are willing to take
in your groups.
You can access the **Policies** section
by clicking on the **Policies** tab on
your organization's home page on ASM.

In this section, you will find two tables.
The first one allows you to define
values for five policies within your
organization.
In front of the column where you enter
the values, we provide you another column
with the numbers we consider recommendable
for each case.

![Policies Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1645537790/docs/web/organizations/policies_section_tab.png)

Below we explain
each of the five policies
you can set up.

## Maximum number of calendar days a finding can be temporarily accepted​

Here you define the maximum number
of calendar days that a finding can
be temporarily accepted; this limit
can be at most 31 calendar days.
This policy affects the execution of
the [DevSecOps agent](/machine/agent)
in case you are using it, since
temporarily accepted vulnerabilities
will not be considered at the time
of breaking your build.
This means that you have to be careful
when setting this number to prevent
some vulnerabilities remaining unresolved
for a long time, which increases the
risk to your applications.

## Maximum number of times a finding can be accepted​

Here you define the maximum number
of times that a vulnerability can
be temporarily accepted.
If, for example, you set this number
as one and accept a vulnerability
temporarily, after the acceptance
period passes, or you change the
treatment of that vulnerability or
remediate it, you won't be able to
accept that same vulnerability again
in the future.
This number can be any number you
deem appropriate.

## Grace period where newly reported vulnerabilities won't break the build

**Period in days (DevSecOps only)**.
Here you define the period in days
that you allow a vulnerability to
be open without it causing the
DevSecOps agent to break the build.

## Minimum CVSS 3.1 score of an open vulnerability for DevSecOps

**Score to break the build in strict mode**.
Here you define the minimum value
of the CVSS score that a vulnerability
has to have in order for the DevSecOps
agent to break the build.

## Temporal CVSS 3.1 score range between which a finding can be accepted​

Here you define the range in severity
score, according to the CVSS 3.1 (values
from 0.0 to 10.0), within which you want
vulnerabilities to be temporarily accepted.
This means that you can control the
maximum risk you are willing to take.
As you will certainly not accept some
risks, the DevSecOps agent will break
your build for the severity scores you
consider relevant.
Of course, if you choose the recommended
0.0 score, no vulnerability can be
temporarily accepted.

In the second table, you will find a
list of the types of vulnerabilities
that your team has suggested for
permanent acceptance.
In front of each vulnerability type name,
you will see whether that acceptance
was approved, rejected or is pending.
All those vulnerability types listed
there as accepted will be ignored by
our DevSecOps agent in its task of
breaking the build.

![List Types Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1645537791/docs/web/organizations/policies_list_types_vuln.png)

Any team member can make the
approval request.
On the other hand, you can approve or
reject only if you are a user manager.
You can accept a type of vulnerability
by clicking the check mark button, which
will change its status from **submitted**
to **approved**.
Conversely, by clicking the cross-mark
button, the status will change to **rejected**.

You can also disable the acceptance
policy for a type of vulnerability by
clicking the button with the minus sign.
A pop-up window will appear asking
for confirmation.
By clicking on **Proceed**, this
vulnerability’s status will automatically
change to **inactive**.

![Disable Acceptance For A Vulnerability](https://res.cloudinary.com/fluid-attacks/image/upload/v1645537790/docs/web/organizations/policies_disable_policy.png)

There’s another button that has
a right arrow symbol.
This button appears when the status
of the type of vulnerability
is **inactive**.
Clicking it will change the status
to **submitted**, and you can further
decide whether or not the vulnerability
will be accepted.

![Button In Inactive Vulnerability](https://res.cloudinary.com/fluid-attacks/image/upload/v1645537790/docs/web/organizations/policies_change_status.png)

Above the table, you will see a text
field with the label **Finding**,
into which you can enter new types
of vulnerabilities that you would
like to add to the list.
Simply enter the name of the type
of vulnerability and click on the
plus sign button.
This will automatically add it with
a submitted status, ready to be
accepted or rejected.

![Enter New Vulnerability Type](https://res.cloudinary.com/fluid-attacks/image/upload/v1645537790/docs/web/organizations/policies_add_newvuln.png)
