---
slug: advisories/avicii/
title: Zettlr 2.3.0  -  Local File Read
authors: Carlos Bello
writer: cbello
codename: avicii
product: Zettlr 2.3.0
date: 2022-09-12 20:30 COT
cveid: CVE-2022-40276
severity: 6.5
description: Zettlr 2.3.0  -  Local File Read
keywords: Fluid Attacks, Security, Vulnerabilities, Zettlr
banner: advisories-bg
advise: no
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | -------------------------------------------------------|
| **Name**              | Zettlr 2.3.0  -  Local File Read                       |
| **Code name**         | [Avicii](https://en.wikipedia.org/wiki/Avicii)         |
| **Product**           | Gridea                                                 |
| **Affected versions** | Version 2.3.0                                          |
| **State**             | Private                                                |
| **Release date**      | 2022-09-12                                             |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| **Kind**              | Lack of data validation - URL                                                                          |
| **Rule**              | [141. Lack of data validation - URL](https://docs.fluidattacks.com/criteria/vulnerabilities/141)       |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N                                                           |
| **CVSSv3 Base Score** | 6.5                                                                                                    |
| **Exploit available** | Yes                                                                                                    |
| **CVE ID(s)**         | [CVE-2022-40276](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40276)                        |

## Description

Zettlr version 2.3.0 allows an external attacker to read arbitrary
local files remotely on any client that attempts to print a malicious
file, via Zettlr. This is possible because the application does not
properly validate the content of the files before launching the
"preview" of the file in HTML format.

## Vulnerability

This vulnerability occurs due to lack of validation in the content
of the files that you want to print from zettlr. When we want to
print a document, a "preview" of the document is opened. At this
moment any JS code present in any type of file accepted by the
application is executed. The reason why the XSS payload is executed
for any type of file is that the preview generates an HTML version
of the file in question. This is why in the end it doesn't matter
what type of file we deliver to the user.

More about this functionality here: https://docs.zettlr.com/en/core/print-preview/

## Exploitation

To exploit this vulnerability, you must send the following file to a
user to open with Zettlr. The exploit is triggered when the user
presses "CTRL+P" or simply clicks "print".

### exploit.md

```markdown
<script>fetch("file:///etc/private").then(response => response.text()).then(leak => alert(leak))</script>
```

## Evidence of exploitation

![LocalFileRead](https://user-images.githubusercontent.com/51862990/189765853-1b6e5c13-5ec2-4062-8b35-c4a1c46cbc3a.gif)

## Our security police

We have reserved the CVE-2022-40276 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Zettlr 2.3.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from the Offensive
Team of `Fluid Attacks`.

## References

**Vendor page** <https://github.com/getgridea/gridea>

## Timeline

<time-lapse
  discovered="2022-09-07"
  contacted="2022-09-08"
  replied=""
  confirmed="2022-09-00"
  patched=""
  disclosure="2022-09-00">
</time-lapse>
