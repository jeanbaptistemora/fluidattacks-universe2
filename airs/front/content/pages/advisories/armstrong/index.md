---
slug: advisories/armstrong/
title: PeTeReport 0.5 - Stored XSS (Markdown)
authors: Oscar Uribe
writer: ouribe
codename: armstrong
product: PeTeReport 0.5
date: 2022-02-18 10:00 COT
cveid: CVE-2022-25220
description: PeTeReport 0.5 - Stored XSS (Markdown)
keywords: Fluid Attacks, Security, Vulnerabilities, PeTeReport
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                            |
|-------------------------|------------------------------------------------------------|
| **Name**                | PeTeReport 0.5 - Stored XSS (Markdown)                     |
| **Code name**           | [Armstrong](https://en.wikipedia.org/wiki/Louis_Armstrong) |
| **Product**             | PeTeReport                                                 |
| **Affected versions**   | Version 0.5                                                |
| **Fixed versions**      | Version 0.7                                                |
| **State**               | Public                                                     |
| **Release date**        | 2022-02-23                                                 |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting (XSS)                                |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)    |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:L/I:L/A:N                     |
| **CVSSv3 Base Score** | 4.8                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-25220](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25220)                                                     |

## Description

PeteReport **Version 0.5** allows an authenticated admin user
to inject persistent javascript code inside the markdown descriptions
while creating a product, report or finding.

## Proof of Concept

Steps to reproduce

1. Click on 'Add Product'.
2. Insert the following PoC inside the product description.

   ```javascript
      [XSS](javascript:alert(1))
   ```

3. Click on 'Save Product'.
4. If a user visits the product and click on the link in
   the description the javascript code will be rendered.

System Information

* Version: PeteReport Version 0.5.
* Operating System: Docker.
* Web Server: nginx.

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

An updated version of PeteReport is available at the vendor page.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://github.com/1modm/petereport>                               |
| **Issue**           | <https://github.com/1modm/petereport/issues/35>                     |

## Timeline

* 2022-02-08: Vulnerability discovered.

* 2022-02-08: Vendor contacted.

* 2022-02-09: Vendor replied acknowledging the report.

* 2022-02-09: Vulnerability patched.

* 2022-02-23: Public Disclosure.
