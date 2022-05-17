---
slug: advisories/bowie/
title: Popcorn Time 0.4.7 - XSS to RCE
authors: Oscar Uribe
writer: ouribe
codename: bowie
product: Popcorn Time 0.4.7
date: 2022-04-28 10:00 COT
cveid: CVE-2022-25229
severity: 7.7
description: Popcorn Time 0.4.7 (Just Keep Swimming) - XSS to RCE
keywords: Fluid Attacks, Security, Vulnerabilities, Popcorn, XSS, RCE
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                            |
|-------------------------|------------------------------------------------------------|
| **Name**                | Popcorn Time 0.4.7 - XSS to RCE                            |
| **Code name**           | [Bowie](https://en.wikipedia.org/wiki/David_Bowie)         |
| **Product**             | Popcorn Time                                               |
| **Affected versions**   | Version 0.4.7 (Just Keep Swimming)                         |
| **State**               | Public                                                     |
| **Release date**        | 2022-05-17                                                 |

## Vulnerability

|                       |                                                                                    |
|-----------------------|------------------------------------------------------------------------------------|
| **Kind**              | XSS to RCE                                                                         |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)   |
| **Remote**            | No                                                                                |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N                                       |
| **CVSSv3 Base Score** | 7.7                                                                                |
| **Exploit available** | No                                                                                 |
| **CVE ID(s)**         | [CVE-2022-25229](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25229)                                                    |

## Description

Popcorn Time 0.4.7 has a Stored XSS in the `Movies API Server(s)`
field via the `settings` page. The `nodeIntegration` configuration
is set to **on** which allows the webpage to use `NodeJs` features,
an attacker can leverage this to run OS commands.

## Proof of Concept

### Steps to reproduce

1. Open the Popcorn time application.

2. Go to `settings`.

3. Enable `Show advanced settings`.

4. Scroll down to the `API Server(s)` section.

5. Insert the following PoC inside the `Movies API Server(s)`
   field and click on `Check for updates`.

```javascript
a"><script>require('child_process').exec('calc');</script>
```

6. Scroll down to the `Database` section and click on
   `Export database`.

7. The application will create a `.zip` file with
   the current configuration.

8. Send the configuration to the victim.

9. The victim must go to `Settings -> Database`
   and click on `Import Database`

10. When the victim restarts the application the XSS
    will be triggered and will run the `calc` command.

### System Information

* Version: Popcorn Time 0.4.7.
* Operating System: Windows 10.0.19042 N/A Build 19042.
* Installer: Popcorn-Time-0.4.7-win64-Setup.exe

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

An updated version of PopcornTime is available at the vendor page.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://github.com/popcorn-official/popcorn-desktop>               |
| **Issue**           | <https://github.com/popcorn-official/popcorn-desktop/issues/2491>   |

## Timeline

* 2022-04-26: Vulnerability discovered.

* 2022-04-26: Vendor contacted.

* 2022-05-04: Vendor confirmed the vulnerability.

* 2022-05-07: Vulnerability patched.

* 2022-05-17: Public disclosure.