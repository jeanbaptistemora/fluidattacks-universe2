---
slug: advisories/osbourne/
title: phpIPAM 1.4.4 - Stored XSS
authors: Oscar Uribe
writer: ouribe
codename: osbourne
product: phpIPAM 1.4.4
date: 2022-01-07 10:00 COT
cveid: CVE-2022-23045
description: phpIPAM 1.4.4 - Stored XSS
keywords: Fluid Attacks, Security, Vulnerabilities, phpIPAM
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                        |
|-----------------------|--------------------------------------------------------|
| **Name**              | phpIPAM 1.4.4 - Stored XSS                             |
| **Code name**         | [Osbourne](https://en.wikipedia.org/wiki/Ozzy_Osbourne)|
| **Product**           | phpIPAM                                                |
| **Affected versions** | 1.4.4                                                  |
| **Fixed versions**    | 1.4.5                                                  |
| **State**             | Public                                                 |
| **Release date**      | 2022-01-18                                             |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting (XSS)                                |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)   |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:L/I:L/A:N                     |
| **CVSSv3 Base Score** | 4.8                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-23045](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23045)                                               |

## Description

PhpIPAM **v1.4.4** allows an authenticated admin user to inject
javascript code inside the "Site title" parameter while updating
the site settings. The "Site title" setting is injected in several
locations which triggers the XSS.

## Proof of Concept

Steps to reproduce:

XSS:

1. Go to "http://192.168.1.5/phpipam/index.php?page=administration&section=settings".
2. Update the "Site Title" parameter with " autofocus onfocus=alert(1)>.
3. Click on 'Save'.
4. If a user visits the setting page the javascript code will be rendered.

Open redirect:

1. Go to "http://192.168.1.5/phpipam/index.php?page=administration&section=settings".
2. Update the "Site Title" parameter with 0;url=https://google.com" http-equiv="refresh".
3. Click on 'Save'.
4. If a user reloads the page will be redirected to https://google.com.

System Information

- Version: phpIPAM IP address management v1.4.4.
- Operating System: Linux.
- Web Server: Apache
- PHP Version: 7.4
- Database and version: Mysql

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

An updated version of PhpIPAM is available at the vendor page.

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
