---
id: requirements
title: Requirements
sidebar_label: Requirements
slug: /about/faq/requirements
---

### What are the necessary inputs and requirements for Continuous Hacking?
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

### What are the technical conditions that I must meet for Continuous Hacking?

Access to `Git` and a monitored environment
in the branch are required,
through automated Linux.
The following environments are not supported:

1. Access through a `VPN` that only runs on `Windows`.
1. `VPN` in `Windows`
that requires manual interaction
such as an `OTP` token.
1. `VPN` Site to Site.

### Why is it necessary for Continuous Hacking to have access to the source code stored in the repository?
Continuous Hacking needs
access to the source code
because it is based on
continuous attacks
on the latest version available.

### What type of hacking is included in Continuous Hacking?
Continuous Hacking includes
source code analysis,
application hacking
(see question 5),
and infrastructure hacking
(see question 5).
