---
slug: advisories/modestep/
title: Multiple XSS in CandidATS leads to account takeover
authors: Carlos Bello
writer: cbello
codename: modestep
product: Multiple XSS in CandidATS leads to account takeover
date: 2022-10-26 14:30 COT
cveid: CVE-2022-42746,CVE-2022-42747,CVE-2022-42748,CVE-2022-42749
severity: 8.8
description: CandidATS 3.0.0      -     Multiple Cross-Site Scripting
keywords: Fluid Attacks, Security, Vulnerabilities, Candid ATS, Cross Site Scripting
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Multiple XSS in CandidATS leads to account takeover                |
| **Code name**         | [Modestep](https://en.wikipedia.org/wiki/Modestep)                 |
| **Product**           | CandidATS                                                          |
| **Affected versions** | Version 3.0.0                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-26                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Reflected cross-site scripting (XSS)                                                                                        |
| **Rule**              | [008. Reflected cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/008)                     |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 8.8                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-42746](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42746), [CVE-2022-42747](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42747), [CVE-2022-42748](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42748), [CVE-2022-42749](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42749)                                                                                                                                  |

## Description

CandidATS version 3.0.0 allows an external attacker to steal the
cookie of arbitrary users. This is possible because the application
application does not properly validate user input against XSS attacks.

## Vulnerability

The XSS present in CandidATS 3.0.0, allows an unauthenticated remote
attacker to perform an Account Takeover. To trigger this vulnerability,
we will need to send the following malicious link to an administrator
in order to hack their account:

* https://demo.candidats.net/ajax.php?f=getPipelineJobOrder&joborderID=50&page=0&entriesPerPage=15&sortBy=dateCreatedInt&sortDirection=desc&indexFile=index.php%27);%22%3E%3Cscript%3Ealert(document.cookie);%3C/script%3E%3C!--&isPopup=0

During the investigation, several parameters of the above URL were
found to be vulnerable to XSS:

1. indexFile      (CVE-2022-42746)

2. sortBy         (CVE-2022-42747)

3. sortDirection  (CVE-2022-42748)

4. page           (CVE-2022-42749)

Different CVE-IDs were reserved for these vulnerabilities because when
analyzing the source code, we realized that each of these flaws is fixed
independently.

## Exploitation

In this attack we will obtain the administrator user account, through
a malicious link:

![exploit](https://user-images.githubusercontent.com/51862990/198105518-9613a6db-ef9c-4fc9-acc3-2f81900b2770.png)

## Our security policy

We have reserved the CVE-2022-42746, CVE-2022-42747, CVE-2022-42748,
 CVE-2022-42749 to refer to these issues from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: CandidATS 3.0.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://candidats.net/>

## Timeline

<time-lapse
  discovered="2022-10-07"
  contacted="2022-10-07"
  replied="2022-10-07"
  confirmed=""
  patched=""
  disclosure="2022-10-26">
</time-lapse>
