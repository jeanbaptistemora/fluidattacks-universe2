---
slug: osce-journey/
title: A Journey to OSCE
date: 2020-08-10
category: attacks
subtitle: A personal OSCE experience
tags: osce, training, exploit
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330965/blog/osce-journey/cover_swxqa7.webp
alt: Photo by Joshua Earle on Unsplash
description: This post will describe the journey that I took to earn
  the OSCE certification.
keywords: Business, Information, Security, Protection, Hacking,
  Vulnerability, Exploit, OSCE
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCE, OSCP, CHFI
about2: '"We don''t need the key, we''ll break in" RATM'
source: https://unsplash.com/photos/9idqIGrLuTE
---

Several days ago, I took the `OSCE` exam and passed. It was the first
time I tried it, and I completed all the tasks in 11 hours.

In this article, I’ll describe my experience and the methodology that I
used, which finally led me to achieve the `OSCE` certification.

## Background

To start, I think it’s fair to mention a little about my experience. I
began to get into the hacking and security world during my college time,
a good 20+ years ago.

The first article I read on exploitation was Aleph One’s mythical
**Smashing The Stack For Fun And Profit**. It was around 1999 and by
that time I knew nothing about computers. The introduction of that
article mentioned unknown things like **Linux**, **C**, **Stack**, etc.,
and it was the first trigger for me to get deep into the security world.
As you may guess, it took me several years to fully understand that
article, but I learned a **LOT** during the process. In fact, I wrote
several tools at that time to debug and reverse `ELF` files.

I also started making contributions to the Debian project in 2003,
maintaining a core package for Linux at that time:
[LILO](https://salsa.debian.org/joowie-guest/maintain_lilo/-/blob/master/debian/changelog)
(the ancestor of Grub). With that, I became an official Debian
maintainer and still hold that position (aroldan \<at\> debian.org). I
was very active from 2003 to 2013, making contributions to the Debian
project, maintaining packages like
[Prelink](https://people.redhat.com/jakub/prelink/) and
[Valgrind](https://www.valgrind.org/), whose manpage I initially
[wrote](https://linux.die.net/man/1/valgrind) (you can see my email in
the credits at the end). I also made the first Debian package for
[Hydra](https://metadata.ftp-master.debian.org/changelogs//main/h/hydra/hydra_9.1-1_changelog)
and packaged [ERESI](https://github.com/thorkill/eresi).

I’ve also been working full time in security-related tasks for over 18
years, mostly focused on offensive security.

I’ve earned the `CEH` certification several times; the last one expired
in 2012. The same year, I took the PWK course (although at that time
Kali was known as Backtrack) and earned the `OSCP` certification.

The `OSCE` was the next step.

## CTP course

In May 2020, during the `COVID-19` pandemic, I started the Cracking The
Perimeter (`CTP`) course. You can see the public course syllabus
[here](https://www.offensive-security.com/documentation/cracking-the-perimeter-syllabus.pdf).
I made no previous special preparation for the course, other than my
work experience.

The course modules are very well structured. Mati’s clear explanations
of each technical detail show his mastery of the topic.

While you’re in the course, you have one month of access to an Offsec
lab to follow the modules' content.

The way I approached the course was to watch the videos following the
written material. Then, at the end of each module, I replicated the
whole exercise from scratch without peeping the course material and
tried to come up with the same result. Also, I developed and solved the
extra mile exercises.

It took me around one and a half weeks to complete the course. However,
I wanted to understand and replicate the vulnerabilities presented on
the modules, all by myself. I re-did all the course modules from scratch
in the remaining lab time at least three times. Every failure in getting
the module objectives was an opportunity to learn new things.

When the lab time was about to expire, I was able to set up my own test
lab. It consisted of Windows XP SP3 and Windows Vista Business machines.

## Self-study

My lab time was scheduled to end on the 8th of June, and the `OSCE` exam
was scheduled for the 13th of July.

During that month, I needed to practice what was learned during the
course. So I used the following to sharpen the skills:

- In my local lab, I ran
  [Vulnserver](https://github.com/stephenbradshaw/vulnserver). It’s a
  `TCP` server with several mock commands, some of them vulnerable on
  purpose, and each vulnerability has its quirk. To be able to fully
  understand the exploitation process of each affected command, I
  produced a series of articles:

    - [TRUN command exploitation](../vulnserver-trun/)

    - [GMON command exploitation](../vulnserver-gmon/)

    - [GTER command exploitation](../vulnserver-gter/)

    - [GTER command exploitation without
      egghunter](../vulnserver-gter-no-egghunter/)

    - [KSTET command exploitation](../vulnserver-kstet/)

    - [KSTET command exploitation
      alternative](../vulnserver-kstet-alternative/)

    - [LTER command exploitation](../vulnserver-lter-seh/)

    - [Reversing vulnserver](../reversing-vulnserver/)

- I also looked for vulnerable applications with exploits and wrote a
  couple of articles with some tricky exploitations:

    - [QuickZip exploitation](../quickzip-exploit/)

    - [MiTec Net Scanner exploitation](../netscan-exploit/)

- Finally, I wrote an article about backdooring and avoiding
  antivirus:

    - [Backdooring PuTTY](../backdooring-putty/)

Writing those articles helped me a lot to fully put together what was
taught in the course.

The web part of the course was practiced using
[DVWA](http://www.dvwa.co.uk/) and [BWAPP](http://www.itsecgames.com/).

In summary, my total preparation time, including the `CTP` course and
self-study, was around 50 days, with an average daily study time of 9
hours.

## Exam

The `OSCE` exam is a `VPN` network with several objectives to complete.
The `VPN` access is provided for 47h:45m, and they give you another 24
hours after the exam to send a detailed professional report with the
findings and objectives.

My exam was scheduled to start on the 13th of July at 2 PM COT. I was
pretty anxious about what was going to be presented in the exam. I read
a lot of reviews, and almost everyone mentioned that the exam was
"brutal," "made by the devil," and the "hardest thing ever tried." When
I checked the objectives, I realized that the course was indeed a
starting point and that further study of what was taught in the `CTP`
modules is extremely important to complete the exam.

With that in place, I decided to start with the lower points tasks.
After around 4 hours, I had them resolved. It was about 6 PM, and I
decided to take a short rest to eat. After approximately 30 minutes, I
started with one of the higher points tasks and fully completed it after
around 3 hours. It was almost 10 PM, and I was a bit exhausted. I was
trying to figure out the other higher point task, but I couldn’t find a
way even to start. I then took a rest and watched the TV to switch the
context of the brain. At around 11 PM, I got an idea of how to approach
the final task. I started working on my idea, not believing that it
would work, but it did. At around 1 AM, I had completed the final task.

I couldn’t almost sleep that night because of the joy of having achieved
all the exam points. The next morning I started writing the exam report.
As I had plenty of time, I could get additional screenshots. At around 5
PM on that day, I had it completed. It was a 79-page report. I
re-checked it several times, following the [exam
guide](https://support.offensive-security.com/osce-exam-guide/), and
finally submitted it to Offsec.

I got the response a couple of days later, saying that I had
successfully completed the exam and earned `OSCE`\!

## Conclusion

That was my `OSCE` journey. I can only advise you to take the time to
expand what is taught in the course because, in the real world, every
application will have its tricks to be exploited, and you won’t have a
teacher next to you. Also, in my case, writing articles greatly helped
me to consolidate what I had learned. But as always, your mileage may
vary.
