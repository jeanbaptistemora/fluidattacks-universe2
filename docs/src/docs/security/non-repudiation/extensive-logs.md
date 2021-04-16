---
id: extensive-logs
title: Extensive logs
sidebar_label: Extensive logs
slug: /security/non-repudation/extensive-logs
---

Typical logs are also essential for a non-repudiation policy to be successful.
Currently, we store logs for:

- **ASM’s logging system:** ASM stores a historical status of projects, findings, vulnerabilities,
and other critical components. Changes made to these components are always tied to a user
and a date. The historical status never expires.

- **ASM’s error tracking system:** It provides real-time logging of errors that occur in its
production environments. It is especially useful for quickly detecting new errors and hacking
attempts. These logs never expire.

- **Redundant data centers:** These store comprehensive logs of all our infrastructure components.
Logs here never expire.

- **DevSecOps execution:** Whenever a client’s [CI pipeline](https://fluidattacks.com/security/#CI)
runs DevSecOps, logs containing information like who ran it, vulnerability status, and other
relevant data are uploaded to our data centers, allowing us to always know the current status of
our client’s DevSecOps service. These logs never expire.

- **IAM authentication:** Our IAM stores logs of login attempts made by users,
accessed applications, and possible threats. Logs here expire after seven (7) days.

- **Collaboration systems activity:** Our collaboration systems such as email, calendar, etc.,
store comprehensive logs of employee activity, spam, phishing and malware emails, suspicious
login attempts, and other potential threats. Employee activity logs never expire.
Other security logs expire after 30 days.

- **CI job logs:** All our [CI pipelines](https://fluidattacks.com/security/#CI) provide a full
record of who triggered them, when, and the console output. These logs never expire.
