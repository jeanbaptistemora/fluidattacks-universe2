---
slug: advisories/cobain/
title: Exponent CMS 2.6.0 patch2 - Stored XSS (User-Agent)
authors: Oscar Uribe
writer: ouribe
codename: cobain
product: Exponent CMS 2.6.0 patch2
date: 2022-01-25 12:00 COT
cveid: CVE-2022-23049
description: Exponent CMS 2.6.0 patch2 - Stored XSS (User-Agent)
keywords: Fluid Attacks, Security, Vulnerabilities, Exponent CMS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                             |                                                          |
|-----------------------------|----------------------------------------------------------|
| **Name**                    | Exponent CMS 2.6.0 patch2 - Stored XSS (User-Agent)      |
| **Code name**               | [Cobain](https://en.wikipedia.org/wiki/Kurt_Cobain)      |
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
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N                     |
| **CVSSv3 Base Score** | 5.4                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-23049](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23049)                                                    |

## Description

Exponent CMS **2.6.0 patch2** allows an authenticated user
to inject persistent javascript code on the User-Agent when
logging in. When an administratoruser visits the 'User Sessions'
tab, the javascript will be triggered allowingan attacker to
compromise the administrator session.

## Proof of Concept

1. Use a Web proxy or a tool to modify the browser
   User-agent with the following PoC.

   ```javascript
   User-Agent: <script>alert('XSS')</script>
   ```

2. Try to login with a non-admin user.
3. If an admin user visits 'User Management' > 'User Sessions' the XSS will be triggered.

A non-admin user may compromise an admin session by exploiting this vulnerability.

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
| **Ticket**          | <https://exponentcms.lighthouseapp.com/projects/61783/tickets/1461> |
| **Issue**           | <https://github.com/exponentcms/exponent-cms/issues/1546>           |

## Timeline

- 2022-01-25: Vulnerability discovered.

- 2022-01-25: Vendor contacted.

- 2022-02-03: Public Disclosure.
