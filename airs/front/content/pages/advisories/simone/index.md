---
slug: advisories/simone/
title: Zenario CMS 9.2 - Insecure file upload (RCE)
authors: Oscar Uribe
writer: ouribe
codename: simone
product: Zenario CMS 9.2
date: 2022-01-14 11:00 COT
cveid: CVE-2022-23043
description: Zenario CMS 9.2 - Insecure file upload (RCE)
keywords: Fluid Attacks, Security, Vulnerabilities, Zenario CMS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                             |                                                            |
|-----------------------------|------------------------------------------------------------|
| **Name**                    | Zenario CMS 9.2 - Insecure file upload (RCE)               |
| **Code name**               | [Simone](https://en.wikipedia.org/wiki/Nina_Simone)        |
| **Product**                 | Zenario CMS                                                |
| **Affected versions**       | 9.2                                                        |
| **Fixed versions**          | 9.2.55826                                                  |
| **State**                   | Public                                                     |
| **Release date**            | 2022-02-18                                                 |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | Insecure file upload (RCE)                                       |
| **Rule**              | [027. Insecure file upload](https://docs.fluidattacks.com/criteria/vulnerabilities/027)   |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H                     |
| **CVSSv3 Base Score** | 9.1                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-23043](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23043)                                                   |

## Description

Zenario CMS 9.2 allows an authenticated admin user to
bypass the file upload restriction by creating a new `File/MIME Types`
using the `.phar` extension. Then an attacker can upload a malicious
file, intercept the request and change the extension to `.phar` in order
to run commands on the server.

## Proof of Concept

Steps to reproduce

1. Once login as admin click on
   'Go to Organizer'> 'Configuration'.
2. Select 'File/MIME Types' in the 'Configuration' menu.
3. Click on 'Create'.
4. Create a new custom file type using 'phar' as extension
   and 'text/plain' as MIME Type and then click on 'Save'.

   The server validates some malicious extensions but still
   there are some valid executable extensions.
   For example 'phar' and 'shtml'.

5. Create a '.phar' file with the following content.

   ```php
   <?php echo system($_GET['cmd']); ?>
   ```

6. On the admin menu, click on 'Documents'
7. Click on 'Upload documents'
8. Click on 'Upload...' and browse the created file.
9. Select 'Public' and click on 'Save'.
10. Select the file and click on 'Actions' > 'View public link'
    in order to get the file location.
11. Go to the url in the browser.

System Information

* Version: Zenario CMS 9.2.
* Operating System: Linux.
* Web Server: Apache
* PHP Version: 7.4
* Database and version: Mysql

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

An updated version of Zenario CMS is available at the vendor page..

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                   |
|---------------------|-------------------------------------------------------------------|
| **Vendor page**     | <https://zenar.io/>                                               |
| **Patched version** | <https://github.com/TribalSystems/Zenario/releases/tag/9.2.55826> |

## Timeline

* 2022-01-13: Vulnerability discovered.

* 2022-01-13: Vendor contacted.

* 2022-01-14: Vendor replied acknowledging the report.

* 2022-02-08: Vulnerability patched.

* 2022-02-18: Public Disclosure.
