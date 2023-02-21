---
slug: advisories/stewart/
title: Bhima 1.27.0 - Account Takeover via IDOR
authors: Carlos Bello
writer: cbello
codename: stewart
product: Bhima 1.27.0 - Account Takeover via IDOR
date: 2023-02-27 12:00 COT
cveid: CVE-2023-0944
severity: 7.6
description: Bhima 1.27.0      -      Account Takeover via IDOR
keywords: Fluid Attacks, Security, Vulnerabilities, IDOR, Bhima, Account Takeover
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Bhima 1.27.0 - Account Takeover via IDOR                           |
| **Code name**         | [Stewart](https://en.wikipedia.org/wiki/Rod_Stewart)               |
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
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L                                                                                |
| **CVSSv3 Base Score** | 7.6                                                                                                                         |
| **Exploit available** | No                                                                                                                          |
| **CVE ID(s)**         | [CVE-2023-0944](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0944)                                               |

## Description

Bhima version 1.27.0 allows an authenticated attacker with regular user
permissions to update arbitrary user session data such as username, email
and password. This is possible because the application is vulnerable to IDOR,
it does not correctly validate user permissions with respect to certain actions
that can be performed by the user.

## Vulnerability

This vulnerability occurs because the application is vulnerable to IDOR, it does
not correctly validate user permissions with respect to certain actions that can
be performed by the user.

## Evidence of exploitation

A user with generic permissions can update the administrator session data through
an IDOR.

![idor-change-info](https://user-images.githubusercontent.com/51862990/220455447-73baa0c6-a367-425d-a0f7-151dc521b7e2.png)

A user with generic permissions can update the administrator password through an
IDOR.

![idor-change-password](https://user-images.githubusercontent.com/51862990/220455527-1c6b6ec5-1bd2-4b16-a518-92d57386f954.png)

Here we can see that from the front end we cannot access any administrative
interface to update user data (the administrator in our case).

However, this functionality is only hidden. If we send the request to update
this data from an account with general permissions, we will not be stopped for
lack of permissions.

This way we will be able to compromise any registered account from a general
account (without administrator permissions clearly).

![ato-bhima](https://user-images.githubusercontent.com/51862990/220455637-87c27e2d-e93a-46f0-b025-311ba5b6291b.gif)

## Our security policy

We have reserved the ID CVE-2023-0944 to refer to this issue from now on.

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
  discovered="2023-02-21"
  contacted="2023-02-21"
  replied="2023-02-21"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
