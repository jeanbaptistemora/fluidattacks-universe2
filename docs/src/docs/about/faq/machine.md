---
id: machine
title: Machine
sidebar_label: Machine
slug: /about/faq/machine
---

## What is the Machine plan?

Machine is a bot which
continuously looks for
vulnerabilities in groups
with active machine subscriptions.

## When does Machine run?

Machine runs continuously
24 hours 7 days
looking for vulnerabilities
in both source code and environments.

## Where does Machine run?

Fluid Attacks's Machine
runs over the environments
and repositories
defined in the Scope (GitRoots),
taking into account
the folder and files exclusions
defined in the gitignores.

## Can I schedule Machine to run over specific times?

No.
In real life scenarios,
real hackers won't take into account
labour days nor specific hours
to perform an attack.

## What happens if I turn off my environments in specific times?

Machine won't report
vulnerabilities on source code
that cannot be cloned
or environments that
do not respond back
to incoming connections.

However in pre-productive environments,
it is expected to find environments
which are not available 24/7
due to different reasons.

As a security company,
we perform our penetration testing
in the most strict configuration,
checking all our environments as production.
Hence,
vulnerabilties found
out of labour hours
are also valid reports.
