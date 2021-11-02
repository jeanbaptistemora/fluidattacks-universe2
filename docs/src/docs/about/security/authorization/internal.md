---
id: internal
title: Internal
sidebar_label: Internal
slug: /about/security/authorization/internal
---

Every application we use
must have user-granular authorization settings
to grant a least privilege policy
at all times.
Some examples are the following:

- **IAM and KMS:** These two tools are widely used
  within `Fluid Attacks`.
  They allow us to ensure
  that hackers can only access the source code,
  environments, exploits,
  and secrets of their assigned projects.
  We can easily remove access
  if the need arises
  without leaking users/passwords.
  These tools
  also allow us to keep application production secrets
  hidden from developers
  (separation of production-development secrets).

- **Infrastructure:** Infrastructure components
  always grant minimum privileges
  only to the applications that need to use them.
  We never give any service full permissions
  over our entire infrastructure.

- **IAM:** It is possible to provide user-level access
  to the application,
  which allows us to give employees access
  [only to what they need](/criteria/requirements/176)
  to perform their tasks.
  [Granting or removing access to applications](/criteria/requirements/034)
  is simple,
  and no users/passwords are leaked.
