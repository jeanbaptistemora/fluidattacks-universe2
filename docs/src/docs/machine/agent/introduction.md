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
on the ARM, you can select and configure
the conditions or policies that the agent
must validate for breaking the build.

## Agent Table

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

![DevSevOps Table](https://res.cloudinary.com/fluid-attacks/image/upload/v1667397781/docs/machine/agent/agent_section.png)

In total,
we have seven columns which
are described below:

- **Date:**
  The date which our DevSecOps agent
  was executed in your pipeline.
- **Status:**
  The agent handles the two states:
  Vulnerable and Secure.
  The **Vulnerable** status is
  given when the agent detects
  at least one open vulnerability.
  The **Secure** status is given
  when there is no open vulnerability
  affecting the transition to production.
- **Vulnerabilities:**
  The total number of open
  vulnerabilities identified
  by the Agent during the execution.
- **Strictness:**
  The agent handles the two modes:
  The **Strict** mode denotes that
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
- **Type:**
  You can find three
  options: SAST, DAST and ALL.
  These options correspond
  to what the agent recognized
  as the techniques with which
  vulnerabilities were detected,
  ALL being with both
  SAST and DAST.
- **Git repository:**
  The name of the repositories
  evaluated by the agent.
- **Identifier:**
  Is the Agent's
  run identifier number.

## Functionalities

### Filters

In the
**DevSecOps** section,
there are seven filters
available for the table.
You can find them on
the right side next to
the search bar.

![DevSevOps Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1663617023/docs/machine/agent/agent_filters.png)

### Export button

In the DevSecOps section,
there is the Export button
on the top left.
Clicking on this button,
you can download a CSV
(comma-separated values)
file containing all the
information in the table
of this section.

### Search bar

The search bar filters the
information contained in the
columns of the table.

## Execution details

Clicking on any of our
DevSecOps agent executions,
you will see a pop-up window
that provides more detailed
information about that execution.

![Agent Executions](https://res.cloudinary.com/fluid-attacks/image/upload/v1667401361/docs/machine/agent/details.png)

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

![Information Table](https://res.cloudinary.com/fluid-attacks/image/upload/v1667413429/docs/machine/agent/sumary.png)

### Summary Table

It has the following columns:

1. **Exploitability:**
  The exploitability score based
  on the CVSS.
1. **Status:**
  The state reported by the agent.
1. **Type:**
  You can find two
  options:
  Static Application Security Testing (SAST)
  and
  Dynamic Application Security Testing (DAST).
1. **What and where:**
  Where exactly is the vulnerability.

#### Columns filter

Clicking on the
**Columns** button,
you can open a window
to show or hide columns
from the table,
depending on the data
you want to observe.

![Filter Options](https://res.cloudinary.com/fluid-attacks/image/upload/v1651011570/docs/machine/agent/exec_details_columns.png)

#### Filters button

Clicking on the
**Filters** button,
you can use to
restrict the set of
information visible
in the table.

![Filter Options](https://res.cloudinary.com/fluid-attacks/image/upload/v1667415359/docs/machine/agent/filters.png)

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

![Execution Log](https://res.cloudinary.com/fluid-attacks/image/upload/v1663673819/docs/machine/agent/execution_log.png)
