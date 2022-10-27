---
slug: advisories/jcole/
title: Local File Read in CandidATS 3.0.0 via XXE
authors: Carlos Bello
writer: cbello
codename: jcole
product: Local File Read in CandidATS 3.0.0 via XXE
date: 2022-10-27 12:00 COT
cveid: CVE-2022-42745
severity: 6.5
description: CandidATS 3.0.0      -     Local File Read via XXE
keywords: Fluid Attacks, Security, Vulnerabilities, Candid ATS, Local File Read, XXE
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Local File Read in CandidATS 3.0.0 via XXE                         |
| **Code name**         | [J.Cole](https://en.wikipedia.org/wiki/J._Cole)                    |
| **Product**           | CandidATS                                                          |
| **Affected versions** | Version 3.0.0                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-27                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | XML injection (XXE)                                                                                                         |
| **Rule**              | [083. XML injection (XXE)](https://docs.fluidattacks.com/criteria/vulnerabilities/083)                                      |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 6.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-42745](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42745)                                             |

## Description

CandidATS version 3.0.0 allows an external attacker to read
arbitrary files from the server. This is possible because the
application is vulnerable to XXE.

## Vulnerability

The XXE present in CandidATS 3.0.0, allows an unauthenticated
remote attacker to read arbitrary files from the server. To
trigger this vulnerability, we will need to upload a malicious
DOCX to the server.

## Exploitation

In this attack we will be able to read arbitrary files from the
server, through an XXE.

![LFR-viaXXE-candidats](https://user-images.githubusercontent.com/51862990/198341860-dc2b0ff1-3761-48b8-ba1d-ed87f3c99bdd.gif)

![exploit.png](https://user-images.githubusercontent.com/51862990/198341712-701500cc-270f-44ed-8f3c-0bfc11ce1238.png)

## Our security policy

We have reserved the CVE-2022-42745 to refer to these issues from now on.

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
  discovered="2022-10-11"
  contacted="2022-10-11"
  replied="2022-10-11"
  confirmed=""
  patched=""
  disclosure="2022-10-27">
</time-lapse>
