---
id: extensive-logs
title: Extensive Logs
sidebar_label: Extensive Logs
slug: /about/security/non-repudiation/extensive-logs
---

Typical logs are also essential
for a non-repudiation policy to be successful.
Currently,
we store logs for:

- **Attack Surface Manager's logging system:**
  [Attack Surface Manager (ASM)](https://app.fluidattacks.com/)
  stores a historical status of projects,
  findings, vulnerabilities,
  and other critical components.
  Changes made to these components are always tied
  to a user and a date.
  The historical status never expires.
  These logs cannot be modified.

- **ASM's error tracking system:**
  ASM provides real-time logging of errors
  that occur in its production environments.
  It is especially useful for quickly detecting
  new errors and hacking attempts.
  These logs never expire and cannot be modified.

- **Redundant data centers:**
  These store comprehensive logs of all
  our infrastructure components.
  Logs here never expire and cannot be modified.

- **DevSecOps execution:**
  Whenever a client's
  [CI pipeline](https://fluidattacks.com/about/security/#CI)
  runs DevSecOps,
  logs containing information
  such as who ran it,
  vulnerability status,
  and other relevant data are uploaded
  to our data centers.
  This allows us to always know
  the current status of our client's DevSecOps service.
  These logs never expire and cannot be modified.

- **IAM authentication:**
  Our IAM stores logs of user login attempts,
  accessed applications,
  and possible threats.
  Logs here expire after seven days
  and cannot be modified.

- **Collaboration systems activity:**
  Our collaboration systems,
  such as email, calendar, etc.,
  store comprehensive employee activity logs,
  spam, phishing and malware emails,
  suspicious login attempts,
  and other potential threats.
  Employee activity logs never expire.
  Other security logs expire after 30 days.
  These logs cannot be modified.

- **CI job logs:**
  All our [CI pipelines](https://fluidattacks.com/about/security/#CI)
  provide a full record of who triggered them,
  when,
  and the console output.
  These logs never expire and cannot be modified.
