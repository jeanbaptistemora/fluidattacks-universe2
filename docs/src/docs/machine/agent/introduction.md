---
id: introduction
title: DevSecOps Agent
sidebar_label: Introduction
slug: /machine/agent
---

We have a component called the
**DevSecOps agent**, which is an
essential element for implementing
DevSecOps in projects.
The agent is included in CI/CD (Continuous
Integration/Continuous Deployment)
environments as a security gate, preventing
vulnerable code from reaching production.
Any change to the Target of Evaluation is
continuously verified.
The agent verifies the status of
vulnerabilities and breaks the build to
force the remediation of those that are
open and unaccepted.

In the [Policies section](/machine/web/organization/policies)
on the ASM, you can select and configure
the conditions or policies that the agent
must validate for breaking the build.

## Table

The DevSecOps section has a table
showing a cumulative record of
the execution of our DevSecOps
agent in your pipeline.
This table contains dates,
numbers of vulnerabilities,
types of testing,
repositories assessed,
among other data.
You can access more details about
each execution by clicking on
the corresponding table row.
These details include a new
table with each vulnerability
and its exploitability,
status and location,
among others.

![DevSevOps Table](https://res.cloudinary.com/fluid-attacks/image/upload/v1650912288/docs/machine/agent/agent_devsecops_table.png)

## Filters

In the
**DevSecOps** section,
five filters are available
for the table.
The first of them is
**Date (range)** which
offers two fields,
allowing you to set a
range of dates during
which our DevSecOps agent
was executed in your pipeline.

![DevSevOps Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1650914016/docs/machine/agent/filters_date_range.png)

The second filter
is **Status**,
which allows you to filter
according to two possible
statuses: Vulnerable and Secure.
The **Vulnerable** status is
given when the agent detects
at least one open vulnerability.
The **Secure** status is given
when there is no open vulnerability
affecting the transition to production.

![DevSevOps Second Filter](https://res.cloudinary.com/fluid-attacks/image/upload/v1650914016/docs/machine/agent/filters_status.png)

The third filter
is **Strictness**,
which lets you select between
two applied agent modes: The
**Strict** mode denotes that
in that execution the agent
was set to deny the deployment
to production (break the build)
when it detected at least one
open vulnerability in the pipeline.
The **tolerant** mode denotes
that in that execution the
agent was set to only give
warnings when it detected
open vulnerabilities
in the pipeline,
allowing deployment to production.

![DevSevOps Third Filter](https://res.cloudinary.com/fluid-attacks/image/upload/v1650914016/docs/machine/agent/filters_strictness.png)

The fourth filter is
**Type**,
in which you have three
options: SAST,
DAST and ALL.
These options correspond
to what the agent recognized
as the techniques with which
vulnerabilities were detected,
ALL being with both SAST and DAST.

![DevSevOps Type Filter](https://res.cloudinary.com/fluid-attacks/image/upload/v1650914016/docs/machine/agent/filters_type.png)

The final filter is
**Git repository**.
In the corresponding field,
you can partially or
completely enter the name
of one of the repositories
evaluated by the agent.
It will restrict the
information in the table
to the repositories with
that name.

## Export button

In the DevSecOps section,
there is the Export button
on the top left.
Clicking on this button,
you can download a CVS
(comma-separated values)
file containing all the
information in the table
of this section.

## Execution details

Clicking on any of our
DevSecOps agent executions,
you will see a pop-up window
that provides more detailed
information about that execution.

![Agent Executions](https://res.cloudinary.com/fluid-attacks/image/upload/v1651011570/docs/machine/agent/exec_details_window.png)

This pop-up window has
two tabs: **Summary**
and **Execution** log.

### Summary

This tab shows a table
that provides you with
concise and clear information
about all the vulnerabilities
reported by our agent in
a specific execution.
You can see each
vulnerability's location,
exploitability,
status and type (according
to the technique that detected it).

![Information Table](https://res.cloudinary.com/fluid-attacks/image/upload/v1651011570/docs/machine/agent/exec_details_summary.png)

Clicking on the
**Columns** button,
you can open a window
to show or hide columns
from the table,
depending on the data
you want to observe.
Clicking on the
**Filters** button,
you can see some filter
options for three
of the columns,
which you can use to
restrict the set of
information visible
in the table.
In addition,
there is a search field
for locations to the right
of these two buttons.

![Filter Options](https://res.cloudinary.com/fluid-attacks/image/upload/v1651011570/docs/machine/agent/exec_details_columns.png)

### Execution log

This tab shows you the
same log you can view in
the pipeline after the
agent's execution.
Here the vulnerabilities
are grouped by type (following
[our standardized set](/criteria/vulnerabilities/)).
Among other data,
you can see the severity score
of each type of vulnerability
and how many vulnerabilities
of that type are open,
closed or accepted.

![Execution Log](https://res.cloudinary.com/fluid-attacks/image/upload/v1651011570/docs/machine/agent/exec_details_log.png)
