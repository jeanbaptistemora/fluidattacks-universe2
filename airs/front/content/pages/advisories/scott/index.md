---
slug: advisories/scott/
title: Ulearn a5a7ca20de859051ea0470542844980a66dfc05d - RCE
authors: Carlos Bello
writer: cbello
codename: scott
product: Ulearn a5a7ca20de859051ea0470542844980a66dfc05d
date: 2023-02-03 12:00 COT
cveid: CVE-2023-0670
severity: 9.1
description: Ulearn a5a7ca20de859051ea0470542844980a66dfc05d - RCE
keywords: Fluid Attacks, Security, Vulnerabilities, Ulearn, RCE
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                         |
| --------------------- | ------------------------------------------------------- |
| **Name**              | Ulearn a5a7ca20de859051ea0470542844980a66dfc05d - RCE   |
| **Code name**         | [Scott](https://en.wikipedia.org/wiki/Travis_Scott)     |
| **Product**           | Ulearn                                                  |
| **Affected versions** | a5a7ca20de859051ea0470542844980a66dfc05d                |
| **State**             | Public                                                  |
| **Release Date**      | 2023-02-03                                              |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------|
| **Kind**              | Insecure file upload                                                                                   |
| **Rule**              | [027. Insecure file upload](https://docs.fluidattacks.com/criteria/vulnerabilities/027)                |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H                                                           |
| **CVSSv3 Base Score** | 9.1                                                                                                    |
| **Exploit available** | No                                                                                                     |
| **CVE ID(s)**         | [CVE-2023-0670](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0670)                          |

## Description

Ulearn version a5a7ca20de859051ea0470542844980a66dfc05d allows an attacker
with administrator permissions to obtain remote code execution on the
server through the image upload functionality. This occurs because the
application does not validate that the uploaded image is actually an image.

## Vulnerability

This vulnerability This occurs because the application does not validate
that the uploaded image is actually an image.

## Evidence of exploitation

To exploit this vulnerability, we only need to send the following malicious
PHP code to the server.

![rce-ulearn](https://user-images.githubusercontent.com/51862990/216733146-d08069b5-d082-432a-8647-a8dd133c8ff6.gif)

## Our security policy

We have reserved the ID CVE-2023-0670 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Ulearn a5a7ca20de859051ea0470542844980a66dfc05d

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/ulearnpro/ulearn/>

## Timeline

<time-lapse
  discovered="2023-02-03"
  contacted="2022-02-03"
  replied="2022-02-03"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
