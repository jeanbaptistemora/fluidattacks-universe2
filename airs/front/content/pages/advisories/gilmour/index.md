---
slug: advisories/gilmour/
title: PHP Server Monitor v3.5.2 - Stored XSS
authors: Oscar Uribe
writer: ouribe
codename: gilmour
product: PHP Server Monitor v3.5.2
date: 2022-01-11 15:00 COT
cveid: CVE-2022-23044
severity: 4.8
description: PHP Server Monitor v3.5.2 - Stored XSS
keywords: Fluid Attacks, Security, Vulnerabilities, PHP Server Monitor
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                             |                                                        |
|-----------------------------|--------------------------------------------------------|
| **Name**                    | PHP Server Monitor v3.5.2 - Stored XSS                 |
| **Code name**               | [Gilmour](https://en.wikipedia.org/wiki/David_Gilmour) |
| **Product**                 | PHP Server Monitor                                     |
| **Affected versions**       | v3.5.2                                                 |
| **State**                   | Public                                                 |
| **Release date**            | 2022-03-07                                             |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting (XSS)                                |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)   |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:L/I:L/A:N                     |
| **CVSSv3 Base Score** | 4.8                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-23044](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23044)                                                 |

## Description

PHP Server Monitor v3.5.2 allows an authenticated admin user to
inject Javascript code inside the "ip" parameter while
adding a new website to monitor.

## Proof of Concept

Steps to reproduce

1. Go to the 'Servers' tab.
2. Click on 'Add new'.
3. Fill the 'Label' field.
4. Select 'Website' as the type.
5. Fill the 'Domain/IP' field using one of the following POCs.

    ```javascript
        https://www.example.com" onmouseover=alert(1)>
        https://www.example.com" style="display: block; position: fixed; top: 0; left: 0; z-index: 99999; width: 9999px; height: 9999px;" onmouseover=alert('XSS')> (To avoid user interaction)
    ```

6. The javascript code will be executed when a user
   visits the 'Servers' tab again.

System Information

* Version: PHP Server Monitor v3.5.2.
* Operating System: Linux.
* Web Server: Apache
* PHP Version: 7.4
* Database and version: Mysql

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

By 2022-03-07 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                 |
|---------------------|-----------------------------------------------------------------|
| **Vendor page**     | <https://www.phpservermonitor.org/>                             |
| **Issue**           | <https://github.com/phpservermon/phpservermon/issues/1178>      |

## Timeline

* 2022-01-11: Vulnerability discovered.

* 2022-01-11: Vendor contacted.

* 2022-01-17: Vendor replied acknowledging the report.

* 2022-03-07: Public Disclosure.