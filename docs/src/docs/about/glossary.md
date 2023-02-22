---
id: glossary
title: Glossary
sidebar_label: Glossary
slug: /about/glossary
---

## CVSS

The Common Vulnerability Scoring System or CVSS
is a free and open industry standard
for assessing the severity
of computer system security vulnerabilities.
CVSS attempts to assign
severity scores to vulnerabilities,
allowing responders to prioritize responses
and resources according to threat.
Scores are calculated based on a formula that
depends on several metrics
that approximate ease of exploit
and the impact of exploit.
Scores range from 0 to 10,
with 10 being the most severe.

## CVSSF

The CVSSF metric is a creation of `Fluid Attacks.`
It shows the level of **risk exposure**
represented by the vulnerabilities in your system.
The **CVSSF** allows an aggregate analysis
of vulnerabilities.
The scale that is handled is from 0.015625 to 4096.
If you want to know more,
you can enter [here.](/about/faq/#severity-vs-vulnerabilities)

## Mailmaps

These are the rules
that must be followed
at the time of
documenting the mailmap:

1. Use the email address
  of the provider
  over the one
  of the client.
    - Use `<eduardo.garcia@company.com>`
      over `Eduardo Garcia` `<eduardo.garcia@corporation.com>`
      or `EduardoGarcia` `<egarcia@institute.edu.co>`.
1. Do not map by default
  a non-corporate email
  such as
  `userdeveloper <user123@gmail.com>`.
1. In order to map
  a non-corporate email
  to a corporate one,
  written request
  from the client
  is required.
## ToE

The Target of Evaluation or ToE
is the product or system
that will be the subject
of the penetration testing
done by `Fluid Attacks`.
The ToE is mostly defined by specifying
which git repositories and/or environments
you want us to check
by adding Git Roots
and its environments
in the Scope section of a group.

> **NOTE:**
> This subsection of our documentation is under construction.

## White box

The white box is a service where
the hacker has all the information
privileges such as Git roots,
credentials,
source code and environments.

## Black box

The black box is a service where
the hacker does not have access to
source code or information of the
IT structure of the project,
having only access to IP and URL,
environments being these services deployed.
