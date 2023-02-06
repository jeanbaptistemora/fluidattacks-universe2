---
id: response
title: Response
sidebar_label: Response
slug: /about/sla/response
---

## Description

**90%** of reattacks,
comments and incidents
will have a median first response time
of less than **16 office hours**.

## Criteria

All of the following are necessary conditions
for the application of the service-level agreements:

- The group has a Squad Plan.
- Both the environment
  and the source code
  are accessible.
- Remote access
  with no human intervention
  (no captcha, OTP, etc.).
- There are over **500 reattacks**,
  comments or incidents.

## Details

Besides the [general measurement aspects](/about/sla#details),
this SLA is measured
taking into account the following:

- Percentages are determined
  using percentiles.
- Office hours correspond to twelve-hour business days,
  as follows:
  7 AM - 7 PM (GMT-5).
- Only reattacks on vulnerabilities reported as closed.

## Indicator calculation

- For each location,
  compute the response time
  for the last reattack request
  that ended in effective vulnerability close.
  Consider closes performed by Machine
  as reattacks with time to respond = 0.
- Compute the full resolution time
  for incidents reported to help@fluidattacks.com
- Compute the response time
  for each vulnerability comment.
- Merge the response times computed
  in 1, 2 and 3 in a single dataset.
- Exclude the top decile of response times
  and compute the median for the remaining values.
