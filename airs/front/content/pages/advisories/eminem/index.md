---
slug: advisories/eminem/
title: Browsershot 3.57.2 - Server Side XSS to LFR via URL
authors: Carlos Bello
writer: cbello
codename: eminem
product: Browsershot 3.57.2 - Server Side XSS to LFR via URL
date: 2022-10-28 18:30 COT
cveid: CVE-2022-41706
severity: 7.5
description: Browsershot 3.57.2 - Server Side XSS to LFR via URL
keywords: Fluid Attacks, Security, Vulnerabilities, Browsershot, Local File Read, XSS, LFR, PDF Generation
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------|
| **Name**              | Browsershot 3.57.2 - Server Side XSS to LFR via URL                                                                 |
| **Code name**         | [Eminem](https://en.wikipedia.org/wiki/Khalid_(singer))                                                             |
| **Product**           | Browsershot                                                                                                         |
| **Affected versions** | Version 3.57.2                                                                                                      |
| **State**             | Public                                                                                                              |
| **Release date**      | 2022-10-28                                                                                                          |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Server Side XSS                                                                                                             |
| **Rule**              | [425. Server Side XSS](https://docs.fluidattacks.com/criteria/vulnerabilities/425)                                          |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 7.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41706](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41706)                                             |

## Description

Browsershot version 3.57.2 allows an external attacker to remotely
obtain arbitrary local files. This is possible because the application
does not validate the URL protocol passed to the `Browsershot::url`
method.

## Vulnerability

This vulnerability occurs because the application does not validate the
URL protocol passed to the Browsershot::url method. Thanks to this, an
attacker can point to internal server files, which will be reflected in
the PDF that will be generated.

## Exploitation

![LFR-via-URL-PDF-Generation](https://user-images.githubusercontent.com/51862990/198747976-c28117a2-5fd3-4035-9275-54944ef51bd5.gif)

![exploit.png](https://user-images.githubusercontent.com/51862990/198747941-7059c7bf-d0ef-4258-8c02-61e3a02e790e.png)

## Our security policy

We have reserved the CVE-2022-41706 to refer to these issues from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Browsershot 3.57.2

* Operating System: GNU/Linux

## Mitigation

An updated version of Browsershot is available at the vendor page.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/spatie/browsershot>

**Release** <https://github.com/spatie/browsershot/releases/tag/3.57.3>

## Timeline

<time-lapse
  discovered="2022-10-25"
  contacted="2022-10-25"
  replied="2022-10-25"
  confirmed="2022-10-25"
  patched="2022-10-25"
  disclosure="2022-10-28">
</time-lapse>
