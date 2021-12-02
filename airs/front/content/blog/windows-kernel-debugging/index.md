---
slug: windows-kernel-debugging/
title: 'Windows Kernel Exploitation: Lab'
date: 2020-09-09
category: attacks
subtitle: Getting in the deeps of the OS
tags: osee, training, exploit, windows, kernel, hevd
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331228/blog/windows-kernel-debugging/cover_jflria.webp
alt: Photo by Wesley Caribe on Unsplash
description: This post will guide you to setup a lab environment for start
  exploiting Windows Kernel drivers
keywords: Business, Information, Security, Protection, Hacking, Exploit,
  OSEE, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCE, OSCP, CHFI
about2: '"We don''t need the key, we''ll break in" RATM'
source: https://unsplash.com/photos/74JeU2jfnfk
---

This post will be the first of a new series in which we will get deep
into Windows Kernel Exploitation. I’ll be using
[HEVD](https://github.com/hacksysteam/HackSysExtremeVulnerableDriver)
(HackSys Extreme Vulnerable Driver) as the target and, just as we did
with the [Vulnserver](../tags/vulnserver) series, there’s going to be a
different articles on the ways to exploit it.

Before dealing with vulnerabilities, we must setup the lab environment
first. Kernel exploiting is different than application exploiting. When
you are attacking an application, if something goes wrong, you can
simply restart it. In kernel mode, you will likely get an infamous blue
screen of death `BSOD`.

This post will guide you to setup a testing lab for kernel debugging on
a Windows 10 target machine and finally we will be able to install
`HEVD` driver that will be our kernel space victim.

## Pre-requisites

Unlike common user-land applications, the Windows Kernel is commonly
debugged remotely. This is because, as I mentioned earlier, when you
mess with kernel memory, you’re likely making the OS unusable. For that,
we will setup a testing environment with a target Windows OS system (the
debuggee) and some tools in the debugger machine.

The following are the tools needed to setup the environment:

- WinDBG. We’ll use the version that’s included in the [Windows 10
  SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/)

- WinDBG dark theme (optional): Because I like [fancy
  debugging](https://github.com/lololosys/windbg-theme)

- Pykd: To run Python scripts on WinDBG. Download
  [here](https://githomelab.ru/pykd/pykd).

- Windbglib + Mona: Download
  [here](https://github.com/corelan/windbglib)

- Windows 10 1703 (Creators Update): For now, we’d only need the 32
  bits
  [version](https://www.getmyos.com/windows-10-1703-home-pro-education-32-64-bit-free-download)

- A virtual machine player. I’ll be using VMWare Workstation Player.

- HackSys Extreme Vulnerable Driver: Our
  [target](https://github.com/hacksysteam/HackSysExtremeVulnerableDriver).
  We’ll be using the latest stable release (`HEVD v3.00` to the date
  of this post).

- OSR Driver Loader: To load `HEVD` into the OS. Download
  [here](https://www.osronline.com/article.cfm%5earticle=157.htm)

With all the requirements in place, we can start setting up our lab,
which will be composed of a debugger machine, that will be the host
machine from which we will run `WinDBG`; and the debuggee machine, on
which we will install `HEVD` that will be running as a virtual machine.

## Setting up debugger

The first stage is to download and install the Windows 10 SDK. If you
want to install only WinDBG, you can choose only the `Debugging Tools
for
Windows` option:

<div class="imgblock">

![WinDBG](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331225/blog/windows-kernel-debugging/windbg0_kw9dff.webp)

</div>

Once installed, if you search for `windbg` on Windows, you should get
something like this:

<div class="imgblock">

![WinDBG
dark](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331226/blog/windows-kernel-debugging/windbg1_do951r.webp)

</div>

The default `WinDBG` configuration provides a not so friendly UI.
However we can use a dark theme for `WinDBG` (see the Pre-Requisites
section). To do that, just download the `dark.reg` file and install it.
You will get a much friendly UI:

<div class="imgblock">

![WinDBG
dark](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331228/blog/windows-kernel-debugging/windbg2_haqojn.webp)

</div>

Next, we need to adjust the Windows symbols resolution. It is done by
creating a new environment variable `_NT_SYMBOL_PATH` with the value
`srv*https://msdl.microsoft.com/download/symbols`, like this:

<div class="imgblock">

![Environment](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331223/blog/windows-kernel-debugging/env1_j1faww.webp)

</div>

Now, we need to install our friend `mona`. To do that, we need to grab
the `pykd.zip` file located
[here](https://github.com/corelan/windbglib/tree/master/pykd).

That ZIP has two files. The `pykd.pyd` file should be placed at
`C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\winext`. Now run
`vcredist_x86.exe` and follow the installing instructions.

Now, all that’s left is to download `windbglib.py` from
[here](https://github.com/corelan/windbglib/raw/master/windbglib.py) and
`mona.py` from
[here](https://github.com/corelan/mona/raw/master/mona.py) and move them
to `C:\Program Files (x86)\Windows Kits\10\Debuggers\x86`.

To check if that worked, load an executable on `WinDBG`, type `.load
pykd.pyd` and then `!py mona`. You should see something like this:

<div class="imgblock">

![Mona](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331232/blog/windows-kernel-debugging/mona1_tc67fd.gif)

</div>

With that, we have now debugger machine set.

## Setting up the debuggee

Now it’s time to setup our target OS. The first thing is to launch a new
virtual machine with a Windows 10 1703 (Creators Update) instance.

It’s recommended to disable Windows Update service to avoid messing with
our lab results.

With the target machine up an running, it’s time to load `HEVD` in the
system. This is done by copying the `osrloaderv30.zip` and
`HEVD.3.00.zip` files to this target OS and uncompressed them. Then, we
must run `OSR Driver Loader` (run the one in the `WNET → i386 → FRE`
folder)

<div class="imgblock">

![OSR Driver
Loader](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331228/blog/windows-kernel-debugging/osr1_wy6ytq.webp)

</div>

Now browse for the `HEVD.sys` file, click on `Register Service` and then
`Start Service`:

<div class="imgblock">

![Driver
Loaded](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331224/blog/windows-kernel-debugging/driver1_wdx60n.gif)

</div>

To check if that went well, open a terminal and type `driverquery |
findstr HEVD`. You should see something like this:

<div class="imgblock">

![Driver
Loaded](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331226/blog/windows-kernel-debugging/hevd1_vomxc0.webp)

</div>

Great\! To ensure that the `HEVD` driver is load every time, open a
terminal as administrator and run

``` powershell
> sc config HEVD start=system
```

<div class="imgblock">

![Driver
autostart](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331221/blog/windows-kernel-debugging/start1_f8d1tx.webp)

</div>

Now we must connect our target OS with the debugger. You need to launch
a new terminal windows as administrator:

<div class="imgblock">

![CMD](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331231/blog/windows-kernel-debugging/cmd1_md0xv5.gif)

</div>

And then you need to enable remote debugging by issuing the following
command:

``` powershell
> bcdedit /dbgsettings NET HOSTIP:192.168.20.31 PORT:50000
```

You need to change the `HOSTIP` param with the IP of the debugger
machine.

This will return a key that will be used for `WinDBG` to expect for a
connection with that identifier.

<div class="imgblock">

![BCDEDIT](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331223/blog/windows-kernel-debugging/cmd2_zl3vuw.gif)

</div>

In the debugger machine, setup `WinDBG` to listen for a connection with
that key:

<div class="imgblock">

![WinDBG](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331222/blog/windows-kernel-debugging/dbg1_dzht53.gif)

</div>

Now, we need to make Windows to start in `DEBUG` mode and restart. To
that, we should issue the following command:

``` powershell
> bcdedit /debug ON
> shutdown -r -t 0
```

The target OS will restart and the debugger machine should now get a
connection from the target OS:

<div class="imgblock">

![WinDBG](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331231/blog/windows-kernel-debugging/dbg2_nsqhbo.gif)

</div>

Great. Now break the execution (`Debug → Break`) and type `.reload` to
load the debugging symbols:

<div class="imgblock">

![Symbols](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331222/blog/windows-kernel-debugging/symbols1_rhgguz.webp)

</div>

To check if everything’s working,
type <code>x /f nt!<b>Create*Process</b></code>.
This will list all the functions in the `NT` module that contain `Create` and
`Process`.

<div class="imgblock">

![NT Create
Process](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331223/blog/windows-kernel-debugging/nt1_lvlrl7.webp)

</div>

Now, set a breakpoint in `nt!MmCreateProcessAddressSpace` and resume
execution:

<div class="imgblock">

![Breakpoint](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331223/blog/windows-kernel-debugging/bp1_lbxuo1.webp)

</div>

Great\! But as we are going to debug `HEVD`, we must add the debugging
symbols to our environment. If you look at the folder
`HEVD.3.00\driver\vulnerable\x86` you can see several files, including
the `HEVD.sys` driver file and `HEVD.pdb`. The latter is the file
containing the `HEVD` debugging symbols. To load it on our debugger,
follow this steps:

- Create a folder called
  `C:\projects\hevd\build\driver\vulnerable\x86\HEVD`

- Copy the `HEVD.pdb` file in that directory.

<div class="imgblock">

![HEVD
symbols](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331224/blog/windows-kernel-debugging/copy1_h2vptb.webp)

</div>

- On `WinDBG`, type `.reload`

- Type `lm m HEVD` to check if the `HEVD` module is loaded.

- And type `x HEVD!*` to check if the symbols were successfully added.

<div class="imgblock">

![HEVD
symbols](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331226/blog/windows-kernel-debugging/hevdsymbols1_tnj3ip.gif)

</div>

With that, we can start debugging our target machine’s kernel space\!:

<div class="imgblock">

![Breakpoint](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331225/blog/windows-kernel-debugging/bp2_dfrb1i.webp)

</div>

In the [next post](../hevd-dos/), you can see a short reference of
`WinDBG` commands that we will be using during this process.

## Conclusions

This post will help you to setup a working Windows Kernel debugging lab.
In the next posts we will be dealing with some theory on Windows Kernel
and will start [exploiting HEVD](../hevd-dos/).
