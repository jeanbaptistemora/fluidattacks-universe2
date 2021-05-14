---
id: agreements
title: Agreements
sidebar_label: Agreements
slug: /squad
---

The following sections
specify information about the agreements
to take into account
when making use of Fluid Attacks products.

## Details

1. Availability:
  **99%** of the planned availability time,
  the platform will be available via internet
  for its registered users.
2. No False Negatives:
  **90%** of vulnerabilities
  adjusted for severity
  are detected.
3. No False Positives:
  **90%** of vulnerabilities adjusted for severity
  have some level of risk.
4. Reattacks:
  **90%** of reattacks
  to effectively closed vulnerabilities
  will have a median response time
  of less than **24** office hours.
5. First Response:
  **90%** of comments and/or incidents
  will have median first response time
  of less than **12** office hours.

## Measurement

All of the SLAs:

1. Are measured in
  calendar quarters.
2. Take into account
  all the groups
  of the organization
  over time.
3. Take into account
  all the historical data,
  not only that of
  the quarterly analisis period.
4. Determine the percentage
  using percentiles.
5. Perform the severity adjustment of vulnerabilities
  using CVSSF = 4^(CVSS-4).
6. Offices hours correspond to
   8 hours bussiness days like this,
   8AM-12M and 1PM-5PM.
7. For partial availability failures
  (only for one functionality),
  the measurement will be based on
  the affected office hours
  and will be adjusted
  according to the percentage
  of affected users.
8. Black vulnerabilities
  detectable only via source code
  are not considered
  false negatives.
9. The required transactionalities
  for measurement and penalty are:
    - Over **500** reattacks,
    - Over **500** comments and/or incidents,
    - Less than **400** manual changes
      per active author.
## Penalty

1. In case of breaching **3** or more SLAs,
  a **1%** discount will apply
  to the monthly cost of the program
  over the next **quarter**.
