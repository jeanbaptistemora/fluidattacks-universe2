---
slug: advisories/castles/
title: CandidATS 3.0.0 - Stored XSS to Account Takeover
authors: Carlos Bello
writer: cbello
codename: castles
product: CandidATS 3.0.0 - Stored XSS to Account Takeover
date: 2022-10-27 14:00 COT
cveid: CVE-2022-42750
severity: 8.8
description: CandidATS 3.0.0  -  Stored XSS to Account Takeover
keywords: Fluid Attacks, Security, Vulnerabilities, Candid ATS, Account Takeover, XSS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | CandidATS 3.0.0 - Stored XSS to Account Takeover                   |
| **Code name**         | [Castles](https://en.wikipedia.org/wiki/Crystal_Castles)           |
| **Product**           | CandidATS                                                          |
| **Affected versions** | Version 3.0.0                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-27                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting (XSS)                                                                                           |
| **Rule**              | [083. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)                        |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 8.8                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-42750](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42750)                                             |

## Description

CandidATS version 3.0.0 allows an external attacker to steal the
cookie of arbitrary users. This is possible because the application
does not correctly validate the files uploaded by the user.

## Vulnerability

The Stored XSS present in CandidATS 3.0.0 allows an unauthenticated
remote attacker to perform an Account Takeover. To trigger this
vulnerability, we will need to force a user to upload a malicious
file and wait for them to view the file.

## Exploitation

In this attack we will obtain the administrator user account, through
a malicious link.

![candidats-xssStored](https://user-images.githubusercontent.com/51862990/198366768-1ca0abdf-00b2-4d21-bb60-ec5427b8f701.gif)

![exploit.png](https://user-images.githubusercontent.com/51862990/198366200-3565e154-d7f0-4941-a0be-3662d11284fa.png)

## Our security policy

We have reserved the CVE-2022-42750 to refer to these issues from now on.

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
