---
slug: advisories/malone/
title: Browsershot 3.57.3 - Server Side XSS to LFR via HTML
authors: Carlos Bello
writer: cbello
codename: malone
product: Browsershot 3.57.3 - Server Side XSS to LFR via HTML
date: 2022-11-18 13:00 COT
cveid: CVE-2022-43984
severity: 7.5
description: Browsershot 3.57.3 - Server Side XSS to LFR via HTML
keywords: Fluid Attacks, Security, Vulnerabilities, Browsershot, Local File Read, XSS, LFR, PDF Generation
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------|
| **Name**              | Browsershot 3.57.3 - Server Side XSS to LFR via HTML                                                                |
| **Code name**         | [Malone](https://en.wikipedia.org/wiki/Post_Malone)                                                                 |
| **Product**           | Browsershot                                                                                                         |
| **Affected versions** | Version 3.57.3                                                                                                      |
| **State**             | Public                                                                                                              |
| **Release date**      | 2022-11-18                                                                                                          |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Server Side XSS                                                                                                             |
| **Rule**              | [425. Server Side XSS](https://docs.fluidattacks.com/criteria/vulnerabilities/425)                                          |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 7.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-43984](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-43984)                                             |

## Description

Browsershot version 3.57.3 allows an external attacker to remotely
obtain arbitrary local files. This is possible because the application
does not validate that the JS content imported from an external source
passed to the `Browsershot::html` method does not contain URLs that use
the `file://` protocol.

## Vulnerability

This vulnerability occurs because the application does not validate that
the JS content imported from an external source passed to the
`Browsershot::html` method does not contain URLs that use the `file://`
protocol.

## Evidence of exploitation

![bypass-LFR-browsershot.gif](https://user-images.githubusercontent.com/51862990/199795560-24b3859a-ec1d-46ed-ac4d-3c8ca098527e.gif)

![bypass-LFR-browsershot.png](https://user-images.githubusercontent.com/51862990/199795469-e6db89bf-cf87-4cda-9082-4e4363753f06.png)

## Our security policy

We have reserved the CVE-2022-43984 to refer to these issues from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Browsershot 3.57.3

* Operating System: GNU/Linux

## Mitigation

An updated version of Browsershot is available at the vendor page.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/spatie/browsershot>

**Release** <https://github.com/spatie/browsershot/releases/tag/3.57.4>

## Timeline

<time-lapse
  discovered="2022-10-25"
  contacted="2022-10-25"
  replied="2022-10-25"
  confirmed="2022-10-25"
  patched=""
  disclosure="2022-11-18">
</time-lapse>
