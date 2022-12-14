---
slug: advisories/oliver/
title: pyhtml2pdf 0.0.6 - Local File Read via Server Side XSS
authors: Carlos Bello
writer: cbello
codename: oliver
product: pyhtml2pdf 0.0.6 - Local File Read
date: 2022-12-14 14:30 COT
cveid: CVE-2022-4500
severity: 7.5
description: pyhtml2pdf 0.0.6 - Local File Read via Server Side XSS
keywords: Fluid Attacks, Security, Vulnerabilities, Server Side XSS, LFR
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | pyhtml2pdf 0.0.6 - Local File Read                                 |
| **Code name**         | [Oliver](https://en.wikipedia.org/wiki/Oliver_(DJs))               |
| **Product**           | Pyhtml2pdf                                                         |
| **Affected versions** | Version 0.0.6                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-12-14                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Server Side XSS                                                                                                             |
| **Rule**              | [425. Server Side XSS](https://docs.fluidattacks.com/criteria/vulnerabilities/425)                                          |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N                                                                               |
| **CVSSv3 Base Score** | 7.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-4500](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-4500)                                               |

## Description

Pyhtml2pdf version 0.0.6  allows an external attacker to remotely obtain
arbitrary local files. This is possible because the application does not
validate the HTML content entered by the user.

## Vulnerability

This vulnerability occurs because the application does not validate that
the HTML content entered by the user is not malicious.

## Exploitation

To exploit this vulnerability, we only need to send the following malicious
HTML to pyhtml2pdf:

### Exploit.html

```html
<iframe width="10000px" height="10000px" src=file:///etc/passwd></iframe>
```

Thus, when pyhtml2pdf parses the malicious HTML, it will return the local file
specified in the generated PDF.

## Evidence of exploitation

![LFR-pyhtml2pdf](https://user-images.githubusercontent.com/51862990/207685111-b06bdf8e-8361-44de-97e8-0d44c3728dec.gif)

![LFR-pyhtml2pdf](https://user-images.githubusercontent.com/51862990/207685156-fe89fb54-5cbc-4636-90a8-8b2d621e5927.png)

## Our security policy

We have reserved the ID CVE-2022-4500 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Pyhtml2pdf 0.0.6

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://pypi.org/project/pyhtml2pdf/>

## Timeline

<time-lapse
  discovered="2022-12-14"
  contacted="2022-12-14"
  replied="2022-12-14"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
