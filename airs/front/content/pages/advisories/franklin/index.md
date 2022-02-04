---
slug: advisories/franklin/
title: Exponent CMS 2.6.0 patch2 - Stored XSS
authors: Oscar Uribe
writer: ouribe
codename: franklin
product: Exponent CMS 2.6.0 patch2
date: 2022-01-24 12:00 COT
cveid: CVE-2022-23047
description: Exponent CMS 2.6.0 patch2 - Stored XSS
keywords: Fluid Attacks, Security, Vulnerabilities, Exponent CMS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                             |                                                          |
|-----------------------------|----------------------------------------------------------|
| **Name**                    | Exponent CMS 2.6.0 patch2 - Stored XSS                   |
| **Code name**               | [Franklin](https://en.wikipedia.org/wiki/Aretha_Franklin)|
| **Product**                 | Exponent CMS                                             |
| **Affected versions**       | v2.6.0 patch2                                            |
| **State**                   | Public                                                   |
| **Release Date**            | 2022-02-03                                               |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting (XSS)                                |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)   |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:L/I:L/A:N                     |
| **CVSSv3 Base Score** | 4.8                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-23047](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23047)                                                    |

## Description

Exponent CMS **2.6.0 patch2** allows an authenticated admin user
to inject persistent javascript code inside the
`Site/Organization Name,Site Title and Site Header` parameters
while updating the site settings on
`http://127.0.0.1/exponentcms/administration/configure_site`.

## Proof of Concept

1. Click on the Exponent logo located on the upper left corner.
2. Go to 'Configure Website'.
3. Update the 'Site Title' field or any of
   the vulnerable fields with the following PoC.

   ```javascript
   Exponent CMS" onmouseover=alert('xss')>
   ```

4. If a user hover the mouse over the logo or visits
   the 'Configure Website' the XSS will be triggered.

System Information:

- Version: Exponent CMS 2.6.0 patch2.
- Operating System: Linux.
- Web Server: Apache
- PHP Version: 7.4
- Database and version: Mysql

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

By 2022-02-03 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://www.exponentcms.org/>                                      |
| **Ticket**          | <https://exponentcms.lighthouseapp.com/projects/61783/tickets/1459> |
| **Issue**           | <https://github.com/exponentcms/exponent-cms/issues/1546>           |

## Timeline

- 2022-01-24: Vulnerability discovered.

- 2022-01-24: Vendor contacted.

- 2022-02-03: Public Disclosure.
