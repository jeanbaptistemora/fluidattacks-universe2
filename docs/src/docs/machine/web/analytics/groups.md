---
id: groups
title: Group
sidebar_label: Group
slug: /machine/web/analytics/groups
---

## Total types

A type is
a group of vulnerabilities
on your system
related to
the same attack vector.

## Vulnerabilities with not-defined treatment

Number of vulnerabilities
without a remediation plan
specified by
one of your managers.

## Systems risk

![Systems Risk](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443231/docs/web/analytics/groups/systems_risk_h1dmre.png)

- Each grey dot
  represents a resource
  (IP, URL, or repository).
- Red and green dots
  represent the open and closed findings
  for that system,
  respectively.
- Size and darkness
  are proportional
  to the security impact
  on that system.

## Findings by tags

![Finding By Tags](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443232/docs/web/analytics/groups/findings_by_tags_jzu4nw.png)

These are
all your findings
categorized by tag.
Tags can be assigned
at the moment
of defining a treatment
for your vulnerabiities,
for more information
[click here](/machine/web/vulnerabilities/management/treatments/).

## DevSevOps analytics

These are the analytics
based on the information
of your usage of the
[DevSecOps Agent](/machine/agent).

### Service status

Here you can see
if the Agent is
active or inactive.

### Service usage

Number of times
your team used the agent
to check for vulnerabilities.

### Automatized vulnerabilities

The agent performs
security testing of your source-code,
deployed environment
and infrastructure.
Single units
of security problems found
are displayed here.

### Repositories and branches

You can run the agent
in any of your repositories
at any of its versions
(commits or branches).

### Your commitment towards security

![Commitment Towards Security](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443231/docs/web/analytics/groups/commitment_towards_security_uszasj.png)

The agent's objective
is to help your team
overcome security vulnerabilities.
For this to work,
we put two things in your hands:

- The strict mode
  (which is enabled by default)
  helps you stop builds
  or deployments
  if there are open vulnerabilities,
  and thus protects your system
  from vulnerable code introduction.
- However,
  accepted vulnerabilities on the ASM
  are ignored by the strict mode,
  and the agent will
  (by decision of your team)
  allow them to be built
  or deployed.

The maximum benefit is reached
when the accepted risk is low,
and the strict mode high.

### Builds risk

![Builds Risk](https://res.cloudinary.com/fluid-attacks/image/upload/v1623443231/docs/web/analytics/groups/builds_risk_grz5vi.png)

Risk is proportional
to the number of vulnerable changes
introduced into your system:

- A build is considered vulnerable
  if it contains security issues.
- The agent in strict mode
  stops those security issues
  from being delivered
  to your end users.

## Agent

By enabling DevSecOps you get access to a
Docker container built specifically to
verify the status of security vulnerabilities
on your system.
You can embed this container into your Continuous
Integration system to look for changes in
security vulnerabilities:

- DevSecOps is fast and automatic, as it is
  created by the same intelligence of the hackers
  who already know your system in-depth.

- In case the DevSecOps agent finds one vulnerability
  to be open, we can (optionally) mark the build as failed.
  This strict mode can be customized with severity
  thresholds and grace periods according to your needs.

- Statistics from over a hundred different systems
  show that DevSecOps increases the remediation ratio,
  helping you build a safer system and be more
  cost-effective throughout your Software Security
  Development Lifecycle.
