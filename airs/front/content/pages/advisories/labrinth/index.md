---
slug: advisories/labrinth/
title: Uvdesk 1.1.1    -     Stored Cross-Site Scripting
authors: Carlos Bello
writer: cbello
codename: labrinth
product: Uvdesk 1.1.1
date: 2023-01-10 09:00 COT
cveid: CVE-2023-0325
severity: 7.1
description: Uvdesk 1.1.1    -     Stored Cross-Site Scripting (XSS)
keywords: Fluid Attacks, Security, Vulnerabilities, Uvdesk, XSS
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Uvdesk 1.1.1    -     Stored Cross-Site Scripting                  |
| **Code name**         | [Labrinth](https://en.wikipedia.org/wiki/Labrinth)                 |
| **Product**           | Uvdesk                                                             |
| **Affected versions** | Version 1.1.1                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2023-01-10                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting (XSS)                                                                                           |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)                        |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N                                                                                |
| **CVSSv3 Base Score** | 7.1                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-0325](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0325)                                               |

## Description

Uvdesk version 1.1.1 allows an unauthenticated remote attacker to exploit
a stored XSS in the application. This is possible because the application
does not correctly validate the message sent by the clients in the ticket.

## Vulnerability

This vulnerability occurs because the application does not correctly validate
the message sent by the clients in the ticket.

## Exploitation

We must send the payload xss through the ticket message. It is important to use
a proxy here, because the payload will be encoded from javascript.

![stored-xss-vdesk](https://user-images.githubusercontent.com/51862990/212711265-7ee4c304-e691-441b-a4fe-6d1f3d0485b5.gif)

## Our security policy

We have reserved the CVE-2023-0325 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Uvdesk 1.1.1

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/uvdesk/community-skeleton>

## Timeline

<time-lapse
  discovered="2023-01-16"
  contacted="2023-01-16"
  replied="2023-01-16"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
