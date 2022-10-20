---
slug: advisories/tiesto/
title: relatedcode/Messenger 7bcd20b - Broken Access Control
authors: Carlos Bello
writer: cbello
codename: tiesto
product: relatedcode/Messenger 7bcd20b
date: 2022-10-14 12:30 COT
cveid: CVE-2022-41708
severity: 6.5
description: relatedcode/Messenger 7bcd20b  -  Broken Access Control
keywords: Fluid Attacks, Security, Vulnerabilities, Relatedcode, Messenger
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | relatedcode/Messenger 7bcd20b  -  Broken Access Control            |
| **Code name**         | [Tiesto](https://en.wikipedia.org/wiki/Ti%C3%ABsto)                |
| **Product**           | relatedcode/Messenger                                              |
| **Affected versions** | Version 7bcd20b                                                    |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-14                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Improper authorization control for web services                                                                             |
| **Rule**              | [039. Improper authorization control for web services](https://docs.fluidattacks.com/criteria/vulnerabilities/039)          |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 6.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41708](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41708)                                             |

## Description

Relatedcode/Messenger version 7bcd20b allows an authenticated external
attacker to access existing chats in the workspaces of any user of the
application. This is possible because the application does not validate
permissions correctly.

## Vulnerability

The application does not validate the application permissions correctly.
Thanks to this we can access confidential information of any user
registered on the server. Here we will see how an attacker manages
to access the internal chats of the victim user:

![image.png](https://user-images.githubusercontent.com/51862990/195903319-78dec301-fa82-42b0-b239-d845ef0d1c8d.png)

## Exploitation

To exploit this broken access control, one must first exploit another
vulnerability present in the application. This vulnerability involves
the [disclosure of sensitive information](../coldplay/).

Thanks to it I was able to gather the necessary data to be able to
obtain the internal chat logs of other users of the application:

![image.png](https://user-images.githubusercontent.com/51862990/195905224-035fa526-5785-4437-aab7-9592f49fa2b5.png)

## Impact

An authenticated remote attacker can access internal chat logs of arbitrary
users of the application.

## Our security policy

We have reserved the CVE-2022-41708 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: relatedcode/Messenger 7bcd20b

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/relatedcode/Messenger>

## Timeline

<time-lapse
  discovered="2022-09-23"
  contacted="2022-09-23"
  replied="2022-09-23"
  confirmed="2022-09-23"
  patched=""
  disclosure="2022-10-14">
</time-lapse>
