---
id: machine
title: Machine
sidebar_label: Machine
slug: /about/faq/machine
---

## What is Fluid Attacks' Machine?

`Fluid Attacks'` Machine is a bot
that continuously looks for vulnerabilities
in groups with active machine subscriptions.

## When does Machine run?

Machine runs continuously 24 hours,
7 days a week,
looking for vulnerabilities
in both source code and environments.

## Where does Machine run?

Machine runs in the environments
and repositories
defined in the Scope (GitRoots),
taking into account
the folder and file exclusions
defined in the gitignores.

## Can I schedule Machine to run over specific times?

No.
In real life scenarios,
real hackers won't take into account working days
nor specific hours
to perform an attack.

## What happens if I turn off my environments at specific times?

Machine won't report vulnerabilities on source code
that cannot be cloned
or environments that do not respond
to incoming connections.

However,
in pre-production,
it is expected to find environments
that are not available 24/7
due to different reasons.

As a security company,
we perform our penetration testing
in the strictest configuration,
checking all our environments
as if they were in production.
Hence,
vulnerabilities found
outside of working hours
are also valid reports.
