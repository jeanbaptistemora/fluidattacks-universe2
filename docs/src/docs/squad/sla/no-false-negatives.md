---
id: no-false-negatives
title: No false negatives
sidebar_label: No false negatives
slug: /squad/sla/no-false-negatives
---

### Description

**90%** of vulnerabilities
adjusted for severity
are detected.

### Preconditions

- It exists in both environment and source code.
- Coupled environment
  (exact deployment of the branch)
- Stable environment
  (**80%** of business days
  with no open eventualities)
- Complete dataset
  for the corresponding use case.
- Remote access with no human intervention
  (no captcha, OTP, etc.).

### Measurement

- Measured in
  calendar quarters.
- Taking into account
  all the groups
  of the organization
  over time.
- Taking into account
  all the historical data,
  not only that of
  the quarterly analisis period.
- Percentages are determined
  using percentiles.
- The severity adjustment of vulnerabilities
  are perfomed using CVSSF = 4^(CVSS-4).
- The accuracy is calculated
  based on the false positives,
  false negatives
  and the F-Score model.
- Black vulnerabilities
  detectable only via source code
  are not considered
  false negatives.
- The required transactionalities
  for measurement and penalty are:
    - Less than **400** manual changes
      per active author.
