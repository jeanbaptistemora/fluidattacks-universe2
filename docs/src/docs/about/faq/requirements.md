---
id: requirements
title: Requirements
sidebar_label: Requirements
slug: /about/faq/requirements
---

## What are the necessary inputs and requirements for the Squad plan?

The necessary inputs
and requirements are:

1. **Phase 1:**
  Access to the integration branch
  of the repository
  for the not-yet-deployed
  application’s source code.
  Ethical Hacking focuses
  on the source code.

1. **Phase 2:**
  When the project has
  a deployed application
  (Integration Environment),
  the hacking coverage expands
  to include application security testing.

1. **Phase 3:**
  This phase applies only if
  the infrastructure supporting the application
  is defined as code
  and kept in the integration branch
  of the repository referred to in Phase 1.
  This phase includes infrastructure hacking.

## What technical conditions must I meet for the Squad plan?

Access to `Git` and a monitored environment
in the branch are required,
through automated Linux.
The following environments are not supported:

1. Access through a `VPN` that only runs on `Windows`.
1. `VPN` in `Windows`
  that requires manual interaction
  such as an `OTP` token.
1. `VPN` Site to Site.

## In the Squad plan, why is access to the source code repository necessary?

The Squad plan needs
access to the source code
because it is based on
continuous attacks
on the latest version available.

## If the application is stored along multiple repositories, can they all be attacked?

Yes,
with one condition.
The code must be stored
in the same branch
in each repository.
For example:
If it is agreed
that all attacks will be performed
on the `QA` branch,
then this same branch
must be present
in all of the repositories
included for hacking.

## What type of hacking is included in the Squad plan?

The Squad plan includes
source code analysis,
application hacking
(see [this question](/about/faq/requirements#what-are-the-necessary-inputs-and-requirements-for-the-squad-plan)),
and infrastructure hacking
(see [this question](/about/faq/requirements#what-are-the-necessary-inputs-and-requirements-for-the-squad-plan)).

## Do the repositories need to be in a specific version control system?

The Squad plan is based
on using `Git`
for version control.
Therefore,
`Git` is necessary
for she Squad plan.

## Does the Squad plan require any development methodology?

No.
It is independent
of the client’s development methodology.
The Squad plan test results
become a planning tool
in future development cycles.
They do not prevent
the continuation of development.

## Does the Squad plan depend on the type of repository I use?

No.
The client can use
whatever repository
they deem appropriate.
We only require
access to the integration branch
and its respective environment.
