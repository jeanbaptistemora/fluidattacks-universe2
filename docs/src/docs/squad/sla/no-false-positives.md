---
id: no-false-positives
title: No false positives
sidebar_label: No false positives
slug: /squad/sla
---

### Description

**90%** of vulnerabilities
adjusted for severity
have some level of risk.

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
- Offices hours correspond to
  8 hours bussiness days like this,
  8AM-12M and 1PM-5PM.
- The required transactionalities
  for measurement and penalty are:
    - Over **500** comments,
      reattacks 
      and/or incidents.