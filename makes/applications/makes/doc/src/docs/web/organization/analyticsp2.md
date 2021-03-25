---
id: analyticsp2
title: Analytics - Part 2
sidebar_label: Analytics - Part 2
slug: /web/organization/analyticsp2
---

### Findings being re-attacked

Once your team has solved a vulnerability you can request a re-attack.
In the re-attack process a hacker will replay the attack vector and confirm that
the proposed solution actually shields your system. In case it does not, your team
will be notified and the finding kept open.

### Days since last remediation

Days since a finding was effectively closed.

### Mean time to remediate (all vulnerabilities)

Amount of time (in days) it takes to your team to fix a security vulnerability.

### Mean time to remediate (non treated vulnerabilities)

Amount of time (in days) it takes to your team to fix a security vulnerability,
excluding accepted vulnerabilities.

### Severity

Security vulnerabilities are ranked based on C.V.S.S. v3.1. The higher the score,
the more damage an attack can make to your system, and the easier it is to carry it on.

### Active resources distribution

Resources can be of two types: Repository and Environment.

- Environment: A URL or IP pointing to an instance of your system.
- Repository: The associated source-code of the environment and (ideally) its infrastructure.

The maximum benefit is reached when every environment has its full source-code available
for us to test it.
