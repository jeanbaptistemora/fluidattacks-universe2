---
slug: advisories/cerati/
title: ManageEngine AppManager15 (Build No:15510) - DLL Hijacking
authors: Andres Roldan & Oscar Uribe
writer: ouribe
codename: cerati
product: ManageEngine AppManager15
date: 2022-02-09 12:00 COT
cveid: CVE-2022-23050
severity: 9.1
description: ManageEngine AppManager15 (Build No:15510) - DLL Hijacking
keywords: Fluid Attacks, Security, Vulnerabilities, ManageEngine, AppManager
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                            |
|-------------------------|------------------------------------------------------------|
| **Name**                | ManageEngine AppManager15 (Build No:15510) - DLL Hijacking |
| **Code name**           | [Cerati](https://en.wikipedia.org/wiki/Gustavo_Cerati)     |
| **Product**             | ManageEngine                                               |
| **Affected versions**   | AppManager15 (Build No:15510)                              |
| **Fixed versions**      | AppManager15 (Build No:15520)                              |
| **State**               | Public                                                     |

## Vulnerability

|                       |                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------- |
| **Kind**              | DLL Hijacking                                                                                           |
| **Rule**              | [413. Insecure file upload - DLL Injection](https://docs.fluidattacks.com/criteria/vulnerabilities/413) |
| **Remote**            | Yes                                                                                                     |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H                                                            |
| **CVSSv3 Base Score** | 9.1                                                                                                     |
| **Exploit available** | No                                                                                                      |
| **CVE ID(s)**         | [CVE-2022-23050](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23050)                         |

## Description

ManageEngine AppManager15 `(Build No:15510)` allows an
authenticated admin user to upload a DLL file to perform
a DLL hijack attack inside the `working` folder through
the `Upload Files / Binaries` functionality.

## Proof of Concept

### Steps to reproduce

1. Log in as an admin user.
2. Go to `Settings`.
3. Go to the `Tools` section and click on `Upload Files / Binaries`.
4. Select the `Upload Script to <Product_Home>/working/` option.
5. Create a malicious DLL with one of the following names

    ```
    MSASN1.dll
    WTSAPI32.dll
    CRYPTSP.dll
    CRYPTBASE.dll
    ```

6. Upload the file.
7. Go to `Shutdown / Restart Service` and click on `Restart`
8. Wait for the service to restart in order to load the DLL file.

### System Information

* Version: ManageEngine AppManager15 (Build No:15510).
* Operating System: Windows 10.0.19042 N/A Build 19042.

## Exploit

There is no exploit for the vulnerability but can be manually exploited.

## Mitigation

An updated version of ManageEngine is available at the vendor page.

## Credits

The vulnerability was discovered by [Andrés
Roldán](https://www.linkedin.com/in/andres-roldan/) and [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                                 |
|---------------------|---------------------------------------------------------------------------------|
| **Vendor page**     | <https://www.manageengine.com/>                                                 |
| **Release notes**   | <https://www.manageengine.com/products/applications_manager/release-notes.html> |
| **Latest version** | <https://www.manageengine.com/products/applications_manager/download.html> |

## Timeline

<time-lapse
  discovered="2022-02-03"
  contacted="2022-02-03"
  replied="2022-02-04"
  confirmed="2022-02-08"
  patched="2022-05-19"
  disclosure="2022-05-20">
</time-lapse>
