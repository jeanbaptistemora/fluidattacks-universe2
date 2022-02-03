---
slug: advisories/mercury/
title: phpIPAM 1.4.4 - SQL Injection
authors: Oscar Uribe
writer: ouribe
codename: mercury
product: phpIPAM 1.4.4
date: 2022-01-07 14:00 COT
cveid: CVE-2022-23046
description: phpIPAM 1.4.4 - SQL Injection
keywords: Fluid Attacks, Security, Vulnerabilities, phpIPAM
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                          |
|-----------------------|----------------------------------------------------------|
| **Name**              | phpIPAM 1.4.4 - SQL Injection                            |
| **Code name**         | [Mercury](https://en.wikipedia.org/wiki/Freddie_Mercury) |
| **Product**           | phpIPAM                                                  |
| **Affected versions** | 1.4.4                                                    |
| **Fixed versions**    | 1.4.5                                                    |
| **State**             | Public                                                   |
| **Release date**      | 2022-01-18                                               |

## Vulnerability

|                       |                                                                                    |
|-----------------------|------------------------------------------------------------------------------------|
| **Kind**              | SQL injection                                                                      |
| **Rule**              | [010. SQL injection](https://docs.fluidattacks.com/criteria/vulnerabilities/146)   |
| **Remote**            | Yes                                                                                |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:L/A:L                                       |
| **CVSSv3 Base Score** | 4.7                                                                                |
| **Exploit available** | No                                                                                 |
| **CVE ID(s)**         | [CVE-2022-23046](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23046)                                                                 |

## Description

phpIPAM **v1.4.4** allows an authenticated admin user to inject
SQL sentences in the "subnet" parameter while searching a subnet
via `app/admin/routing/edit-bgp-mapping-search.php`.

## Proof of Concept

Steps to reproduce

1. Go to settings and enable the routing module.
2. Go to show routing.
3. Click on "Add peer" and create a new "BGP peer".
4. Click on the newly created "BGP peer".
5. Click on "Actions" and go to "Subnet Mapping".
6. Scroll down to "Map new subnet".
7. Insert an SQL Injection sentence inside the search parameter,
   for example: `" union select @@version,2,user(),4 -- -`.

System Information

- Version: phpIPAM IP address management v1.4.4.
- Operating System: Linux.
- Web Server: Apache
- PHP Version: 7.4
- Database and version: Mysql

## Exploit

An exploit developed for another researcher can be found at
[ExploitDB](https://www.exploit-db.com/exploits/50684).

## Mitigation

An updated version of phpIPAM is available at the vendor page.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                 |
|---------------------|-----------------------------------------------------------------|
| **Vendor page**     | <https://phpipam.net/>                                          |
| **Patched version** | <https://github.com/phpipam/phpipam/releases/tag/v1.4.5>        |

## Timeline

- 2022-01-06: Vulnerability discovered.

- 2022-01-07: Vendor contacted.

- 2022-01-07: Vendor replied acknowledging the report.

- 2022-01-17: Vulnerability patched.

- 2022-01-18: Public Disclosure.
