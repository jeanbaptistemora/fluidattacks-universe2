---
slug: advisories/supply/
title: Uvdesk 1.1.1 - RCE via Insecure File Upload
authors: Carlos Bello
writer: cbello
codename: supply
product: Uvdesk 1.1.1
date: 2023-01-10 09:00 COT
cveid: CVE-2023-0265
severity: 9.9
description: Uvdesk 1.1.1    -     RCE via Insecure File Upload
keywords: Fluid Attacks, Security, Vulnerabilities, Uvdesk, RCE
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Uvdesk 1.1.1 - RCE via Insecure File Upload                        |
| **Code name**         | [Supply](https://en.wikipedia.org/wiki/Air_Supply)                 |
| **Product**           | Uvdesk                                                             |
| **Affected versions** | Version 1.1.1                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2023-01-10                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Insecure file upload                                                                                                        |
| **Rule**              | [027. Insecure file upload](https://docs.fluidattacks.com/criteria/vulnerabilities/027)                                     |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 9.9                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-0265](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0265)                                               |

## Description

Uvdesk version 1.1.1 allows an authenticated remote attacker to execute
commands on the server. This is possible because the application does not
properly validate profile pictures uploaded by customers.

## Vulnerability

This vulnerability occurs because the application does not properly validate
profile pictures uploaded by customers.

## Exploitation

The application only accepts images (validates content and mimetype), however
it does not correctly validate the image extension. Thanks to this we can inject
PHP code in the image comments (so as not to corrupt it), and then through a
proxy we change the image extension to `.php`.

![inject-code-comments](https://user-images.githubusercontent.com/51862990/212500420-0941e1e6-1778-418c-8c52-4176a9db2ba4.png)

![burpsuite-bad-image](https://user-images.githubusercontent.com/51862990/212500190-688d3fed-ad1c-4cb3-9983-21925ba725f7.png)

![command-execute-success](https://user-images.githubusercontent.com/51862990/212500447-76cea3ec-88b5-4739-9211-7fcbec0477a0.png)

## Evidence of exploitation

<iframe src="https://www.veed.io/embed/7e600b02-ed61-4dbf-ab93-7dffae7bb06b"
width="835" height="505" frameborder="0" title="explotation-rce-vdesk.mp4"
webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

## Our security policy

We have reserved the CVE-2023-0265 to refer to this issue from now on.

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
  discovered="2023-12-14"
  contacted="2023-12-14"
  replied="2023-12-14"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
