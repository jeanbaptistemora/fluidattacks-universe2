---
slug: advisories/dylan/
title: Exponent CMS 2.6.0 patch2 - Insecure file upload (RCE)
authors: Oscar Uribe
writer: ouribe
codename: dylan
product: Exponent CMS 2.6.0 patch2
date: 2022-01-24 12:00 COT
cveid: CVE-2022-23048
description: Exponent CMS 2.6.0 patch2 - Insecure file upload (RCE)
keywords: Fluid Attacks, Security, Vulnerabilities, Exponent CMS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                             |                                                          |
|-----------------------------|----------------------------------------------------------|
| **Name**                    | Exponent CMS 2.6.0 patch2 - Insecure file upload (RCE)   |
| **Code name**               | [Dylan](https://en.wikipedia.org/wiki/Bob_Dylan)         |
| **Product**                 | Exponent CMS                                             |
| **Affected versions**       | v2.6.0 patch2                                            |
| **State**                   | Public                                                   |
| **Release Date**            | 2022-02-03                                               |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | Insecure file upload (RCE)                                       |
| **Rule**              | [027. Insecure file upload](https://docs.fluidattacks.com/criteria/vulnerabilities/027)   |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H                     |
| **CVSSv3 Base Score** | 9.1                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | CVE-2022-23048                                                   |

## Description

Exponent CMS **2.6.0 patch2** allows an authenticated admin user to upload
a malicious extension in the format of a zip file with a php file inside it.
After upload it, the php file will be placed at `themes/simpletheme/{rce}.php`
from where can be access in order to execute commands..

## Proof of Concept

1. Click on the Exponent logo located on the upper left corner.
2. Go to 'Super-Admin Tools' > 'Extensions' > 'Install Extension'.
3. Click on 'Upload Extension'.
4. Create a malicious PHP file with the following PoC.

   ```php
   <?php echo system($_GET['cmd']); ?>
   ```

5. Zip the php file.
6. Upload the zip file.
7. Click on 'Upload Extension'
8. Next, click on 'Continue with Installation'.
9. Go to `http://127.0.0.1/exponentcms/themes/simpletheme/{rce}.php`
   in order to execute commands

System Information:

- Version: Exponent CMS 2.6.0 patch2.
- Operating System: Linux.
- Web Server: Apache
- PHP Version: 7.4
- Database and version: Mysql

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

By 2022-02-03 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://www.exponentcms.org/>                                      |
| **Ticket**          | <https://exponentcms.lighthouseapp.com/projects/61783/tickets/1460> |
| **Issue**           | <https://github.com/exponentcms/exponent-cms/issues/1546>           |

## Timeline

- 2022-01-24: Vulnerability discovered.

- 2022-01-24: Vendor contacted.

- 2022-02-03: Public Disclosure.
