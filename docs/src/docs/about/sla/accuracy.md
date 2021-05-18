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

1. Applies only
  to plan Squad.
1. It exists
  in both environment
  and source code.
1. Pair environment
  (exact deployment of the branch)
1. Stable environment
  (**80%** of business days
  with no open eventualities)
1. Complete dataset
  for the corresponding use case.
1. Remote access with no human intervention
  (no captcha, OTP, etc.).
1. The required transactions
  are less than 400 manual changes
  per active author.

### Details

1. The severity of vulnerabilities
  are calculated using
  CVSSF = 4^(CVSS-4).
1. The accuracy is calculated
  based on the false positives,
  false negatives
  and the F-Score model.
1. Black vulnerabilities
  detectable only via source code
  are not considered
  false negatives.
1. Additionally,
  this SLA is measured
  taking into account
  [these aspects](/about/sla/introduction#details).
