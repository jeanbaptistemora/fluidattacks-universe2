---
slug: advisories/kiniza/
title: Frappe 14.10.0 - Local File Read
authors: Carlos Bello
writer: cbello
codename: kiniza
product: Frappe 14.10.0 - LFR
date: 2022-11-21 12:00 COT
cveid: CVE-2022-41712
severity: 4.3
description: Frappe 14.10.0       -       Local File Read (LFR)
keywords: Fluid Attacks, Security, Vulnerabilities, Frappe, LFR
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Frappe 14.10.0 - LFR                                               |
| **Code name**         | [Kiniza](https://en.wikipedia.org/wiki/Nebu_Kiniza)                |
| **Product**           | Frappe                                                             |
| **Affected versions** | Version 14.10.0                                                    |
| **State**             | Public                                                             |
| **Release date**      | 2022-11-21                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Lack of data validation - Path Traversal                                                                                    |
| **Rule**              | [063. Lack of data validation - Path Traversal](https://docs.fluidattacks.com/criteria/vulnerabilities/063)                 |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 4.3                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41712](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41712)                                             |

## Description

Frappe version 14.10.0 allows an external attacker to remotely obtain
arbitrary local files. This is possible because the application does
not correctly validate the information injected by the user in the
`import_file` parameter.

## Vulnerability

This vulnerability occurs because the application does not correctly
validate the path of the `import_file` parameter. Thanks to this, an
attacker can point to internal server files.

## Evidence of exploitation

![LFR-Frappe.png](https://user-images.githubusercontent.com/51862990/199772519-336d79be-ee93-4fa6-a2d0-3deebb1dc395.png)

![LFR-Frappe.gif](https://user-images.githubusercontent.com/51862990/199772736-8572e8d4-2c06-46d8-a401-d7bdfb8f3439.gif)

## Our security policy

We have reserved the CVE-2022-41712 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Frappe 14.10.0

* Operating System: GNU/Linux

## Mitigation

An updated version of Badaso is available at the vendor page.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/frappe/frappe>

## Timeline

<time-lapse
  discovered="2022-10-10"
  contacted="2022-10-10"
  replied="2022-10-10"
  confirmed="2022-10-11"
  patched="2022-10-12"
  disclosure="2022-11-21">
</time-lapse>
