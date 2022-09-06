---
slug: offensive-hyperv-directx-1/
title: DirectX/HyperV An Offensive View
date: 2022-09-06
category: attacks
subtitle: A Black Hat talk follow up
tags: vulnerability, hacking, exploit, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1662484193/blog/offensive-hyperv-directx-1/axel-ruffini-iulnjpZyWnc-unsplash.webp
alt: Photo by Axel Ruffini on Unsplash
description: We will take a brief understanding at DirectX, a new attack surface on Hyper-V
keywords: Business, Security, Hacking, Exploit, Ethical Hacking, Pentesting, Bypass, Evasion, Windows
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: https://www.linkedin.com/in/andres-roldan/
about2: We don't need the key, we'll break in RATM
source: https://unsplash.com/photos/iulnjpZyWnc
---

I attended Black Hat USA 2022. The available talks
were diverse, all of them inviting and some of them
particularly attractive for my current field of work,
which is currently mainly focused on advanced topics
on Red Teaming and Exploit Development.

One of the talks I found most interesting was
[DirectX: The new Hyper-V Attack surface](https://i.blackhat.com/USA-22/Thursday/US-22-Hong-DirectX-The-New-Hyper-V-Attack-Surface.pdf),
presented by Zhenhao Hong
(@[rthhh17](https://twitter.com/rthhh17)). In that
talk, four vulnerabilities were presented (CVE-2021-43219,
CVE-2022-21898, CVE-2022-21912 and CVE-2022-21918)
regarding bugs like Null Pointer Dereference, Arbitrary
Address Read and Arbitrary Address Write, which included a
few lines of the PoC (Proof-Of-Concept) code to trigger
each vulnerability.

Also, it was presented an overview of the architecture
of Hyper-V DirectX components and a proposed fuzzing
methodology to find new vulnerabilities.

In this post(s) I will try to follow up with that
research and overcome expected shortcomings of the
talk due to time restrictions:

- There is no public access to the PoC codes.
- There is no public access to the fuzzing artifacts.
- The infrastructure to perform research on that
  specific environment was also not covered.
- Hyper-V → DirectX integration is a work-in-progress
  for Microsoft, so many of the things mentioned in that
  talk are no longer working in the current version of Windows 11.

## Setting up environment

We have already covered [a post](../windows-kernel-debugging/)
to set up a basic environment to perform remote kernel
debugging. It involved creating a virtual machine,
enabling debug mode using a network connection and
plugging in the debugger. That could be done using
a single computer.

This case is different. We need to debug a DirectX
GPU adapter on a Windows machine acting as hypervisor
using Hyper-V with a VM running Linux. Enabling
virtualized extensions (__VT-x__) in a Windows VM can
enable a nested Hyper-V, but the DirectX adapter will
not be visible. After testing different scenarios,
I ended needing to use two laptops.

The first laptop will be the debuggee (`host1`).
In that laptop, the latest version of Windows 11 was
installed:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481151/blog/offensive-hyperv-directx-1/Screenshot_2022-09-02_170953.webp)

</div>

In that machine, WSL was installed along with Kali
as guest VM:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481154/blog/offensive-hyperv-directx-1/Screenshot_2022-08-26_171949.webp)

</div>

The latest stable kernel used on WSL for the guest
machines is `5.10.102.1-microsoft-standard-WSL2`.
However, I wanted to use the latest version available
of [WSL](https://github.com/microsoft/WSL2-Linux-Kernel/releases),
so I built it to use it. To the date of the exercise,
the latest version was `5.15.57.1`.

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481152/blog/offensive-hyperv-directx-1/Screenshot_2022-09-02_171509.webp)

</div>

Make sure that you have partitionable GPUs
using `Get-VMHostPartitionableGpu`:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481154/blog/offensive-hyperv-directx-1/Screenshot_2022-08-26_172158.webp)

</div>

In a [past article](../windows-kernel-debugging/), we could
be able to perform remote debugging using a network connection.
I tried to do that, but failed because the physical network
adapter didn't support debugging:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481154/blog/offensive-hyperv-directx-1/Screenshot_2022-08-26_172126.webp)

</div>

So I had to use another approach. Luckily, Windows has several
ways to be debugged. In this case, I chose to use
[USB3 debugging](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/setting-up-a-usb-3-0-debug-cable-connection).
To do that, I had to:

- Find a USB3 port on my debuggee laptop with debugging support.
  That could be done using __USBView__ from Windows SDK:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481154/blog/offensive-hyperv-directx-1/Screenshot_2022-08-26_172045.webp)

</div>

- Enabling debug options.

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481154/blog/offensive-hyperv-directx-1/Screenshot_2022-08-26_172015.webp)

</div>

- Plug the debugger and the debuggee using a quality USB3 cable.

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481154/blog/offensive-hyperv-directx-1/Screenshot_2022-08-26_171730.webp)

</div>

In the end, the lab environment looked like this:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481677/blog/offensive-hyperv-directx-1/IMG_0964.webp)

</div>

We are ready now!

## An updated Hyper-V DirectX data flow

The following graph was presented by Zhenhao Hong
(@[rthhh17](https://twitter.com/rthhh17)) which
nicely describes the DirectX components and how are
they accessed by a VM on Hyper-V:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481803/blog/offensive-hyperv-directx-1/Screenshot_2022-09-06_112949.webp)

</div>

The following is a detailed and updated flow of these
interactions:

1. There is a Linux driver called `dxgkrnl.ko` which
   exposes a set of `IOCTL` commands to interact with the host's
   DirectX adapters.
2. When a `IOCTL` is called, there is another driver
   called `hv_vmbus.ko` which uses the
   [VMBUS](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-architecture)
   to create a packet and a bus channel between the VM,
   the hypervisor and the kernel of the host machine.
3. The `IOCTL` payload is contained in a structure
   called `DXGADAPTER_VMBUS_PACKET` which contains the
   command (`DXGK_VMBCOMMAND`) and the command options
   to be sent.
4. The host machine implements the receiving and processing
   counterpart in the `dxgkrnl.sys` driver.
5. The procedure `dxgkrnl!VmBusProcessPacket` is the `VMBUS`
   receiving method that handles the `DXGADAPTER_VMBUS_PACKET`
   payload.
6. If the `DXGK_VMBCOMMAND` is a global command (listed
   on `enum dxgkvmb_commandtype_global`), a function pointer
   (indirect call) is set to a method with the form
   `dxgkrnl!DXG_HOST_GLOBAL_VMBUS::<command>`, for example
   `dxgkrnl!DXG_HOST_GLOBAL_VMBUS::VmBusDestroyProcess`.
   Otherwise, the flow skips to point 7.
7. If the `DXGK_VMBCOMMAND` is not a global command packet,
   it is processed by `dxgkrnl!VmBusExecuteCommandInProcessContext`
   which also uses indirect calls (function pointers) to compute
   the target handling method of that specific `IOCTL`
   request command. In this case, the handler has the
   form `dxgkrnl!DXG_HOST_VIRTUALGPU_VMBUS::<command>`, for
   example `dxgkrnl!DXG_HOST_VIRTUALGPU_VMBUS::VmBusCreateDevice`.
8. The handling method casts the `DXGADAPTER_VMBUS_PACKET`
   packet using `dxgkrnl!CastToVmBusCommand<DXGKVMB_COMMAND_<command>>`
   (for example,
   `dxgkrnl!CastToVmBusCommand<DXGKVMB_COMMAND_DESTROYPROCESS>`)
   to filter the data as needed to this specific command
   handler.
9. The handler performs boilerplate checks and perform
   the desired action. In some cases, it delivers the packet
   to a function with the pattern `dxgkrnl!*Internal`
   (for example, `dxgkrnl!SignalSynchronizationObjectInternal`)
   or `dxgkrnl!Dxgk<command>Impl`
   (for example, `dxgkrnl!DxgkCreateDeviceImpl`) which has the
   required interfaces to deliver the packet to the MMS
   (Microsoft Media System) components of DirectX that resides
   on the `dxgmms1.sys` and `dxgmms2.sys` drivers.
10. The MMS system is finally in charge to talk with the
    corresponding GPU driver, which exposes the adapter that
    can virtual or physical.
11. In the end, the response is sent back to the VM
    via `dxgkrnl!VmBusCompletePacket`.

It's a complex process if you read it, but let's look at it
in action. Let's see an example performing only one
command: `Create Device`. Here is the sample code.

```c
/*
Hyper-V -> DirectX Interaction Sample Code

Compile as: cc -ggdb -Og -o sample1 sample1.c

Author: Andres Roldan <aroldan@fluidattacks.com>
LinkedIn: https://www.linkedin.com/in/andres-roldan/
Twitter: @andresroldan
*/

#define _GNU_SOURCE 1
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include "/home/aroldan/WSL2-Linux-Kernel-linux-msft-wsl-5.15.y/include/uapi/misc/d3dkmthk.h"

int open_device() {
    int fd;
    fd = open("/dev/dxg", O_RDWR);
    if (fd < 0) {
        printf("Cannot open device file...\n");
        exit(1);
    }
    printf("Opened /dev/dxg: 0x%x\n", fd);
    return fd;
}

void create_device(int fd) {
    int ret;
    struct d3dkmt_createdevice ddd = { 0 };
    struct d3dkmt_adapterinfo adapterinfo = { 0 };
    struct d3dkmt_enumadapters3 enumada = { 0 };

    enumada.adapter_count = 0xff;
    enumada.adapters = &adapterinfo;
    ret = ioctl(fd, LX_DXENUMADAPTERS3, &enumada);
    if (ret) {
        printf("Error calling LX_DXENUMADAPTERS3: %d: %s\n", ret, strerror(errno));
        exit(1);
    }
    printf("Adapters found: %d\n", enumada.adapter_count);

    ddd.adapter = adapterinfo.adapter_handle;
    printf("Adapter handle: 0x%x\n", ddd.adapter.v);
    printf("Creating device\n");
    ret = ioctl(fd, LX_DXCREATEDEVICE, &ddd);
    if (ret) {
        printf("Error calling LX_DXCREATEDEVICE: %d: %s\n", ret, strerror(errno));
        exit(1);
    }
    printf("Device created: 0x%x\n", ddd.device);
}

int main() {
    int fd;
    struct d3dkmthandle device;

    fd = open_device();
    create_device(fd);
    close(fd);
}
```

It's a straightforward code:

1. Opens a handle to `/dev/dxg`.
2. Uses that handle to enumerate the adapters available.
3. Creates the device handle.

The output on the console should be something like:

```console
aroldan@host1:~$ cc -ggdb -Og -o sample1 sample1.c
aroldan@host1:~$ ./sample1
Opened /dev/dxg: 0x3
Adapters found: 2
Adapter handle: 0x40000000
Creating device
Device created: 0x40000000
```

Let's first look at the Linux side of things.
First, I'm going to pause the execution on `gdb`
at `*create_device+176` which is when the `IOCTL`
calling to `LX_DXCREATEDEVICE` is performed:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481152/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_150948.webp)

</div>

If we see the value of the variable `ddd.device`
before the call, you should see something like this:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481152/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_151006.webp)

</div>

After the `IOCTL`, we can see that the device handle
is now populated:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481152/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_151035.webp)

</div>

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481152/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_151051.webp)

</div>

Now, let's check at the host running Windows. We're
going to need to set a few breakpoints to check the
flow. First, let's put a breakpoint
at `dxgkrnl!VmBusProcessPacket`

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481152/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_151313.webp)

</div>

Inspecting `dxgkrnl!VmBusProcessPacket` we can see at
`dxgkrnl!VmBusProcessPacket+0x568` an indirect call
being performed. This is where `dxgkrnl!VmBusProcessPacket`
handles `DXGK_VMBCOMMAND` global commands. You can find
indirect calls (function pointers) in kernel space because
they are wrapped by calls to `_guard_dispatch_icall_fptr`,
which is added when the kernel is compiled with
[CFG](https://docs.microsoft.com/en-us/windows/win32/secbp/control-flow-guard).

Let's put another breakpoint there:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662482749/blog/offensive-hyperv-directx-1/Screenshot_2022-09-06_114526.webp)

</div>

Now, let's put a breakpoint
at `dxgkrnl!VmBusExecuteCommandInProcessContext`:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481153/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_160007.webp)

</div>

In that function
at `dxgkrnl!VmBusExecuteCommandInProcessContext+0x1f0`
we can also find an indirect call being performed. We
can set a new breakpoint in that place:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481153/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_160050.webp)

</div>

Finally, a breakpoint at `dxgkrnl!VmBusCompletePacket`
will be set:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662482824/blog/offensive-hyperv-directx-1/Screenshot_2022-09-06_114653.webp)

</div>

We should now have five breakpoints as follows:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481153/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_160835.webp)

</div>

I'm going to
reference the steps described above in the following
execution flow. When we run the sample code again,
it hits our first breakpoint (step 5):

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481152/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_151349.webp)

</div>

When we resume the execution, the next breakpoint is
hit at the `dxgkrnl!_guard_dispatch_icall_fptr` call,
which is an indirect call to the first command's handler.
In this case, the handling function was resolved
as `dxgkrnl!DXG_HOST_GLOBAL_VMBUS::VmBusCreateProcess` (step 6):

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481154/blog/offensive-hyperv-directx-1/bp2.gif)

</div>

If we resume the execution, a call
to `dxgkrnl!VmBusCompletePacket` is performed to send to
the caller the result of
the `dxgkrnl!DXG_HOST_GLOBAL_VMBUS::VmBusCreateProcess`
command:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481153/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_162624.webp)

</div>

When we resume the execution twice, first the breakpoint
at `dxgkrnl!VmBusProcessPacket` is hit (step 5) as expected,
but the next breakpoint hit is
at `dxgkrnl!VmBusExecuteCommandInProcessContext`, which means
that the incoming command is not a global command (step 7):

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481153/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_162650.webp)

</div>

Now, when we resume the execution, the next breakpoint is
hit at `dxgkrnl!VmBusExecuteCommandInProcessContext+0x1f0`
which contains the indirect call resolved to a non-global
command. In this case, we see the command we sent
(`LX_DXCREATEDEVICE`) for creating a device:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481154/blog/offensive-hyperv-directx-1/bp4.gif)

</div>

In that method,
at `dxgkrnl!DXG_HOST_VIRTUALGPU_VMBUS::VmBusCreateDevice+0x8d`
we can see a call
to `dxgkrnl!CastToVmBusCommand<DXGKVMB_COMMAND_CREATEDEVICE>`
which will extract the needed parts of
the `DXGADAPTER_VMBUS_PACKET` (step 8):

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481153/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_163241.webp)

</div>

Here's the decompiled code:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662483805/blog/offensive-hyperv-directx-1/Screenshot_2022-09-06_120255.webp)

</div>

Later on that function,
at `dxgkrnl!DXG_HOST_VIRTUALGPU_VMBUS::VmBusCreateDevice+0x3b0`,
we can see a call to `dxgkrnl!DxgkCreateDeviceImpl` which do
the dirty job (step 9):

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662483947/blog/offensive-hyperv-directx-1/Screenshot_2022-09-06_120538.webp)

</div>

And finally, when we continue the execution, the breakpoint
at `dxgkrnl!VmBusProcessPacket` is hit. According to
[this article](https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/vmbuskernelmodeclientlibapi/nc-vmbuskernelmodeclientlibapi-fn_vmb_channel_packet_complete),
the second parameter of the function `dxgkrnl!VmBusProcessPacket`
is the data to be sent back to the caller (step 11). It means
that if we check the double word data pointed by the
`rdx` register, we should see the device handler (`0x40000000`)
returned as we saw before in the Linux VM output:

<div class="imgblock">

![dxgkrnl](https://res.cloudinary.com/fluid-attacks/image/upload/v1662481153/blog/offensive-hyperv-directx-1/Screenshot_2022-09-05_162933.webp)

</div>

Great!

You can download the `sample1.c` file [here](./sample1.c).

## Conclusion

The Hyper-V DirectX interaction is not officially documented.
You can understand most of the internals by
[reading](../../categories/sast/) the WSL code,
performing [reverse engineering](../../categories/re/) of the
Windows drivers and doing
[kernel debugging](../../categories/dast/).
In the next article, we will see that most of the `dxgkrnl`
commands are not stateless and some of them depends on
creating certain kernel objects first. We will also see how
to leverage this architecture using an offensive approach.
