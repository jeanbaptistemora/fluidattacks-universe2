---
id: accuracy
title: Accuracy
sidebar_label: Accuracy
slug: /about/sla/accuracy
---

## Description

**90%** of the severity of vulnerabilities is detected
and has some level of risk.

## Criteria

All of the following are necessary conditions
for the application of the service-level agreements:

- The group has a Squad Plan.
- Both the environment
  and the source code
  are accessible.
- The environment is paired with the code,
  i.e.,
  the environment corresponds to the provided branch.
- Stable environment
  (**80%** of business days
  with no open eventualities).
- Complete dataset
  for the corresponding use case.
- Remote access with no human intervention
  (no captcha, OTP, etc.).
- 100% Health Check was performed
  on a group potentially affected
  by a false negative.
- Average of **400** weekly changes per author
  from the start of service
  to the potential false negative report.

## Details

Besides the [general measurement aspects](/about/sla#details),
this SLA is measured
taking into account the following:

- The severity of vulnerabilities are calculated
  using [CVSSF = 4^(CVSS-4)](/about/faq/#adjustment-by-severity).
- The accuracy is calculated
  based on the false positives,
  false negatives
  and the [F-Score model](https://en.wikipedia.org/wiki/F-score).
- Black vulnerabilities
  detectable only via source code
  are not considered false negatives.
