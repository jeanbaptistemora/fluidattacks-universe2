---
slug: amsi-bypass/
title: AMSI Bypass Using Memory Patching
date: 2021-07-09
category: attacks
subtitle: Dynamic in-memory AMSI bypass
tags: vulnerability, hacking, exploit, discovery
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1625837523/blog/amsi-bypass/cover-amsi-bypass_sa9bdi.webp
alt: Photo by Calvin Ma on Unsplash
description: In this article we will be able to bypass AMSI using memory patching.
keywords: Business, Information, Security, Protection, Hacking,
  Exploit, Ethical Hacking, Pentesting, Bypass
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCE, OSWP, OSCP, CRTP, CRTE, eWPT
about2: We don't need the key, we'll break in RATM
source: https://unsplash.com/photos/sCrnFwDYMFs
---

Most of us have faced `AMSI` (Antimalware Scan Interface) and suffered
the constraints it poses whenever we want to load a fancy PowerShell
module like
[PowerView](https://github.com/PowerShellMafia/PowerSploit/tree/master/Recon)
or
[Invoke-Mimikatz](https://github.com/PowerShellMafia/PowerSploit/tree/master/Exfiltration)
in the middle of a [Red Team](../../solutions/red-teaming) engagement.

`AMSI` is a programmatic resource offered by Microsoft to enable an
interface to any application for interacting with any anti-malware
product available on the machine. `AMSI` is EDR-agnostic and can be
integrated with any vendor. When `AMSI` appears on stage, something like
this should be familiar:

<div class="imgblock">

![AMSI in
action](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837510/blog/amsi-bypass/amsi1_glc7wk.webp)

</div>

Programmatically, `AMSI` can be included in an application using [Win32
API](https://docs.microsoft.com/en-us/windows/win32/amsi/antimalware-scan-interface-functions)
functions and the `IAmsiStream` `COM`
[interface](https://docs.microsoft.com/en-us/windows/win32/api/amsi/nn-amsi-iamsistream).

As a result, if an application was built with `AMSI`, `amsi.dll` will
become part of the runtime modules of the application. Hence, it is seen
as a `DLL` that is loaded at runtime when the application starts. The
basic architecture of `AMSI` is the following:

<div class="imgblock">

![AMSI Architecture](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837511/blog/amsi-bypass/amsi7archi_hlwvqp.png)

<div class="title">

Figure 1. Source: [Microsoft](https://docs.microsoft.com/en-us/windows/win32/amsi/how-amsi-helps)

</div>

</div>

As you can see, the functions responsible for checking the content for
malicious content are `AmsiScanBuffer()` and `AmsiScanString()`. These
functions act as the entry point that the application uses to send the
suspected tainted input to the underlying antivirus software.

Using a tool like [Process
Hacker](https://processhacker.sourceforge.io/), it is possible to check
the runtime modules on any process in the system. Checking the process
of our PowerShell session, we can see the `AMSI` `DLL` loaded in memory:

<div class="imgblock">

![AMSI
DLL](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837510/blog/amsi-bypass/amsidll1_mve67c.webp)

</div>

We can also check the exported symbols, which are the functions provided
as the high-level interface with `AMSI`. Here we can see all the
exported functions that compose `AMSI`, including `AmsiScanBuffer()` and
`AmsiScanString()`.

<div class="imgblock">

![AMSI
Exports](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837510/blog/amsi-bypass/amsiexports1_ogosn2.webp)

</div>

However, these two functions are not really different. In fact,
`AmsiScanString()` is a small function which uses `AmsiScanBuffer()`
underneath. This can be seen in
WinDBG:

<div class="imgblock">

![AmsiScanString()](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837511/blog/amsi-bypass/amsistring0_tdxnw1.webp)

</div>

And with a
disassembler:

<div class="imgblock">

![AmsiScanString()](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837512/blog/amsi-bypass/amsistring1_gityf1.webp)

</div>

So, if we can bypass the checks performed by `AmsiScanBuffer()`, we can
also bypass `AmsiScanString()`\!

Let’s get it done\!

Here, we can see the disassembly graph of
`AmsiScanBuffer()`:

<div class="imgblock">

![AmsiScanBuffer()](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837532/blog/amsi-bypass/amsiscanbuffer1_bqcyo9.webp)

</div>

As you can see, it is not a complex function either.

At the end of the function, we can see
this:

<div class="imgblock">

![AmsiScanBuffer()](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837510/blog/amsi-bypass/amsiscanbuffer2_oxibne.webp)

</div>

It seems that the actual anti-malware scanning is performed in the
instructions that compose the big box on the left. Also, we notice that
several `JMP` instructions land in `mov eax 0x800700057` and then the
function ends. The value `0x80070057` is a standardized error code from
Microsoft, which is `E_INVALIDARG`. In this case, it’s used by
`AmsiScanBuffer()` to return when the parameters passed by the caller
code are not valid.

So, what would happen if we modify the `AmsiScanBuffer()` function in
memory to bypass the anti-malware checking instructions altogether and
force it always to return `0x80070057`? Let’s check it\!

First, let’s examine the instructions using WinDBG:

<div class="imgblock">

![AmsiScanBuffer()
disassembly](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837536/blog/amsi-bypass/amsiscanbuffer3_f0sb0r.webp)

</div>

Here we can see the disassembled instructions of `AmsiScanBuffer()`. We
can also see the byte-code corresponding to the `mov eax,80070057h`
instruction: `b857000780`.

Using that information, we can modify the very beginning of
`AmsiScanBuffer()` with the following instructions:

``` x86asm
b857000780          mov eax,0x80070057
c3                  ret
```

That would move the `E_INVALIDARG` value (`0x80070057`) to `EAX`, making
it the return value of `AmsiScanBuffer()`, and then the function ends
with a `RET`. As can be seen above, the bytes `b857000780` and `c3` are
the byte-codes of those instructions.

We can do the memory patching using [WinDBG](../hevd-dos/). The steps
are the following:

- Attach the current PowerShell session to WinDBG.

- Break the execution.

- Try to load a common flagged module (e.g., `PowerView`) to see
  `AMSI` in action.

- Check the current instructions of the beginning of
  `AmsiScanBuffer()`. This can be accomplished with `u
  amsi!AmsiScanBuffer` inside WinDBG.

- As we are in a little-endian architecture (`x86_64`), we need to
  reverse the byte-code of the `mov eax,0x80070057 | ret`
  instructions: `c380070057b8`.

- Modify the start of `amsi!AmsiScanBuffer` with those bytes. This can
  be done using `eq amsi!AmsiScanBuffer c380070057b8`.

- Resume the execution.

- Load again `PowerView`.

- Enjoy an `AMSI`-free PowerShell session\!

Let’s check the bypass in action:

<div class="imgblock">

![AMSI
Bypass](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837525/blog/amsi-bypass/success1_e0ak8t.webp)

</div>

However, returning `80070057` is not the only way to bypass
`AmsiScanBuffer()`. In fact, we can make it return `0`, using something
like `sub eax,eax | ret`, and the bypass will be successful as well.

Let’s see:

<div class="imgblock">

![AMSI Bypass
v2](https://res.cloudinary.com/fluid-attacks/image/upload/v1625854245/blog/amsi-bypass/success2_zrp8re.webp)

</div>

Success\! Now we can use `PowerView`, `Invoke-Mimikatz` or any other
[Red Team](../../solutions/red-teaming) tool\!

<div class="imgblock">

![AMSI
Bypass](https://res.cloudinary.com/fluid-attacks/image/upload/v1625837515/blog/amsi-bypass/tools1_t2h47m.webp)

</div>

## Conclusion

Memory patching is a nice trick to use to modify the behavior of running
applications. Keep in mind that this technique is not persistent. The
modification of `AmsiScanBuffer()` is performed **on the memory of the
PowerView process** and the original `amsi.dll` is never touched on
disk.
