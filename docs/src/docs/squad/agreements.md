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
  **99%** of the planned time,
  the platform will be available via internet
  for its registered users.
2. No False Negatives:
  **90% - 95%** of vulnerabilities adjusted for severity
  are detected if each active author
  makes up to **400 - 600**
  manual changes.
3. No False Positives:
  **90% - 95%** of vulnerabilities adjusted for severity
  have some level of risk.
4. Reattacks:
  **90%** of reattacks
  to effectively closed vulnerabilities
  will have a median response time
  of less than **24 - 18** office hours.
5. First Response:
  **90%** of comments and/or incidents of the program
  will have median first response time
  of less than **12 - 8** office hours.

## Measurement

All of the SLAs:

1. Are measured in
  full calendar quarters:
    - (January 1st to March 31st,
      April 1st to June 30th,
      July 1st to Setember 30th,
      October 1st to December 31st)
2. Apply penalties
  when the required transactionality
  is available:
    - Over **100** reattacks,
    - Over **100** comments and/or incidents,
    - Each active author
    makes less than **600**
    weekly manual changes (accuracy).
3. Take into account
  all the subscriptions
  hired by the organization
  over time (program).
4. Take into account
  all the historical data,
  not only that of
  the quarterly analisis period.
5. Determine the percentage
  using percentiles:
    - I.e,
      sorting from highest to lowest
      according to a variable,
      and selecting the N%
      of units of least value.
    - Another way to express this
      is excluding the top outliers
      of this same calculation.
6. Perform the severity adjustment of vulnerabilities
  using CVSSF = 4^(CVSS-4).
7. Offices hours correspond to
  bussiness days from 7AM to 7PM.
8. For partial availability failures
  (only for one functionality),
  the measurement will be based on
  the affected office hours
  and will be adjusted
  according to the percentage
  of affected ASM users.
  Examples:
    - 4 hours from 4PM to 8PM
      for 10 of 100 registered users,
      corresponds to
      2H x <25% = 0.5 hours
    - 3H from 8AM to 11AM
      for all users
      = 3H long impact
9. All SLAs apply to both White and Black,
  the only difference is that in Black
  it is not considered a leak
  the vulnerability that to be discovered
  required a White.
  Example:
  Use of outdated cryptography.

## Penalty

1. In case of breaching **2** or more SLAs,
  a **1%** discount will apply
  to the monthly cost of the program
  over the next quarter.
