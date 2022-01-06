---
slug: advisories/hendrix/
title: PartKeepr v1.4.0 url attachment 'add parts' - LFI
authors: Oscar Uribe
writer: ouribe
codename: hendrix
product: PartKeepr v1.4.0
date: 2022-01-04 14:00 COT
cveid: CVE-2022-22701
description: PartKeepr v1.4.0 url attachment 'add parts' - LFI
keywords: Fluid Attacks, Security, Vulnerabilities, PartKeepr
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                    |                                                      |
|--------------------|------------------------------------------------------|
| **Name**           | PartKeepr v1.4.0 url attachment 'add parts' - LFI    |
| **Code name**      | [Hendrix](https://en.wikipedia.org/wiki/Jimi_Hendrix)|
| **Product**        | PartKeepr                                            |
| **Versions**       | v1.4.0                                               |
| **State**          | Unpublished/Contacted Vendor                         |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | Local file inclusion                                             |
| **Rule**              | [123. Local file inclusion](https://docs.fluidattacks.com/criteria/vulnerabilities/123)   |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N                     |
| **CVSSv3 Base Score** | 6.5                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-22701](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-22701)                   |

## Description

In PartKeepr before v1.4.0, the functionality to load attachments using
a URL while creating a part, allows the use of the 'file://' URI scheme,
allowing an authenticated user to read local files.

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

By 2022-01-04 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                 |
|---------------------|-----------------------------------------------------------------|
| **Vendor page**     | <https://partkeepr.org/>                               |

## Timeline

- 2022-01-03: Vulnerability discovered.

- 2022-01-04: Vendor contacted.
