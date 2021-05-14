---
id: accuracy
title: Accuracy
sidebar_label: Accuracy
slug: /about/sla/accuracy
---

### Criteria

- Applies only
  to plan Squad.
- It exists
  in both environment
  and source code.
- Coupled environment
  (exact deployment of the branch)
- Stable environment
  (**80%** of business days
  with no open eventualities)
- Complete dataset
  for the corresponding use case.
- Remote access with no human intervention
  (no captcha, OTP, etc.).

### Details

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
- The severity of vulnerabilities
  are calculated using
  CVSSF = 4^(CVSS-4).
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
