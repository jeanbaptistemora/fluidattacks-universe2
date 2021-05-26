---
id: accuracy
title: Accuracy
sidebar_label: Accuracy
slug: /about/sla/accuracy
---

### Description

**90%** of the severity of vulnerabilities
is detected and has some level of risk.

### Criteria

All of the following aspects
are necessary conditions
for the application
of the service-level agreements:

1. The group has
  a SQUAD plan,
1. Both the environment
  and the source code
  are accesible,
1. The environment is
  pair to the code,
  i.e.,
  the environment corresponds
  to the provided branch,
1. Stable environment
  (**80%** of business days
  with no open eventualities),
1. Complete dataset
  for the corresponding use case,
1. Remote access with no human intervention
  (no captcha, OTP, etc.),
1. 100% health check
  was performed
  to a group
  potentially affected
  by a false negative,
1. Average of **400** weekly changes
  per author
  since service started
  up to the potential
  false negative report.

### Details

Besides the
[general measurement aspects](/about/sla#details),
this SLA is measured
taking into account
the following:

1. The severity of vulnerabilities
  are calculated using
  CVSSF = 4^(CVSS-4),
1. The accuracy is calculated
  based on the false positives,
  false negatives
  and the
  [F-Score model](https://en.wikipedia.org/wiki/F-score),
1. Black vulnerabilities
  detectable only via source code
  are not considered
  false negatives.
