---
slug: vulnerable-google-chrome/
title: A Highly Vulnerable Google Chrome?
date: 2022-04-20
subtitle: Three strikes already for this web browser in 2022
category: attacks
tags: cybersecurity, vulnerability, risk, software, exploit, web
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1650483635/blog/vulnerable-google-chrome/cover_vulnerable_google_chrome.webp
alt: Photo by Chris Briggs on Unsplash
description: In this blog post, you can learn about three zero-day vulnerabilities of at least high severity in Google Chrome that have been exploited this year.
keywords: Chrome, Google, Zero Day, Vulnerability, Exploit, Web, Browser, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/x9TCnxNBofE
---

Are you sure
you're using the latest version of Google Chrome?
Make sure you are.
So far this year,
Chrome has received three strikes.
Cybercriminals have exploited *at least* three zero-day vulnerabilities
in this famed web browser.

## First strike: CVE-2022-0609

Barely [beginning this year](https://www.zdnet.com/article/google-we-stopped-these-hackers-who-were-targeting-job-hunters-and-crypto-firms/),
a couple of North Korean hacking groups
were already exploiting a Google Chrome zero-day vulnerability.
A little over a month later,
on [February 10](https://chromereleases.googleblog.com/2022/02/stable-channel-update-for-desktop_14.html),
Google's Threat Analysis Group (TAG) discovered it
and, within days,
managed to patch this high-severity bug:
[CVE-2022-0609](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0609).
(CVSS 3.1 base score: [8.8](https://nvd.nist.gov/vuln/detail/CVE-2022-0609).)
Apparently,
the cybercriminals were associated
with the notorious and powerful North Korean [criminal gang Lazarus](../lazarus-malware-cyberattack/).
As [reported by the researchers](https://blog.google/threat-analysis-group/countering-threats-north-korea/),
these attackers used the same exploit kit,
since they had a shared supply chain,
but with different targets and techniques.

One group
(its activity is tracked as [Operation Dream Job](https://www.clearskysec.com/operation-dream-job/))
targeted about ten news media and IT companies.
Approximately 250 people from these firms received emails
with sham job opportunities
sent from Oracle, Google and Disney.
These emails contained links
[spoofing](../spoofing/) genuine recruiting websites.
Once the person clicked on it,
they received a hidden [iframe](https://www.techtarget.com/whatis/definition/IFrame-Inline-Frame)
that activated the exploit kit.
The other group
(its activity is tracked as [Operation AppleJeus](https://securelist.com/operation-applejeus/87553/))
targeted more than 85 users
in cryptocurrency and fintech companies.
According to [the late March report](https://blog.google/threat-analysis-group/countering-threats-north-korea/),
at least two websites were compromised,
hosting hidden iframes
to deliver the exploit kit to visitors.
There were also fake websites
directing visitors to the same kit.

This exploit kit served a highly [obfuscated](https://en.wikipedia.org/wiki/Obfuscation_(software))
JavaScript
to fingerprint the victim's system.
It then collected data
such as user-agent and resolution
and sent it to the exploit server.
If a certain number of unknown requirements were met,
the user received a Chrome remote code execution ([RCE](https://docs.fluidattacks.com/criteria/vulnerabilities/004/))
exploit
along with additional JavaScript.
Then,
if the RCE was successful,
the JavaScript requested a new phase called SBX,
an acronym for Sandbox Escape.
In these cases,
the ["attacker can execute](https://medium.com/ssd-secure-disclosure/ios-vulnerabilities-3-sandbox-escape-cves-5233c92ad875)
malicious code
from a sandbox outside of an environment,
forcing the device to run the code within it."

In response to this first strike,
Google updated its Stable channel to 98.0.4758.102
for Windows, Mac and Linux.
Additionally,
they included all identified websites and domains
in their free [Safe Browsing](https://safebrowsing.google.com/) service
["to protect users](https://blog.google/threat-analysis-group/countering-threats-north-korea/)
from further exploitation."

## Second strike: CVE-2022-1096

The news of the previous strike was still fresh
when Google [reported](https://chromereleases.googleblog.com/2022/03/stable-channel-update-for-desktop_25.html)
an urgent update
due to a second zero-day vulnerability in Chrome.
They were informed by an anonymous party about this bug
([CVE-2022-1096](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1096))
on March 23.
In the release update,
only about two days later,
they admitted being aware of the existence of an exploit in the wild
(i.e., widely published)
for this "high" severity vulnerability.
(There's yet no official CVSS score for this vulnerability.)
But additional information was kept by them to a minimum.
At this time,
unlike in the previous case,
there is no dedicated post on Google's TAG's [official blog](https://blog.google/threat-analysis-group/).
As they pointed out,
["Access to bug](https://chromereleases.googleblog.com/2022/03/stable-channel-update-for-desktop_25.html)
details and links may be kept restricted
until a majority of users are updated with a fix."

Based on their report
and [what we've seen](https://therecord.media/google-releases-emergency-security-update-for-chrome-users-after-second-0-day-of-2022-discovered/)
[on the web](https://threatpost.com/google-chrome-bug-actively-exploited-zero-day/179161/),
we know this is a type-confusion vulnerability
in the Chrome [V8](https://v8.dev/) JavaScript and WebAssembly engine.
In this bug,
pieces of software code in the middle of data execution operations
do not verify the types of inputs they receive
and may incorrectly process them as other types.
Threat actors can take advantage
of the software's subsequent logical errors
to execute malicious code on victims' systems.

The affected engine, V8,
is an open-source component
for processing JavaScript and WebAssembly code
that Chrome and Chromium-based web browsers use.
[The latter include](https://www.zdnet.com/pictures/all-the-chromium-based-browsers/5/),
for example,
Microsoft Edge, Samsung Internet, Opera and Vivaldi.
([Microsoft also informed](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-1096)
its users
about this vulnerability
and the new version of Edge promptly).
So here we prefer to extend our initial warning:
Make sure you have any of your web browsers up to date.
It's worth noting that
[16 zero-day vulnerabilities](https://www.cybersecurity-help.cz/blog/2471.html)
were detected in Chrome in 2021.
Eight of these were also present in V8.
And [three of them](https://threatpost.com/google-chrome-bug-actively-exploited-zero-day/179161/),
like the one described in this segment,
were type-confusion vulnerabilities:
[CVE-2021-21224](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-21224),
[CVE-2021-30551](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-30551)
and [CVE-2021-30563](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-30563).

In response to this second strike,
Google updated its Stable channel to 99.0.4844.84
for Windows, Mac and Linux.

## Third strike: CVE-2022-1364

[April](https://www.zdnet.com/article/google-fixes-chrome-zero-day-being-used-in-exploits-in-the-wild/)
brought more confusion.
On the 13th,
[Google's TAG reported](https://chromereleases.googleblog.com/2022/04/stable-channel-update-for-desktop_14.html)
another "high" severity type-confusion vulnerability
in V8: [CVE-2022-1346](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1364).
(There's yet no official CVSS score for this vulnerability either.)
The patch was available
for all [3.2 billion Chrome users](https://www.forbes.com/sites/daveywinder/2022/04/17/emergency-security-update-for-32-billion-google-chrome-users-attacks-underway/)
the next day.
However,
Google again warned about the exploit's existence in the wild.
Was this another hacking onslaught orchestrated by North Koreans?
As in the previous case,
we have to wait for a majority of users
to update the web browser
to get more details about this vulnerability.

In response to this third strike,
Google updated its Stable channel to **100.0.4896.127**
for Windows, Mac and Linux.
(Read about Microsoft Edge's new version [here](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-1364).)
If you want to check that your Chrome is updated,
open a new browser window
and go to the top right corner.
Click on the three dots to open the drop-down menu
and select the Settings option.
Then,
click the About Chrome option
at the bottom of the menu on the left.
Verify that you see the message "Chrome is up to date"
and that the version number matches the one we give you here.

<div class="imgblock">

![Settings - About Chrome](https://res.cloudinary.com/fluid-attacks/image/upload/v1650481065/blog/vulnerable-google-chrome/about_chrome_settings.webp)

</div>

Already three strikes were received by Google Chrome in 2022.
Could we now determine a strikeout?
Not in this game.
It's enough to look back at the history of this software
to say that they are likely to receive more strikes this year.
Maybe this latest version we presented you here
will be obsolete in a few days.
So stay tuned for updates!

At `Fluid Attacks`,
we are on the lookout for these and many,
many other security vulnerabilities
that may affect our clients.
Thanks to our [Continuous Hacking](../../services/continuous-hacking/)
service,
with our [highly certified](../../about-us/certifications/)
[red team](../../solutions/red-teaming/),
you can prevent your organization
from receiving highly harmful impacts from cyberattacks.
For more information,
do not hesitate to [contact us](../../contact-us/).
