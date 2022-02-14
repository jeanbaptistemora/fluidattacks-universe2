---
id: estimation
title: Estimation
sidebar_label: Estimation
slug: /about/faq/estimation
---

## What information is needed in order to provide a price estimate?

To provide a price estimate, we
need to determine the objective
of the evaluation, which we refer
to as the scope.
Therefore, we require the
following information depending
on the plan you choose.

### One-Shot Hacking (per project)

- How many ports are included
  within the scope?

  1. On-premises or cloud infrastructure
  1. Number of Internet-connected servers to evaluate
  1. Number of servers on internal network to evaluate
  1. Number of wired network devices to
     evaluate (e.g., switches, routers, firewalls)
  1. Number of wireless network devices to evaluate
     (e.g., SSIDs, switches, routers, firewalls)

- How many application entry points
  are included within the scope?

  1. Application name
  1. Application type (i.e., mobile, web or desktop)
  1. Total input fields
  1. Requires authentication
  1. Testing method (i.e., black, gray or white-box)
  1. Internet-connected application or
     internal network application
  1. Special installations by the client (e.g., specific
     browser version browser extensions, digital certificates)

  > **NOTE:**
  > In this scenario, we evaluate the application
  > without knowledge of its internal workings
  > and without credentials.
  > **Gray-box testing:** This scenario includes
  > black-box testing plus an internal evaluation
  > of the application that requires the client
  > to provide access credentials.
  > **White-box testing:** This scenario includes
  > black and gray-box testing plus evaluation
  > of the source code.

- How many Lines of Code (LOC) are
  included within the scope?

We recommend using Tokei
to carry on the
quantification of LOC.
These are the instructions for
using this software:

1. Download Tokei at https://github.com/XAMPPRocky/tokei
1. Run Tokei using `$ tokei <code path> --output yaml > LOC.yaml`
  to get a YAML file

Preferably, access credentials are
provided (e.g., access credentials
of a standard user with low-level privileges).

### Continuous Hacking with Machine Plan

- How many applications or groups
  will be included in the security test?

- What programming languages does
  the application have?

### Continuous Hacking with Squad Plan

- How many applications or groups
  will be included in the security
  test?

- How many developers are working
  on the client’s application?

- How many LOC are included
  within the scope?

The Health Check service requires
the client to provide us with how
many LOC are developed.
We recommend using Tokei to carry
on the quantification of LOC.
These are the instructions for
using this software:

1. Download Tokei at https://github.com/XAMPPRocky/tokei
1. Run Tokei using `$ tokei <code path> --output yaml > LOC.yaml`
  to get a YAML file
