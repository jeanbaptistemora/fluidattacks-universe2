---
id: common
title: Common
sidebar_label: Common
slug: /machine/web/analytics/common
---

This is the information
that is in every section
where you can find
the analytics,
each one varies
depending on where
are you visualizing them,
for example,
if you see them
inside a group,
then everything is based
on the information
of only that specific group.
The following are
the common analytics:

## Vulnerabilities over time

![Vulns Over Time](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/vulns_over_time_zjlwdi.png)

In the ASM,
you can track the evolution of your systems
from a security point of view:

- Open vulnerabilities represent a risk
  currently impacting
  your end-users and systems.
- Open vulnerabilities with accepted treatment
  are exactly like open ones,
  except that you decided
  to coexist with that risk.
- Closed vulnerabilities may be seen
  as security breaches
  that your system no longer has.

## Vulnerabilities status

![Vulns Status](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/vulns_status_exbwkp.png)

Ratio between
open and closed vulnerabilities,
ignoring treatments.

## Vulnerabilities treatment

![Vulns Treatment](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443231/docs/web/analytics/common/vulns_by_treatments_ofir6j.png)

In the ASM,
you can plan and manage
the remediation of security findings:

- Not defined:
  New vulnerabilities go here
  until one of your managers
  generates an action plan.
- In progress:
  The system is currently
  being hardened by your developers.
- Temporarily accepted:
  A manager decided
  to coexist with the risk
  temporarily.
- Permanently accepted:
  A vulnerability
  that will never be remediated.

## Total vulnerabilities

Vulnerabilities are
the minimum units of risk.
They are tied to a system,
and a specific location
within that system.

## Vulnerabilities being re-attacked

Once your team has solved a vulnerability
you can request a re-attack.
In the re-attack process
a hacker will replay the attack vector
and confirm that the proposed solution
actually shields your system.
In case it does not,
your team will be notified
and the finding kept open.

## Days since last remediation

Days since a finding
was effectively closed.

## Mean time to remediate (all vulnerabilities)

Amount of time (in days)
it takes to your team
to fix a security vulnerability.

## Mean time to remediate (non treated vulnerabilities)

Amount of time (in days)
it takes to your team
to fix a security vulnerability,
excluding accepted vulnerabilities.

## Severity

![Severity](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/severity_pftfig.png)

Security vulnerabilities are ranked
based on [CVSS v3.1](/about/glossary#cvss).
The higher the score,
the more damage an attack
can make to your system,
and the easier it is to carry it on.

## Active resources distribution

![Active Resources Distribution](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443231/docs/web/analytics/common/active_resources_distribution_kqmp7h.png)

Resources can be of two types:
Repository and Environment.

- Environment:
  A URL or IP pointing to an instance
  of your system.
- Repository:
  The associated source-code
  of the environment
  and (ideally) its infrastructure.

The maximum benefit is reached
when every environment
has its full source-code available
for us to test it.

## Vulnerabilities by tag

![Vulns By Tag](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/vulns_by_tag_kixwyd.png)

These are
all your vulnerabilities
categorized by tag.
Tags can be assigned
at the moment
of defining a treatment
for your vulnerabiities,
for more information
[click here](/machine/web/vulnerabilities/management/treatments/).

## Vulnerabilities by level

![Vulns By Level](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/vulns_by_level_u8aydw.png)

These are
all your vulnerabilities
categorized by level.
Levels can also be assigned
at the moment
of defining a treatment
for your vulnerabiities,
for more information
[click here](/machine/web/vulnerabilities/management/treatments/).

## Accepted vulnerabilities by user

![Accepted Vulns By User](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/accepted_vulns_by_user_pfrrpz.png)

These are the accepted vulnerabilities
grouped under the user
with access to them
that accepted the vulnerabilities.

## Vulnerabilities by treatment

![Vulns By Treatment](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/vulns_treatment_fbvsjj.png)

These are your vulnerabilities
categorized by the number of times
that they changed treatments.
For example,
a vulnerability starts as **New**,
then changes to **In progress**
when a user starts solving it,
then it may change to **Permanently accepted**
if for any number of circumstances
it couldn't be solved,
and then this vulnerability
would fall under those
that changed treatment three times.

## Vulnerabilities by type

![Vulns By Type](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/vulns_by_type_x6vnga.png)

These are the vulnerabilities
categorized based on
whether they come
directly from an app,
code or the infrastructure.

## Top vulnerabilities

![Top Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/top_findings_by_open_vulns_vl8lls.png)

These graph shows the findings
that have the highest number
of individual open vulnerabilities.

## Accepted vulnerabilities by severity

![Accepted By Severity](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443231/docs/web/analytics/common/accepted_vulns_by_severity_weloug.png)

Here you can see information
about the vulnerabilities
that you have accepted
against those that are open
and if those vulnerabilities
have low, medium, high or critical
severities.
