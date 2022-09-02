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

## Total types

A type is a group of vulnerabilities
on your system related to the same
attack vector.

## Treatmentless vulnerabilities

Number of vulnerabilities without
a remediation plan specified by
one of your managers.

## Exposure over time

![Exposure Over Time](https://res.cloudinary.com/fluid-attacks/image/upload/v1643928304/docs/web/analytics/common/common_severity_otime.png)

In the ARM,
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

## Total vulnerabilities

![Total Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1652121574/docs/web/analytics/common/total_vulns.png)

Vulnerabilities are
the minimum units of risk.
They are tied to a system,
and a specific location
within that system.

## Vulnerabilities being re-attacked

![Vulnerability Being Re-Attacked](https://res.cloudinary.com/fluid-attacks/image/upload/v1652120561/docs/web/analytics/common/vulns_being_reattacked.png)

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

![Days Since Last Remediation](https://res.cloudinary.com/fluid-attacks/image/upload/v1652121514/docs/web/analytics/common/days_last_remediation.png)

Days since a finding
was effectively closed.

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

## Exposure by assignment

![Exposure By Assignment](https://res.cloudinary.com/fluid-attacks/image/upload/v1654545004/docs/web/analytics/common/severity_by_assignment.png)

This bar chart in an organization,
group or portfolio has
two modes of presentation,
which can be accessed using
the filter function.
It shows you each of your team
members with the percentages
corresponding to the different
treatments they have given to
(a) the total vulnerabilities
or (b) the total risk exposure
[CVSSF](/about/faq/#severity-vs-vulnerabilities)
assigned to them.

## Exposure trends by categories

![Exposure Trends Categories](https://res.cloudinary.com/fluid-attacks/image/upload/v1661885630/docs/web/analytics/common/exposure_trends_cat.png)

According to the nine categories
that group the different
types of vulnerabilities,
it will be possible to filter by
days how the CVSSF of these has varied,
showing whether the exposure
has increased or decreased.

## Accepted vulnerabilities by user

![Accepted Vulns By User](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/accepted_vulns_by_user_pfrrpz.png)

These are the accepted vulnerabilities
grouped under the user
with access to them
that accepted the vulnerabilities.

## Vulnerabilities by source

![Vulns By Source](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/vulns_by_type_x6vnga.png)

These are the vulnerabilities
categorized based on
whether they come
directly from an app,
code or the infrastructure.

## Accepted vulnerabilities by severity

![Accepted By Severity](https://res.cloudinary.com/fluid-attacks/image/upload/v1645810726/docs/web/analytics/common/common_vuln_by_severity.png)

Here you can see information
about the vulnerabilities
that you have accepted
against those that are open
and if those vulnerabilities
have low, medium, high or critical
severities.

## Mean (average) days to remediate

![Mean Days To Remediate](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/mean_average_days_to_remediate_eyfowf.png)

Here you can see
the average number of days
that it takes for the users
of the organization
to solve a discovered vulnerability,
categorized by severity.

## MTTR benchmarking

![MTTR Benchmarking](https://res.cloudinary.com/fluid-attacks/image/upload/v1643928855/docs/web/analytics/common/common_mttr.png)

This section shows how your organization
optimizes how many days pass before closing
or fixing vulnerabilities and how your MTTR
compares to that of the best, the average
and the worst organization.

> **NOTE:**
  > MTTR  means “Mean Time To Remediate.”

## Total exposure

![Total Exposure](https://res.cloudinary.com/fluid-attacks/image/upload/v1644932532/docs/web/analytics/common/common_total_exposur.png)

One of the main dilemmas organizations face
every day is which vulnerability they
should close first.
To address this, we at `Fluid Attacks` designed
a metric called the [CVSSF](/about/faq/#severity-vs-vulnerabilities)
to help you make better decisions.

This new metric recognizes that closing 10
vulnerabilities with a score equal to 1 is
not the same as closing 1 vulnerability
with a score equal to 10.
Additionally, it helps calculate the level
of exposure of a system.

Thanks to the new graph based on the
[CVSSF](/about/faq/#severity-vs-vulnerabilities),
you will be able to know which vulnerabilities
to attack and remediate first to reduce the
level of exposure of your system.

## Days until zero exposure

![Days Until Zero Exposure](https://res.cloudinary.com/fluid-attacks/image/upload/v1646407723/docs/web/analytics/common/common_days_until_0exposure.png)

This is an estimate of the total
number of days it will take you
to remediate all the vulnerabilities
reported to this date.

## Distribution over time

![Distribution Over Time](https://res.cloudinary.com/fluid-attacks/image/upload/v1643929350/docs/web/analytics/common/common_distribution_time.png)

This section shows the percentage of
closed, accepted and open vulnerabilities
over time, based on our standard
[CVSSF](/about/faq/#severity-vs-vulnerabilities).

## Open exposure by type

![Exposure By Type](https://res.cloudinary.com/fluid-attacks/image/upload/v1643929472/docs/web/analytics/common/common_open_severity.png)

This section shows what vulnerability
types are open and their severity
level according to our
[CVSSF](/about/faq/#severity-vs-vulnerabilities)
metric.

## Vulnerabilities by assignment

![Vulnerabilities By Assignment](https://res.cloudinary.com/fluid-attacks/image/upload/v1654033821/docs/web/analytics/common/vulnerabilities_by_assignment.png)

This pie chart in an organization,
group or portfolio shows you the
percentage of open vulnerabilities
assigned to your team members
versus the percentage of those
vulnerabilities not yet assigned.

## Vulnerabilities treatment

On the ARM, you can plan and manage the
remediation of security findings.
Vulnerabilities can be grouped according
to their assigned treatment:

- **Not defined:**
  New vulnerabilities go here until you
  generate an action plan and assign it
  to a developer.

- **In progress:**
  With this treatment, you acknowledge
  the existence of the vulnerability and
  assign a user to it in order to ensure
  it is solved.

- **Temporarily accepted:**
  This treatment is used when you don't
  intend to solve the vulnerability, but
  only temporarily, in which case you
  accept the risks that come with it
  until a selected date.

- **Permanently accepted:**
  As with the previous treatment, this
  is used when you don't intend to solve
  the vulnerability, but this time you
  accept the risks that come with it
  permanently.

![Vulner Treatment](https://res.cloudinary.com/fluid-attacks/image/upload/v1643932056/docs/web/analytics/common/common_vulnerabilities_treatment.png)

## Status of assigned vulnerabilities

Of all the vulnerabilities
already assigned,
it is shown what percentage
are Open or Close.

![Assigned Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1660756441/docs/web/analytics/common/status_assigned_vuln.png)

## Sprint exposure change overall

![Sprint Exposure Overall](https://res.cloudinary.com/fluid-attacks/image/upload/v1655482748/docs/web/analytics/common/sprint_exposure_overall.png)

This figure is the resulting
percentage change in risk
exposure in the current sprint
(i.e.,
the exposure decrement minus
the exposure increment).
A positive value means that
more exposure was reported
than remediated.
A negative value means that
more exposure was remediated
than reported.
A zero value means that as much
exposure was remediated as reported.

## Sprint exposure increment

![Sprint Exposure Increment](https://res.cloudinary.com/fluid-attacks/image/upload/v1655482748/docs/web/analytics/common/sprint_increment.png)

This figure is the percentage
increase in risk exposure in
the current sprint (i.e.,
the newly reported exposure
value relative to the initial
exposure value).
The value is zero when no
vulnerability has been
reported in the period.

## Sprint exposure decrement

![Sprint Exposure Decrement](https://res.cloudinary.com/fluid-attacks/image/upload/v1655482748/docs/web/analytics/common/sprint_decrement.png)

This figure is the percentage
decrease in risk exposure in
the current sprint (i.e.,
the newly remediated exposure
value relative to the initial
exposure value).
The value is zero when no
vulnerability has been
remediated in the period.

## Report technique

![Report Technique](https://res.cloudinary.com/fluid-attacks/image/upload/v1657895822/docs/web/analytics/common/report_technique.png)

Of all the vulnerabilities
reported (Open and Closed),
what is the percentage of
these according to the
different types of security
tests (Sast,
Dast,
and Sca).

## Mean time to reattack

![Mean time to reattack](https://res.cloudinary.com/fluid-attacks/image/upload/v1658425016/docs/web/analytics/common/mean_time_to_reattack.png)

This chart shows how long
reattacks take in number
of hours. From when a reattack
is requested until it is executed.

## Files with open vulnerabilities in the last 20 weeks

![In Last Weeks](https://res.cloudinary.com/fluid-attacks/image/upload/v1660771972/docs/web/analytics/common/open_last_20_weeks.png)

From the last 20 weeks,
you can see the files are
reported with open vulnerabilities
and the total number of these.
The X-axis represents
the registered files,
and the total number of
vulnerabilities on the Y-axis.
