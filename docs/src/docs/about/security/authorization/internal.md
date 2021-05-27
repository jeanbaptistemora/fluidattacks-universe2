---
id: internal
title: Internal
sidebar_label: Internal
slug: /about/security/authorization/internal
---

Every application we use must have
user-granular authorization settings
to grant minimum-privilege policy at all times.
Some examples are:

- **IAM and KMS:** These two tools
are widely used within `Fluid Attacks`.
They allow us to ensure
that hackers can only access the source code,
environments, exploits, and secrets
of the projects they are assigned to.
Access can be easily removed should the need arise,
with no users/passwords leaked.
These tools also let us
keep application production secrets
hidden from developers
(Production-Development secrets separation).

- **Infrastructure:** Infrastructure components
always provide minimum privileges
only to the applications that need to use them.
We never give any service full permissions
over our entire infrastructure.

- **IAM:** It is possible to give
application access at the user level,
which allows us to give employees access
[only to what they need](/criteria/requirements/data/176)
to execute their tasks.
[Giving or removing access to applications](/criteria/requirements/authorization/034)
is simple, and no users/passwords are leaked.
