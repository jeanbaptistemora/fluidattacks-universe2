---
slug: advisories/ingrosso/
title: Bhima 1.27.0 - Sensitive Information Disclosure via IDOR
authors: Carlos Bello
writer: cbello
codename: ingrosso
product: Bhima 1.27.0 - Sensitive Information Disclosure via IDOR
date: 2023-02-27 12:00 COT
cveid: CVE-2023-0967
severity: 6.5
description: Bhima 1.27.0      -      Sensitive Information Disclosure via IDOR
keywords: Fluid Attacks, Security, Vulnerabilities, IDOR, Bhima, Sensitive Information Disclosure
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Bhima 1.27.0 - Sensitive Information Disclosure via IDOR           |
| **Code name**         | [Ingrosso](https://en.wikipedia.org/wiki/Sebastian_Ingrosso)       |
| **Product**           | Bhima                                                              |
| **Affected versions** | Version 1.27.0                                                     |
| **State**             | Public                                                             |
| **Release date**      | 2023-02-27                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Insecure object reference                                                                                                   |
| **Rule**              | [013. Insecure object reference](https://docs.fluidattacks.com/criteria/vulnerabilities/013)                                |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 6.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-0967](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0967)                                               |

## Description

Bhima version 1.27.0 allows an attacker authenticated with normal user
permissions to view sensitive data of other application users and data
that should only be viewed by the administrator. This is possible because
the application is vulnerable to IDOR, it does not properly validate user
permissions with respect to certain actions the user can perform.

## Vulnerability

This vulnerability occurs because the application is vulnerable to IDOR, it
does not correctly validate user permissions with respect to certain actions
that can be performed by the user.

## Exploitation

### Evidence of exploitation

![idor-leak-data](https://user-images.githubusercontent.com/51862990/220761163-3f561935-f22e-4c40-bc99-ce02afb3c637.gif)

## Our security policy

We have reserved the ID CVE-2023-0967 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Bhima 1.27.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/IMA-WorldHealth/bhima/>

## Timeline

<time-lapse
  discovered="2023-02-22"
  contacted="2023-02-22"
  replied="2023-02-22"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
