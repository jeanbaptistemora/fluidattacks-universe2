---
slug: advisories/jagger/
title: Money Transfer Management System 1.0 - SQL Injection
authors: Oscar Uribe
writer: ouribe
codename: jagger
product: Money Transfer Management System 1.0
date: 2022-03-15 12:00 COT
cveid: CVE-2022-25223
severity: 4.3
description: Money Transfer Management System 1.0 - SQL Injection
keywords: Fluid Attacks, Security, Vulnerabilities, MTMS, SQL
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                                  |
|-------------------------|------------------------------------------------------------------|
| **Name**                | Money Transfer Management System - SQL Injection                 |
| **Code name**           | [Jagger](https://en.wikipedia.org/wiki/Mick_Jagger)              |
| **Product**             | Money Transfer Management System 1.0                             |
| **Affected versions**   | Version 1.0                                                      |
| **State**               | Public                                                           |
| **Release date**        | 2022-03-15                                                       |

## Vulnerability

|                       |                                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| **Kind**              | SQL injection                                                                   |
| **Rule**              | [146. SQL injection](https://docs.fluidattacks.com/criteria/vulnerabilities/146)|
| **Remote**            | Yes                                                                             |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N                                    |
| **CVSSv3 Base Score** | 4.3                                                                             |
| **Exploit available** | No                                                                              |
| **CVE ID(s)**         | [CVE-2022-25223](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25223)                                                                                      |

## Description

Money Transfer Management System **Version 1.0** allows an
authenticated user to inject SQL queries
in `mtms/admin/?page=transaction/view_details` via the `id` parameter.

## Proof of Concept

Steps to reproduce

1. Log in to the application as a normal user.
2. Go to `http://127.0.0.1/mtms/admin/?page=transaction/view_details&id=1`
3. Insert the following query inside the `id` parameter.

```sql
id=a' union select 1,user(),2,4,5,6,7,8,9,10-- -
```

4. The current database user will be shown inside the `Tracking Code` field.

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
