---
slug: advisories/avicii/
title: Zettlr 2.3.0  -  Local File Read
authors: Carlos Bello
writer: cbello
codename: avicii
product: Zettlr 2.3.0
date: 2022-09-26 15:30 COT
cveid: CVE-2022-40276
severity: 5.5
description: Zettlr 2.3.0  -  Local File Read - Insecure or unset HTTP headers
keywords: Fluid Attacks, Security, Vulnerabilities, Zettlr, HTTP
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | -------------------------------------------------------|
| **Name**              | Zettlr 2.3.0  -  Local File Read                       |
| **Code name**         | [Avicii](https://en.wikipedia.org/wiki/Avicii)         |
| **Product**           | Zettlr                                                 |
| **Affected versions** | Version 2.3.0                                          |
| **State**             | Public                                                 |
| **Release date**      | 2022-09-26                                             |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Insecure or unset HTTP headers - Content-Security-Policy                                                                    |
| **Rule**              | [043. Insecure or unset HTTP headers - Content-Security-Policy](https://docs.fluidattacks.com/criteria/vulnerabilities/043) |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 5.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-40276](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40276)                                             |

## Description

Zettlr version 2.3.0 allows an external attacker to remotely obtain
arbitrary local files on any client that attempts to view a malicious
markdown file through Zettlr. This is possible because the application
does not have a CSP policy (or at least not strict enough) and/or does
not properly validate the contents of markdown files before rendering
them.

## Vulnerability

This vulnerability occurs because the application does not have a CSP
policy (or at least not strict enough) and/or does not properly validate
the contents of markdown files before rendering them. Because of the above,
an attacker can embed malicious JS code in a markdown file and send it to
the victim to view and thus achieve an exfiltration of their local files.

More about this functionality here: https://docs.zettlr.com/en/core/print-preview/

## Exploitation

To exploit this vulnerability, you must send the following file to a
user to open with Zettlr. The exploit is triggered when the user
presses `CTRL+P` or simply clicks `print`.

### exploit.md

```markdown
<script>fetch("file:///etc/private").then(response => response.text()).then(leak => alert(leak))</script>
```

## Evidence of exploitation

![LocalFileRead](https://user-images.githubusercontent.com/51862990/189765853-1b6e5c13-5ec2-4062-8b35-c4a1c46cbc3a.gif)

## Our security policy

We have reserved the CVE-2022-40276 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Zettlr 2.3.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/Zettlr/Zettlr>

## Timeline

<time-lapse
  discovered="2022-09-07"
  contacted="2022-09-08"
  replied=""
  confirmed=""
  patched=""
  disclosure="2022-09-26">
</time-lapse>
