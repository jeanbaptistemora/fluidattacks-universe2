---
slug: advisories/londra/
title: CandidATS 3.0.0 - CSRF to Privilege Escalation
authors: Carlos Bello
writer: cbello
codename: londra
product: CandidATS 3.0.0 - CSRF to Privilege Escalation
date: 2022-10-27 15:30 COT
cveid: CVE-2022-42751
severity: 8.8
description: CandidATS 3.0.0   -   CSRF to Privilege Escalation
keywords: Fluid Attacks, Security, Vulnerabilities, Candid ATS, Account Takeover, XSS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | CandidATS 3.0.0 - CSRF to Privilege Escalation                     |
| **Code name**         | [Londra](https://en.wikipedia.org/wiki/Paulo_Londra)               |
| **Product**           | CandidATS                                                          |
| **Affected versions** | Version 3.0.0                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-27                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Cross-site request forgery                                                                                                  |
| **Rule**              | [007. Cross-site request forgery](https://docs.fluidattacks.com/criteria/vulnerabilities/007)                               |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 8.8                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-42751](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42751)                                             |

## Description

CandidATS version 3.0.0 allows an external attacker to elevate
privileges in the application. This is possible because the
application suffers from CSRF. This allows to persuade an
administrator to create a new account with administrative
permissions.

## Vulnerability

The stored XSS present in CandidATS 3.0.0 allows a remote attacker
to elevate privileges in the application. To trigger this
vulnerability, we will need to persuade an administrator to open a
malicious link.

## Exploitation

In this attack we will elevate privileges in the application, through
a malicious link.

![candidATS-CSRF-Privilege-Escalation](https://user-images.githubusercontent.com/51862990/198388527-addbe400-26d6-4653-af2c-549585e416c6.gif)

## Our security policy

We have reserved the CVE-2022-42751 to refer to these issues from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: CandidATS 3.0.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://candidats.net/>

## Timeline

<time-lapse
  discovered="2022-10-07"
  contacted="2022-10-07"
  replied="2022-10-07"
  confirmed=""
  patched=""
  disclosure="2022-10-27">
</time-lapse>
