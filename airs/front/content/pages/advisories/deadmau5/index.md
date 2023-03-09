---
slug: advisories/deadmau5/
title: Gridea 0.9.3  -  Local File Read
authors: Carlos Bello
writer: cbello
codename: deadmau5
product: Gridea 0.9.3
date: 2022-09-26 15:00 COT
cveid: CVE-2022-40275
severity: 5.5
description: Gridea 0.9.3  -  Local File Read - Insecure or unset HTTP headers
keywords: Fluid Attacks, Security, Vulnerabilities, Gridea, HTTP
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | -------------------------------------------------------|
| **Name**              | Gridea 0.9.3  -  Local File Read                       |
| **Code name**         | [Deadmau5](https://en.wikipedia.org/wiki/Deadmau5)     |
| **Product**           | Gridea                                                 |
| **Affected versions** | Version 0.9.3                                          |
| **State**             | Public                                                 |
| **Release date**      | 2022-09-26                                             |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Insecure or unset HTTP headers - Content-Security-Policy                                                                    |
| **Rule**              | [043. Insecure or unset HTTP headers - Content-Security-Policy](https://docs.fluidattacks.com/criteria/vulnerabilities/043) |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 5.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-40275](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40275)                                             |

## Description

Gridea version 0.9.3 allows an external attacker to remotely obtain
arbitrary local files on any client that attempts to view a malicious
markdown file through Gridea. This is possible because the application
does not have a CSP policy (or at least not strict enough) and/or does
not properly validate the contents of markdown files before rendering
them.

## Vulnerability

This vulnerability occurs because the application does not have a CSP policy
(or at least not strict enough) and/or does not properly validate the contents
of markdown files before rendering them.  Because of the above, an attacker can
embed malicious JS code in a markdown file and send it to the victim to view and
thus achieve an exfiltration of their local files.

## Exploitation

To exploit this vulnerability, you must send the following file to a user to open
with Gridea. The exploit is triggered when the user presses `CTRL+P` or simply
clicks `preview`.

### exploit.md

```markdown
<img src="1" onerror='fetch("file:///etc/private").then(data => data.text()).then(leak => alert(leak));'/>
```

## Our security policy

We have reserved the CVE-2022-40275 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Gridea 0.9.3

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/getgridea/gridea>

## Timeline

<time-lapse
  discovered="2022-09-05"
  contacted="2022-09-05"
  replied=""
  confirmed=""
  patched=""
  disclosure="2022-09-26">
</time-lapse>
