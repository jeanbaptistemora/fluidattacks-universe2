---
slug: crtl-review/
title: A CRTL Review
date: 2022-11-25
subtitle: A Certified Red Team Lead (CRTL) Review
category: opinions
tags: cybersecurity, red-team, training, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1669229599/blog/crtl-review/oleksii-khodakivskiy-RLQB7rX-pyY-unsplash.webp
alt: Photo by Oleksii Khodakivskiy on Unsplash
description: In this post we review the RTO-2 course and CRTL certification offered by Zero-Point Security.
keywords: RTO, CRTL, Red Team, Red Team Lead, Cybersecurity Success, Security Status, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: VP of Hacking and Research
source: https://unsplash.com/photos/RLQB7rX-pyY
---

A few months ago (August 18 to be precise),
[@Rastamouse's](https://twitter.com/_RastaMouse)
Zero-Point Security released the course Red Team Ops II,
or *RTO-2* for short:

![RTO-2 announcement](https://res.cloudinary.com/fluid-attacks/image/upload/v1669229599/blog/crtl-review/Screenshot_2022-11-23_102856.webp)

[RTO-2](https://training.zeropointsecurity.co.uk/courses/red-team-ops-ii)
is meant to be a follow-up to the
[RTO](https://training.zeropointsecurity.co.uk/courses/red-team-ops)
course, focusing on advanced OPSEC tactics, including
bypassing modern enterprise Windows endpoint controls.
This means that RTO-2 is an advanced course, and it's
recommended to have taken and passed at least the RTO
exam to try this course and the associated certification.

By the time of this writing, RTO-2 is listed at £399.00
which includes lifetime access to the course contents
and an exam voucher. You can pay an extra (£425.00 in total)
for 40 hours of lab access, which is highly recommended.

In this post, I will give you an overview of the course
contents and will relate my experience on the exam that
gave me the title of Certified Red Team Lead.

## Red Team Ops II

Early this year, I took and completed the *RTO* course
and associated
[CRTO exam](https://eu.badgr.com/public/assertions/T0j8f2HRS_yrqzNAndBn9Q),
after which I gave a
[talk](https://www.youtube.com/watch?v=a8sOW-Dnqwg)
(in Spanish) on how to pass it.

*RTO* focused on how to perform Red Team operations
on a multi-forest *AD* environment using Cobalt Strike.

OPSEC (Operations Security) notes and tips are given
throughout the course but the main focus is not that.
*RTO-2* was born to compliment *RTO* on the *OPSEC* realm.

Currently, the *RTO-2* course is divided into seven chapters:

1. C2 Infrastructure
1. Windows APIs
1. Process Injection
1. Defense Evasion
1. Attack Surface Reduction
1. Windows Defender Application Control
1. EDR Evasion

The chapter *C2 Infrastructure* presents a way to have
a versatile, resilient and secure C2 architecture,
including the use of redirectors, custom Apache
redirect rules to avoid detection of the C2 infrastructure,
SSL certificates for Beacon and strategies for
beaconing failover. This is very useful for real
engagements on mature corporate environments and, thus,
something a Red Team operator should be aware of.

The chapters *Windows APIs* and *Process Injection*
are both heavily focused on offensive tooling
development. First, there's an overview of commonly
used Windows APIs used for offensive purposes,
how to call those functions from *C++*
and how to make use of unmanaged APIs from managed
languages like *C#* and *VBA* by the use of P/Invoke
and D/Invoke. Then, in the *Process Injection*
chapter, those capabilities are used to inject code into
processes using a wide range of techniques, from
injecting arbitrary code into the current process
to injecting code into a remote process or using
undocumented functions on `ntdll.dll` to create
a new executable section on a running process and
inject the shellcode in it, and even creating a new
suspended benign process, queuing an Asynchronous Procedure
Call with the desired shellcode and dispatching it on a
new thread. They are a couple of fun chapters.

The chapter *Defense Evasion* explains capabilities
used for endpoint controls to detect anomalous
behavior and the way to bypass them. Cobalt Strike
provides some interesting *OPSEC* features out of the box,
like *PPID* spoofing, command line spoofing, avoiding
RWX sections, at-rest Beacon memory encryption
and thread stack spoofing. There is also mention
of what is and how to bypass Event Tracing for
Windows (*ETW*), which is a Windows mechanism that
is used to give EDRs feedback on events dispatched
from user-mode, without the need of API hooking.

The next chapter describes *Attack Surface Reduction*,
which is composed of a set of rules that can be enforced
by a GPO to prevent common techniques used
by attackers. The rules include blocking API calls from
Office macros, creating child processes from Office
applications, blocking processes originating from
*PSExec* and *WMI*, and blocking credential stealing from
the *LSASS* process (which is a complement to mitigations
like *PPL* and *Credential Guard*). Those rules can be
used together, providing a defense-in-depth protection.
However, they are based mainly on blacklists
and the chapter describes ways to bypass some of them.

Then comes the chapter *Windows Defender Application Control*
or *WDAC*, which is about the protection
that allows for the specification of what applications
can be run on a machine, based on things like its path,
digital signature and file hash. As this is a
[security boundary](https://www.microsoft.com/en-us/msrc/windows-security-servicing-criteria),
*WDAC* bypasses are actually fixed by Microsoft.
However, misconfigurations can allow an attacker to
circumvent the control to gain further access to the
machine. So, this chapter teaches us a way to find common
scenarios which can be abused.

And finally, the chapter *EDR evasion* provides
an overview of how modern EDRs work and some
bypasses, including API unhooking, indirect
syscalls and unregistering kernel callbacks. A
fun chapter that even includes kernel-mode
exploits to bypass EDR controls.

As you can see, the course contents is very technical.
By the way,
there are a lot less videos than on the RTO
course, as a certain level of prior knowledge is assumed
to pass it through. However, it is an absolutely
valuable material, given the fact that you have
lifetime access to the course and related
updates to its contents.

<cta-banner
  buttontxt="Read more"
  link="/solutions/red-teaming/"
  title="Get started with Fluid Attacks' Red Teaming solution right now"
/>

## Lab

The *RTO-2* course comes with a companion lab
in Cyber Ranges (formerly Snaplabs) that can be accessed for up to 40 hours.
In the lab, you can practice everything
that's presented in the written material. It's composed
of several machines with different configurations:

- 2 Attacking machines
- 2 Redirectors
- 1 DC
- 1 CA
- 3 Workstations

## Exam

After I was enrolled in *RTO-2*, it took me about three
weeks to complete the material twice (yes, twice) because
there were a lot of new concepts for me to digest.

The course fee includes an exam attempt. You can schedule it
on the platform anytime after you start the course, where
you can pick a start day and hour.

For example, I scheduled the exam to start on November 21 at
9 a.m.

For the exam, you are given 72 hours or
five days (whatever happens first) to obtain four
flags on a given set of machines in an AD environment.
Unlike *CRTO* (in which you need 6 out of 8 flags to pass),
you must collect all the flags to pass this exam.

You must enter the flags in a scoring system
provided with the exam which checks the value and
gives the points. You don't need to write a report, just
enter the flags. In the end, it took me around
11 hours to complete the exam:

![Time spent](https://res.cloudinary.com/fluid-attacks/image/upload/v1669229599/blog/crtl-review/Screenshot_2022-11-22_160255.webp)

![Flags](https://res.cloudinary.com/fluid-attacks/image/upload/v1669229599/blog/crtl-review/Screenshot_2022-11-22_160334.webp)

However, as the exam is designed to last five days, you must
wait until the fifth day to get the certification.

## Exam tips

Here are some of the things that helped me to complete
the exam:

- Follow the indications given on the course and practice
  them in the lab. Just reading will not give you the
  required skills to complete the exam (at least it didn't for me).
- Bear in mind there are things that are not covered in the
  course material. You need to be comfortable using
  tools like Visual Studio Community, not only for
  compiling tools but also for debugging them.
- Practice *C#* development. If you understand
  how a *C#* assembly works, that's also a plus.
- Although *RTO-2* is based on defense evasion and
  advanced *OPSEC* tactics, you must be comfortable with
  things like *AD* enumeration, pivoting, lateral movement,
  user impersonation, Kerberos attacks, etc., and
  have experience using Cobalt Strike. The *RTO* course
  will give you that.
- Technically speaking, you are not strictly required
  to use Cobalt Strike for everything in the exam, but you
  must know how to use other tools that may fulfill
  the same needs.
- There are some exercises proposed in the course. I
  suggest to complete them as that would give you
  confidence when dealing with unexpected requirements
  during the exam.
- Last but not least, enumeration and reconnaissance
  are key to knowing what kind of beast you are
  dealing with.

## Exam results

After the five days of the exam time passed, I received
and email with the certification:

![Cert](https://res.cloudinary.com/fluid-attacks/image/upload/v1669901155/blog/crtl-review/cert1.webp)

## Comparison

I've taken several certifications to date related to
Red Teaming, including *eCPTXv2*, *CRTE*, *CRTP*, *CRTO*,
*PNPT* and *OSCP*. Most of them are focused on exploiting
misconfigurations and vulnerabilities, some of them in
realistic AD environments. As RTO-2 is heavily focused
on defense evasion, the certifications that come closer
to it are *eCPTXv2* and *CRTE*, the former includes some
of the contents found in RTO-2 like evasions on *ETW*,
*EDRs* and things like syscall unhooking and stealth
Office macros.

*Attack Surface Reduction* and
*Windows Defender Appplication Control* are the chapters
that were new to me.

## Conclusions

Red Team Ops II is a very nice course dealing with modern
controls on mature enterprise infrastructures. It will
also prepare you to win in engagements with restricted
environments.

The exam is fun (`s/fun/HARD AS HELL/g`), but I think that the
72 hours/five days given are enough to go through all the stages:
from rage, sadness and stress to, finally, joy.
