---
slug: advisories/charles/
title: Money Transfer Management System 1.0 - DOM-Based XSS
authors: Oscar Uribe
writer: ouribe
codename: charles
product: Money Transfer Management System 1.0
date: 2022-03-15 12:00 COT
cveid: CVE-2022-25221
description: Money Transfer Management System 1.0 - DOM-Based XSS
keywords: Fluid Attacks, Security, Vulnerabilities, MTMS, XSS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                      |
|-------------------------|------------------------------------------------------|
| **Name**                | Money Transfer Management System - DOM-Based XSS     |
| **Code name**           | [Charles](https://en.wikipedia.org/wiki/Ray_Charles) |
| **Product**             | Money Transfer Management System                     |
| **Affected versions**   | Version 1.0                                          |
| **State**               | Public                                               |
| **Release date**        | 2022-03-15                                           |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | DOM-Based Cross-Site Scripting (XSS)                             |
| **Rule**              | [371. DOM-Based Cross-Site Scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/371)    |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N                     |
| **CVSSv3 Base Score** | 4.3                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-25221](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25221)                                                     |

## Description

Money Transfer Management System **Version 1.0** allows an attacker
an attacker to inject JavaScript code in the url and then trick a user
into visits the link in order to execute JavaScript code.

## Proof of Concept

Steps to reproduce

1. Send the following url to a victim `http://127.0.0.1/mtms/admin/?page=xss';alert('XSS');//`

2. If a victim visits the link the JavaScript code will be triggered.

System Information

* Version: Money Transfer Management System version 1.0.
* Operating System: Linux.
* Web Server: Apache
* PHP Version: 7.4
* Database and version: MySQL

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

By 2022-03-15 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://www.sourcecodester.com/php/15015/money-transfer-management-system-send-money-businesses-php-free-source-code.html>           |

## Timeline

* 2022-02-15: Vulnerability discovered.

* 2022-02-15: Vendor contacted.

* 2022-03-15: Public Disclosure.
