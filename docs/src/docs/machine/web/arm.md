---
id: arm
title: Attacks Resistance Management
sidebar_label: Attacks Resistance Management
slug: /machine/web/arm
---

`Fluid Attacks'` Attacks Resistance Management (ARM)
comes with all functions you need
to manage all your applications
and vulnerabilities effectively.

To access this platform
you can click [here](https://app.fluidattacks.com).

## Requirements

We support the web browsers
listed below and,
in general,
any browser that supports
ECMAScript 2019 standard.

| Browser    | Version                                                                                                           |
|------------|-------------------------------------------------------------------------------------------------------------------|
| Firefox    | 60, 68, 78, 81, 82, 83, 88, 89, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105                  |
| Chrome     | 71, 75, 80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100, 101, 102, 103, 104, 105, 106 |
| Edge       | 84, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105                                      |
| Safari     | 12.1, 13.1, 14, 14.1, 15, 15.1, 15.2, 15.3, 15.4, 15.5, 15.6,16                                                   |
| Opera      | 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90                                                                |
| Chrome iOS | 90, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103,  105                                                          |                                      |

## Login

To authenticate in the ARM,
you need a valid user
in at least one of these providers:

- Google
- Azure
- Bitbucket

For added security,
we do not manage users,
credentials
or MFA (multi-factor authentication).
We adopt our customers' policies.

## Organizations

All customer data is consolidated
in this ARM's section.
Each [organization](/machine/web/creating-organization)
has a data bucket
that only users of that organization
can access.

In this section,
you will find the following subsections
(see the right-hand menu):

### Analytics

Charts and indicators
will help you know what is happening
with your applications.
Information presented,
among others,
includes the following:

- Exposure over time
- Vulnerability status
- Vulnerability treatment
- Open vulnerabilities
- Exposure management over time

### Groups

You may have multiple apps
in your organization,
and you probably want to
keep their vulnerabilities separate.

You can have as many [groups](/machine/web/groups)
as you want.
One group for each application
or several groups for one application,
it is your choice.

In Groups section,
you will find:

#### Vulnerabilities

One of the main sections on the platforms
is where you find all the confirmed security issues
of your application.

[Vulnerabilities](/machine/web/groups/vulnerabilities)
section is divided as follows:

##### Locations

[Here](/machine/web/vulnerabilities/management/locations)
you find the list
of all vulnerabilities
with their specific locations:
File and LoC,
URL and input or IP and port.

You can ask for a reattack
or change the treatment
for one or many vulnerabilities
as you want.

Also,
you can add tag
 or define a qualitative risk level.

##### Reattack

When a vulnerability is remediated,
you need to request the `Fluid Attacks` team
to [reattack](/squad/reattacks)
it and confirm
if it was indeed remediated.

You can check in the
[Locations table](/machine/web/vulnerabilities/management/locations#locations-table)
which vulnerabilities were requested
to reattack and verify their remediation.
After verification,
the `Fluid Attacks` team
will inform you through the
[Consulting](/squad/consulting)
tab about the results.

##### Treatments

Risk management is an essential part
of vulnerabilities management.
You can define different
[treatments](/machine/web/vulnerabilities/management/treatments)
in the [Locations tab](/machine/web/vulnerabilities/management/locations):

- **New:**
  The vulnerability was reported,
  and there is no treatment defined.
- **In progress:**
  The vulnerability is going to be remediated
  and has a user responsible
  for that remediation.
- **Temporarily accepted:**
  You may not resolve the vulnerability
  and decide to coexist with the risk
  for some time.
  The platform accepts by default
  a maximum of six months.
  You can control this setting
  in the Organization Policies section.
- **Permanently accepted:**
  You may not resolve the vulnerability
  and decide to coexist
  with the risk forever.

##### Description

In this [section](/machine/web/vulnerabilities/management/description)
you can discover
all required information
to understand reported vulnerabilities.

##### Severity

For the calculation
of the [severity](/machine/web/vulnerabilities/severity)
of vulnerabilities,
we use the Common Vulnerability Scoring System
(CVSS) version 3.1.

##### Evidence

In [evidence](/machine/web/vulnerabilities/evidence)
we provide video examples and screenshots
to help you understand
the context of the vulnerabilities.

##### Tracking

[Here](/machine/web/vulnerabilities/management/tracking)
you find the history of each Vulnerability.
What has happened to the vulnerabilities
since the first one was reported.
When and by whom
the treatment was closed or changed.

##### Records

Some vulnerabilities
can expose customer information;
for context,
we share the disclosed information in this
[section.](/machine/web/vulnerabilities/management/records)

##### Consulting in the vulnerability

[Consulting](/squad/consulting/#concerning-vulnerabilities)
should be used to
communicate with us when a problem
is related to any of the reported
vulnerabilities or to validate the
executed reattacks.

> **Note:** This section is for Squad plan only.

#### Group analytics

As in the case of Organization Analytics,
[Group Analytics](/machine/web/analytics/groups)
have all the information about your group.

#### DevSecOps

`Fluid Attacks'` ARM
includes an [agent](/machine/agent)
that present in the CI pipelines
can break the build for open vulnerabilities.
This section shows
the result of recent executions
and more information such as the following:

- Execution date
- Execution status (secure or vulnerable)
- Checked vulnerabilities
- Strictness (Tolerant/Strict)
- Type (SAST/DAST)

#### Events

In the service execution,
many things can and will happen.
In the [events](/machine/web/groups/events),
our analysts can report
any situation that affects the service.
It can be a full or partial disruption
or merely a request for information.

#### Consulting

Communication is essential
to achieve the remediation goal.
You can post any doubt,
comment, or thought
you want to share
with the `Fluid Attacks` team
or your team in the
[Consulting tab.](/squad/consulting#concerning-groups)
This section works like a forum
where anyone can post and reply.

> **Note:** This section is only for the Squad plan.

#### Group stakeholders

You have group access control
[here](/machine/web/groups/stakeholders)
to define who and what they can do.
When you give access to the group,
there are four role options available:

- User
- User manager
- Vulnerability Manager

To get more information about it,
check the
[Roles section.](/machine/web/groups/roles)

#### Authors

The [authors](/machine/web/groups/authors)
section gives you a list of git users
that commit code
to checked repositories.

#### Surface

The [surface](/machine/web/groups/surface)
tab gives more information
about the Target of Evaluation (ToE).
This ToE is the result of repositories,
environments and languages specified
in the scope roots section.

#### Scope

For an ARM,
you need to define the surface
that the `Fluid Attacks` team will check.
The following information
is required to enable
the testing service:

- **Roots:**
  Git repositories
  where you version
  the application’s source code.
- **Environments:**
  URLs where applications are deployed.
- **Files:**
  Any information
  that could help the service.
- **Tags:**
  Keywords to build portfolios
  and get information and analytics
  for groups that share the tag.
- **Services:**
  Active services for the group.
- **Deletion:**
  Function to safely delete
  all group data.

If you want to see more of this
section of scope,
you can enter it
[here](/machine/web/groups/scope/roots)

### Portfolios

In the Analytics subsection,
you have the data of all your groups.
But if you want analytics for only a subset,
you can go to the [Portfolios](/machine/web/portfolios)
subsection
(we employ the same charts and indicators).

Please check the tags
in [Scope](/machine/web/groups/scope/portfolios)
for more information.

### Organization Stakeholders

Some users can access
your organization's data,
but this permission
does not guarantee access
to groups or vulnerabilities,
only access to organization-level analytics and policies.

Explore more of this section by
clicking on this [link.](/machine/web/stakeholders)

### Policies

You can use vulnerability treatments
to plan remediation.
To control the correct use of them,
you can define rules
that will apply to all groups
in your organization.

[Policies](/machine/web/organization/policies)
to define:

1. Temporal acceptance:
  maximum number
  of days for assignment.
1. Temporal acceptance:
  maximum number of assignments for a
  single vulnerability.
1. Temporal acceptance:
  minimum CVSS 3.1 score allowed for assignment.
1. Temporal acceptance:
  maximum CVSS 3.1 score allowed for assignment.
1. DevSecOps:
  Days before agent starts breaking the build
  for new vulnerabilities.
1. DevSecOps:
  Minimum CVSS 3.1 score from which agent breaks
  the build for open vulnerabilities.

### Credentials

In this [section,](/machine/web/machine/web/global-credentials)
you can create,
edit and delete credentials at the Organization
level and use them in all the groups
that compose that. These credentials help
us to have access to the
[ToE](/about/glossary#toe)

### Compliance

[Compliance](/machine/web/compliance)
shows the compliance of all
standards validated by `Fluid Attacks`
at the Organization and group level.

## ARM Update

When the ARM was last deployed,
be it because of new features or
improvements to old features, is
not top secret information we
are keeping from our clients.
You can see this information by
clicking on the icon with the
letter **i** on the ARM’s
top-right menu.

![Top Right Menu](https://res.cloudinary.com/fluid-attacks/image/upload/v1646329458/docs/web/web_asm_update_menu.png)

Upon clicking, you will see the
commit hash ID (a commit’s unique
identifier) that corresponds
to the update.
Below, you will see the update
deployment date and time.
You can click on the commit hash
to see on GitLab the specific
lines of code that were changed,
the developer who made the change,
what was removed and added, and
on what file.

![Commit Hash Id](https://res.cloudinary.com/fluid-attacks/image/upload/v1646329458/docs/web/web_asm_update_commit.png)
