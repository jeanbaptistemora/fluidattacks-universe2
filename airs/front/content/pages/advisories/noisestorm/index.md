---
slug: advisories/noisestorm/
title: Markdownify 1.4.1 - Local File Read
authors: Carlos Bello
writer: cbello
codename: noisestorm
product: Markdownify 1.4.1 - Local File Read
date: 2022-10-18 19:00 COT
cveid: CVE-2022-41710
severity: 5.5
description: Markdownify 1.4.1        -         Local File Read
keywords: Fluid Attacks, Security, Vulnerabilities, Markdownify, LFR
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Markdownify 1.4.1 - Local File Read                                |
| **Code name**         | [Noisestorm](https://en.wikipedia.org/wiki/Noisestorm)             |
| **Product**           | Badaso                                                             |
| **Affected versions** | Version 1.4.1                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-18                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Insecure or unset HTTP headers - Content-Security-Policy                                                                                                                               |
| **Rule**              | [043. Insecure or unset HTTP headers - Content-Security-Policy](https://docs.fluidattacks.com/criteria/vulnerabilities/043)                                                                                                                                                  |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 5.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41710](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41710)                                             |

## Description

Markdownify version 1.4.1 allows an external attacker to remotely
obtain arbitrary local files on any client that attempts to view a
malicious markdown file through Markdownify. This is possible because
the application does not have a CSP policy (or at least not strict enough)
and/or does not properly validate the contents of markdown files before
rendering them.

## Vulnerability

This vulnerability occurs because the application does not have a CSP
policy (or at least not strict enough) and/or does not properly validate
the contents of markdown files before rendering them.  Because of the
above, an attacker can embed malicious JS code in a markdown file and
send it to the victim to view and thus achieve an exfiltration of their
local files.

## Exploitation

To exploit this vulnerability, you must send the following file to a user
to open with Markdownify.

### exploit.md

```php
<img src="1" onerror='fetch("file:///etc/private").then(data => data.text()).then(leak => alert(leak));'/>
```

## Evidence of exploitation

![LFR-Markdownify](https://user-images.githubusercontent.com/51862990/196567814-83f3f413-a16c-4993-8157-ab44906c86d3.gif)

## Our security policy

We have reserved the CVE-2022-41710 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Markdownify 1.4.1

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/amitmerchant1990/electron-markdownify>

## Timeline

<time-lapse
  discovered="2022-09-28"
  contacted="2022-09-28"
  replied="2022-09-28"
  confirmed=""
  patched=""
  disclosure="2022-10-18">
</time-lapse>
