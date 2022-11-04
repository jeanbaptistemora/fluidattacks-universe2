---
id: governance
title: Governance
sidebar_label: Governance
slug: /development/governance
---

The Universe code repository at Fluid Attacks
is a Free and Open Source Software project
that depends entirely on contributions
from the employees at Fluid Attacks.
Anyone may [contribute](/development/contributing) to the project at any time
by participating in discussions,
making suggestions,
or any other contributions they see fit.

The summary of our current Governance model is:

- The most recent Developer is responsible.
  That is to say,
  responsibility is transferred between Developers
  as they create and maintain code over time.
  In other words,
  the last Developer that maintained something
  is responsible for that something,
  and by default, when a Developer creates something,
  the Developer is responsible for that something.
  This mechanism facilitates the growth and empowerment of newer Developers
  and also prevents overburdening older Developers with excessive scope.
  At the same time,
  having a single responsible for something
  also defines an explicit boundary
  and sets an implicit expectation
  of who should answer questions,
  provide support,
  and pursue the quality attributes of the things inside that boundary.

- Awareness of technical ideas and problems flow upwards
  through the organizational structure.
- The current vision and the needs of the business
  flow downwards through the organizational structure.
- There is a person that makes the last call on any aspect
  and is ultimately responsible for everything: the CTO.

You can think of it as a [convection cell](https://en.wikipedia.org/wiki/Convection_cell).

<!--

OpenSSF Requirements:

- Key roles, tasks and responsibilities.
- Who has each role (this can be in a separate document).
- How the project makes decisions, what role takes them,
  and how disputes are resolved.

-->

Below you'll find a breakdown of the organizational structure:

![Governance](./governance.dot.svg)

## Roles and responsibilities

Some of the roles here
may have a scope and responsibilities that go beyond this repository.
However,
this document only describes the relevant portion of those roles
to the Universe code repository.

### Chief Technology Officer (CTO)

Responsibilities:

1. Be in frequent contact with other Chief Executives and areas of the company
   to reconcile the current vision of the [products](/development/products).

1. Communicate the vision and requirements of the [products](/development/products)
   to the Head of Product and the Head of Analytics.

1. Decide on proposals that modify the
   [status quo](https://en.wikipedia.org/wiki/Status_quo)
   in any aspect (technical, financial, managerial, ...).

1. Know what's happening everywhere,
   and be ultimately responsible for everything.

1. Intervene and modify whatever is needed to further or protect
   the interests of Fluid Attacks as a business.

:::note
Our current CTO is [Rafael Alvarez](https://www.linkedin.com/in/jralvarezc/).
:::

### Head of Product

Responsibilities:

1. Be in frequent contact with the CTO
   to reconcile the current vision of the [products](/development/products).

1. Communicate the vision and requirements of the [products](/development/products)
   to the Developers.

1. Maintain the Backlog (Bug Tracker) synchronized with the vision.

1. Verify that the business requirements
   have been met
   as Developers modify
   the [products](/development/products) over time.

1. Communicate the progress made by the Developers back to the CTO.

What decisions does the Head of Product take?

1. The head of Product
   defines which Issues in the Bug Tracker will be implemented or ignored,
   in which order will they be solved by the Developers
   (by assigning a priority),
   and which Developers will work on them
   (by assigning/removing them to/from the Issue).

:::note
Our current Head of Product
is [Juan Restrepo](https://www.linkedin.com/in/juancrestrepo/).

This role is a combination of what the Software Industry recognizes as
Business Analyst, Product Owner, and Scrum Master.
:::

### Developers

Responsibilities:

1. Resolve the Issues assigned to them in the Bug Tracker,
   and do so according to the
   [Contributing Guidelines](/development/contributing).

1. Communicate ideas or identified problems
   (for instance through an Issue in the Bug Tracker)
   to the Head of Product.

1. Participate in technical discussions
   where their experience is applicable.

1. Review what other people do, say or ask
   related to something they have personally created or maintained in the past,
   except when another Developer that still works at Fluid Attacks
   has maintained it more recently,
   in which case the most recent Developer
   will take responsibility for the Review.

What decisions do Developers take?

1. Developers can decide on technical matters
   so long as they preserve the
   [status quo](https://en.wikipedia.org/wiki/Status_quo)
   and are
   [homeomorphic](https://en.wikipedia.org/wiki/Homeomorphism)
   and [homogenous](https://en.wikipedia.org/wiki/Homogeneous_function)
   to the existing code base
   (same architecture, stack, programming language, paradigm, ...).

   When the [status quo](https://en.wikipedia.org/wiki/Status_quo)
   is to be modified,
   a public,
   all-developers-wide,
   constructive discussion is initiated,
   either
   through verbal or written communication,
   or a Request For Comments in the Bug Tracker.
   It doesn't suffice to ask the responsible Developer,
   or to seek approval from the perceived technical authorities of the moment.
   **A thought process is mandatory**.

   After some time has passed,
   and sufficient discussion has happened,
   the discussion is brought up to the CTO for a final decision,
   and the outcome is publicly communicated.

1. Developers cannot decide on any non-technical matters,
   the Backlog,
   or the priority of Issues in the Bug Tracker.
   However, they can manifest their importance to the Head of Product,
   who makes the last call,
   or escalates to the CTO as needed.

:::note
The current list of Developers can be found
[here](https://gitlab.com/fluidattacks/universe/-/project_members?sort=access_level_desc).

This role is a combination of what the Software Industry recognizes as
Project Manager, Team Lead, Software Architect, QA, and Tester.
:::
