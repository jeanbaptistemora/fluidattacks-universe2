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

![Total type](https://res.cloudinary.com/fluid-attacks/image/upload/v1666184692/docs/web/analytics/common/total_types.png)
## Vulnerabilities with no treatment

Number of vulnerabilities without
a remediation plan specified by
one of your managers.

![Vulnerabilities no treatment](https://res.cloudinary.com/fluid-attacks/image/upload/v1666124094/docs/web/analytics/common/vulnerabilities_with_no_treatment.png)
## Open vulnerabilities

![Open Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1664814053/docs/web/analytics/common/open_vulnerabilities.png)

Number of open vulnerabilities
within your system.

## Remediation rate

![Remediation Rate](https://res.cloudinary.com/fluid-attacks/image/upload/v1664814053/docs/web/analytics/common/remediation_rate.png)

The percentage of
[CVSSF](/about/glossary#cvssf)
remediated (closed/total) in
the different groups,
organization (all groups in
the organization),
or portfolio (all groups in
the portfolio).

## Exposure management over time

![Exposure Management Over Time](https://res.cloudinary.com/fluid-attacks/image/upload/v1643928304/docs/web/analytics/common/common_severity_otime.png)

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

Remember that this graph has three different filters:

- [CVSSF](/about/glossary#cvssf)
  Exposure Level. (The graph that displays by default)
- Vulnerability level, where it tells you the total vulnerabilities.
- The data of the last 30, 90 days, or all.

## Total vulnerabilities

![Total Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1652121574/docs/web/analytics/common/total_vulns.png)

Vulnerabilities are
the minimum units of risk.
They are tied to a system,
and a specific location
within that system.

## Vulnerabilities being re-attacked

![Vulnerability Being Re-Attacked](https://res.cloudinary.com/fluid-attacks/image/upload/v1652120561/docs/web/analytics/common/vulns_being_reattacked.png)

This metric shows an integer,
which refers to the vulnerabilities
still in the reattacked state,
waiting for validation by `Fluid Attacks'.`

## Days since last remediation

![Days Since Last Remediation](https://res.cloudinary.com/fluid-attacks/image/upload/v1652121514/docs/web/analytics/common/days_last_remediation.png)

Days since a finding
was effectively closed.

## Severity

![Severity](https://res.cloudinary.com/fluid-attacks/image/upload/v1666127996/docs/web/analytics/common/severity.png)

Security vulnerabilities are ranked
based on [CVSS v3.1](/about/glossary#cvss).
The higher the score,
the more damage an attack
can make to your system,
and the easier it is to carry it on.

## Active resources distribution

![Active Resources Distribution](https://res.cloudinary.com/fluid-attacks/image/upload/v1666184470/docs/web/analytics/common/active_resources_distribution.png)

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

## Exposure by assignee

![Exposure by Assignee](https://res.cloudinary.com/fluid-attacks/image/upload/v1654545004/docs/web/analytics/common/severity_by_assignment.png)

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

## Exposure trends by vulnerability category

![Exposure Trends Categories](https://res.cloudinary.com/fluid-attacks/image/upload/v1661885630/docs/web/analytics/common/exposure_trends_cat.png)

According to the nine categories
that group the different
types of vulnerabilities,
it will be possible to filter by
30,
60,
90 and 180 days how the
[CVSSF](/about/glossary#cvssf)
of these has varied,
showing whether the exposure
has increased or decreased.

## Accepted vulnerabilities by user

![Accepted Vulns By User](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/accepted_vulns_by_user_pfrrpz.png)

These are the accepted vulnerabilities
grouped under the user
with access to them
that accepted the vulnerabilities.

## Vulnerabilities by source

![Vulns By Source](https://res.cloudinary.com/fluid-attacks/image/upload/v1666183901/docs/web/analytics/common/vulnerabilities_by_source.png)

These are the vulnerabilities
categorized based on
whether they come
directly from an app,
code or the infrastructure.

## Accepted vulnerabilities by CVSS severity

![Accepted By Severity](https://res.cloudinary.com/fluid-attacks/image/upload/v1645810726/docs/web/analytics/common/common_vuln_by_severity.png)

Here you can see information
about the vulnerabilities
that you have accepted
against those that are open
and if those vulnerabilities
have low, medium, high or critical
severities.

## Mean time to remediate (MTTR) by CVSS severity

![Mean Days To Remediate](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443230/docs/web/analytics/common/mean_average_days_to_remediate_eyfowf.png)

Here you can see the average number of days
it takes to remediate vulnerabilities grouped
by the CVSS severity in your organization,
group,
or portfolio.
These times are weighted by exposure to risk (CVSSF).

Remember that this graph has six different filters:

- Days per exposure (The graph that displays by default)
- Days are counted without applying CVSSF
- Non-treated CVSSF which refers to non
  permanently accepted treatment vulnerabilities.
- Non-treated days are counted without applying
  CVSSF which refers to vulnerabilities whose
  treatment is not permanently accepted.
- The data of the last 30, 90 days, or all.

## Mean time to remediate (MTTR) benchmark

![MTTR Benchmark](https://res.cloudinary.com/fluid-attacks/image/upload/v1643928855/docs/web/analytics/common/common_mttr.png)

This section shows the average time your organization,
group,
or portfolio takes to fix vulnerabilities.
These times are weighted by exposure to risk
[(CVSSF)](/about/glossary#cvssf)
and days with non-treated,
which refers to non permanently accepted treatment vulnerabilities.
Also you can filter by the data of the last 30,
90 days,
or all.
You can compare your numbers to those of the best,
the average,
and the worst organizations.

> **NOTE:**
  > MTTR  means “Mean Time To Remediate.”

## Exposure over time

![Exposure over time](https://res.cloudinary.com/fluid-attacks/image/upload/v1644932532/docs/web/analytics/common/common_total_exposur.png)

One of the main dilemmas organizations face
every day is which vulnerability they
should close first.
To address this, we at `Fluid Attacks` designed
a metric called the [CVSSF](/about/glossary#cvssf)
to help you make better decisions.

This new metric recognizes that closing 10
vulnerabilities with a score equal to 1 is
not the same as closing 1 vulnerability
with a score equal to 10.
Additionally, it helps calculate the level
of exposure of a system.

Thanks to the new graph based on the
[CVSSF](/about/glossary#cvssf),
you will be able to know which vulnerabilities
to attack and remediate first to reduce the
level of exposure of your system.

## Days until zero exposure

![Days Until Zero Exposure](https://res.cloudinary.com/fluid-attacks/image/upload/v1646407723/docs/web/analytics/common/common_days_until_0exposure.png)

This is an estimate of the total
number of days it will take you
to remediate all the vulnerabilities
reported to this date.

## Exposure management over time (%)

![Exposure management over time](https://res.cloudinary.com/fluid-attacks/image/upload/v1643929350/docs/web/analytics/common/common_distribution_time.png)

This section shows the **percentage** of closed,
accepted and open vulnerabilities over time,
based on our standard
[CVSSF](/about/glossary#cvssf)
and total Vulnerabilities.

## Exposure by type

![Exposure By Type](https://res.cloudinary.com/fluid-attacks/image/upload/v1643929472/docs/web/analytics/common/common_open_severity.png)

This section shows what vulnerability types are open according to:

- Exposure severity level the our
  [CVSSF](/about/glossary#cvssf) metric.
- Number of Vulnerabilities.
- According to what type Code,
  infra and app.

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

- **Untreated:**
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

![Assigned Vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1666130296/docs/web/analytics/common/status_of_assigned_vulnerabilities.png)

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

## Files with open vulnerabilities in the last 20 weeks

![In Last Weeks](https://res.cloudinary.com/fluid-attacks/image/upload/v1660771972/docs/web/analytics/common/open_last_20_weeks.png)

From the last 20 weeks,
you can see the files are
reported with open vulnerabilities
and the total number of these.
The X-axis represents
the total number of vulnerabilities
and on the Y-axis you can see the
name of the registered files.

## Exposure benchmark

![Exposure benchmark](https://res.cloudinary.com/fluid-attacks/image/upload/v1663701130/docs/web/analytics/common/aggregated_exposure_benchmark.png)

In this chart,
you will be able to compare
your risk exposure levels
[(CVSSF)](/about/glossary#cvssf)
results with other organizations,
groups or portfolios (the best,
the average,
and the worst).

## Mean time to request reattacks

This metric shows the average number
of days it takes customers to request
a reattack.

![Mean time to request](https://res.cloudinary.com/fluid-attacks/image/upload/v1666199798/docs/web/analytics/common/mean_time_to_request_reattacks.png)

:::tip free trial
**Search for vulnerabilities in your apps for free
with our automated security testing!**
Start your [21-day free trial](https://fluidattacks.com/free-trial/)
and discover the benefits of our [Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/)
[Machine Plan](https://fluidattacks.com/plans/).
If you prefer a full service
that includes the expertise of our ethical hackers,
don't hesitate to [contact us](https://fluidattacks.com/contact-us/)
for our Continuous Hacking Squad Plan.
:::
