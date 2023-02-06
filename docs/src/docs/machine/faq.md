---
id: faq
title: FAQ
sidebar_label: FAQ
slug: /machine/faq
---

In this section,
we answer frequently asked questions
about our
[Attack Resistance Management](/machine/web/arm)
platform.

## Group

### What is a group?

Each [group](/machine/web/groups/general/#group-table)
corresponds to individual projects our
clients create to manage their
[vulnerabilities](/machine/web/groups/vulnerabilities/)
separately.
Inside a group on the
[ARM platform](/machine/web/arm/),
there are several sections that can be
accessed according to the
[role](/machine/web/groups/roles/)
and plan you are subscribed to.
For more information on groups and sections,
please see our [Documentation.](/machine/web/groups)

### Why do we advise you to create several groups?

It is recommended to create several
separate [groups](/machine/web/groups),
each dedicated to one project;
you can have better visibility of
[vulnerabilities](/machine/web/groups/vulnerabilities/)
for their management,
generate focused [reports](/machine/web/groups/reports/)
and certificates independently,
have an organized view of the
[analytics](/machine/web/analytics/),
and have a better track of the details of
each project you work on.

## Vulnerabilities

### What are vulnerabilities?

[Vulnerabilities](/criteria/vulnerabilities/)
are the noncompliance with cybersecurity
[requirements](/criteria/requirements/),
which are rules based on the several international
[standards](/criteria/compliance/)
we check in our comprehensive tests.

### What is the difference between Age and Last report in the Vulnerabilities table?

Age refers to how many days the
[vulnerability](/machine/web/groups/vulnerabilities)
has been open,
whereas last report is the total number
of days passed since the vulnerability
was last reported.

### How do I suggest that a vulnerability is a false positive?

Choose Request [zero risk](/machine/web/vulnerabilities/management/zero-risk/)
as its [treatment.](/machine/web/vulnerabilities/management/treatments)

### How can I see only the findings of the dynamic application security testing (DAST)?

Find the [search bar](/machine/web/groups/vulnerabilities#search-bar)
in the [Vulnerabilities table](/machine/web/groups/vulnerabilities).
By entering **"HTTP"** as a keyword,
you will see the great majority of
vulnerabilities as **“dynamic” (found through DAST)**

### How can I see vulnerabilities specific to a particular Git root?

In the [search bar](/machine/web/groups/vulnerabilities#search-bar)
that you can find in the
[Vulnerabilities table](/machine/web/groups/vulnerabilities),
enter the nickname of the repository
you are interested in,
and the table will show you only the
vulnerabilities reported in that repository.

## Evidence

### How many pieces of evidence (images and videos) do I have access to?

There is a limit of six files
(images or videos).
However,
these are constantly updated according to
the reattacks or new vulnerabilities that
may be reported.

## Scope

### What is a nickname?

A nickname is how the team can identify a
[root](/machine/web/groups/scope/roots/)
or set of
[credentials](/machine/web/machine/web/global-credentials/),
making it easier to search for or identify them.

### Where can I find my repository's nickname?

In the [Git root](/machine/web/groups/scope/roots/#git-roots)
table in the [Scope](/machine/web/groups/scope) section.

## Reattack

### How many hours do I have to wait for a response to a reattack request?

Up to 16 hours,
according to our
[service-level agreement](/about/sla/response/).

### How to request a reattack?

A [reattack](/squad/reattacks/)
can be requested from the
[Locations](/machine/web/vulnerabilities/management/locations/#reattack)
and
[To-do list](/machine/web/vulnerabilities/management/to-do-list/)
section.
You must select the vulnerability to
attack followed by clicking the
**Reattack** button.
Then,
the selected vulnerability will show
the status **Requested** in the
**Reattack** column for up to 16 hours.
Remember to check the
[Consulting](/squad/consulting/#concerning-vulnerabilities)
section for any new comments regarding the reattack.

### How do I know that a requested reattack is in progress?

You can check the reattack status in
the column called **Reattack** in the
[Locations](/machine/web/vulnerabilities/management/locations/#locations-table) section.
You can also check in the
[Consulting](/squad/consulting/#concerning-vulnerabilities)
whether there are comments  on the request.

## Certificate

### How do I generate a service certificate?

In the [Vulnerabilities](/machine/web/groups/vulnerabilities/)
section,
click on the [Generate report](/machine/web/groups/reports/)
button and select the **Certificate**
option.
However,
this option will not be available if
you have not filled out the
**Business Registration Number**
and **Business Name** fields in the
[Information](/machine/web/groups/information/)
section.
Remember that the roles that can download
certifications are
[user manager](/machine/web/groups/roles/#user-manager-role)
and [vulnerability manager](/machine/web/groups/roles/#vulnerability-manager-role).

## Reports

### How do I generate the vulnerability report?

In the [Vulnerability](/machine/web/groups/vulnerabilities/)
section,
click the [Generate report](/machine/web/groups/reports/)
button and select which type of
[report](/machine/web/groups/reports/)
you want to download,
either **technical** or **executive**.
Remember that you must register your
[mobile number](/machine/web/user/)
beforehand to enable two-factor authentication
to download the report.
Remember that the roles that can download
reports are [user manager](/machine/web/groups/roles/#user-manager-role)
and [vulnerability manager](/machine/web/groups/roles/#vulnerability-manager-role).

### What is the difference between executive and technical reports?

The **executive report** is a summary
report in PDF format,
generally intended for personnel in
management roles.
This report contains concise and clear
information on the vulnerabilities
reported in the group.
On the other hand,
the **technical report** is an XLSX file
where you have all the vulnerabilities
reported in the group with their technical details.
