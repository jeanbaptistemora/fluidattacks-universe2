---
slug: treacherous-poodle/
title: The Treacherous POODLE
date: 2018-05-02
subtitle: How does the SSL fallback's works
category: attacks
tags: ssl, flaw, cbc
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331125/blog/treacherous-poodle/cover_x0hhns.webp
alt: Unknown person below lights
description: Here we discuss the exploitation of an SSL/TLS flaw that creates
  a fallback on TLS usage to SSL 3.0.
keywords: SSL, CBC, MAC, Padding, Flaw, Exploit, Ethical Hacking, Pentesting
author: Daniel Yepes
writer: cestmoi
name: Daniel Yepes
about1: '"If the doors of perception were cleansed everything would appear
  to man as it is, Infinite." William Blake.'
source: https://unsplash.com/photos/S2qA7JhjI6Y
---

A gas vendor, each week receives gas, which he stores in pipes and
discretely refills them with water. Each day sells this gas to his
clients, unbeknown to an "auditor" in black robes - aka Poodle - paying
attention to this situation. One day the "auditor" undercover, tells the
vendor he will only offer gas with less octanage, thus his pipes should
met certain old requeriments, ignorant of the situation he downgrades
it’s pipes standards until the "auditor" agrees on it.\
Next day, the "auditor" goes to the station, disguised as a client and
ask the vendor to refill his car, next he reveals himself telling the
vendor that he knows what he is doing plus that he has outdated pipes
which represent a threat, but it won’t talk if he pays him a commision
for each sell.

Following act, the auditor was just a regular dude impersonating someone
else. And the vendor in it’s infortune, kept an old standard storage
pipes without realizing the harm it could make to it’s clients or to
himself.

I hope that doesn’t end in the worst analogy in human history, moreover
i hope it helps to understand certain technicisms we will see later. But
please, bare in mind that i’m not an expert on oil industry.

<div class="imgblock">

![blackistopheles](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331125/blog/treacherous-poodle/mephisto-black_fqauve.webp)

<div class="title">

Figure 1. Black poodle

</div>

</div>

## Techninal introduction

The Padding Oracle On Downgraded Legacy Encryption SSL 3.0 (POODLE v3),
it is a protocol vulnerability on <code><b>Secure Socket Layer</b> (SSL 3.0)</code>,
which can make any \*Transport Layer Secure (TLS)\*\` version to fallback to
\`(SSL 3.0) plus it takes advantage on weak encryption using a mechanism
to check message authencity using **Cipher Block Chaining Message
Authentication Code (CBC-MAC)**, allowing an attacker to steal cookies
from an user on the same network.

Discovered on September, 2014, by `Bodo Möller` , `Thai Duong` and
`Krzysztof Kotowicz` from the `Google` security team.

If you are not aware what this terms are check the
[`BEAST`](../release-the-beast/) article, the `(CBC-MAC)` will be
explained here, don’t worry.

## Petting the POODLE

Have you clean yourself from that awful analogy? From now on, guess you
will see why i wrote it.

Whenever client and server are going to start an exchange using
`SSL/TLS`, they use a protocol called
[`Handshake`](https://tools.ietf.org/html/rfc6101#page-21), a process
that is explicity to settle a ground of standards between the client and
the server, where both agrees which `SSL/TLS` **version protocol** will
be used, the **cryptography method** used, **key exchange**, plus more.
All with the final intention to send messages while speaking on the same
language.

But why does this matter? Let’s take a look at that process step by
step:

<div class="imgblock">

![handshaking](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331124/blog/treacherous-poodle/handshake-protocol_nr9tn9.webp)

<div class="title">

Figure 2. Handshake step by step

</div>

</div>

Although i will not describe each step in depth, it is necesary to show
the [overall
process](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380513\(v=vs.85\).aspx),
to understand how does the downgrading process is and where the attack
finally lands.

In simple terms, the attack relies on the fact, that whenever an attempt
to establish a secure connection, it fails (Step 1 to Step 2), then the
server will fallback to an older protocol, [<sup>\[1\]</sup>](#r1).

Remeber the gas vendor downgrading it’s pipes until the "auditor" waits
till he has that old pipes standard? Good…​

Notice that whilst `TLS` is the sucessor of `SSL`, `SSL 3.0` has more
precedence than `TLS 1.0 - 1.2`, mostly to guarantee an smooth user
experience and interoperability across legacy machines, thought, it was
obsolete and insecure. Moreover the attack will even work if both have
`TLS`, [<sup>\[1\]</sup>](#r1).

Well then, let’s see how does the downgrade works.
If in the first step, the client offers it’s highest version of the
protocol, let’s say, `TLS 1.2`, the server, while not having such
version, will negotiate the usage of `TLS 1.0` by downgrading it’s own
protocol version, but notice, that such offering can be repeated several
times as long it fails.

Quite like this:

<div class="imgblock">

![downgrade](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331125/blog/treacherous-poodle/downgrade-version_ybwkle.webp)

<div class="title">

Figure 3. Protocol downgrading

</div>

</div>

Hope you didn’t miss the `CBC-MAC` under the protocol version, because
this is the most interesting part of this attack.

The reason behind the fallback advantage, is to force the client and the
server to use weak encryption. It won’t reveal the key, but it will
allow an attacker to eventually recreate cookies/session parameters by
intercepting the downgraded exchange channel, [<sup>\[2\]</sup>](#r2).

How does this works in `SSL 3.0`? Well, `CBC` works as expected, just
with one subtle difference, the
[`MAC`](https://en.wikipedia.org/wiki/Message_authentication_code) is
done to check the authencity of a message, works like a charm on
fixed-length messages. But\! **not** on variable-length messages as the
padding will fail to be fully verified when decrypting.

Remeber from that stupid analogy the gas vendor refilling it’s gas pipes
with water? Well, that’s what the padding is, although the `CBC-MAC`
algorithm won’t have any economic advantage, it just tries to handle
variable-length messages, by adding extra random characters to met the
needed multiple block-length, to get 8 or 16 bytes blocks depending on
the algorithm (DES, 3DES, AES). Taking advantage on this is ofently
called [`Padding Oracle
Attack`](https://www.owasp.org/index.php/Testing_for_Padding_Oracle_\(OTG-CRYPST-002\)).

So, here is where the version downgrade lands. But let’s see it in
action with this simple example, i’m gonna use 8-bytes blocks to make it
short.

Let’s suppose we have already intercepted a client-server communication
and we have forced the use of `SSL 3.0`, now we are going to reveal the
encrypted messages while both are at the last step of the handshake.

Without too much details, the client sends a request to the server:

<div class="imgblock">

![request-example](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331124/blog/treacherous-poodle/http-request_lcjscl.webp)

<div class="title">

Figure 4. Http request

</div>

</div>

A message request from the client which is going to be encrypted with
`DES` using `CBC-MAC` mode. First at all, the `MAC` of the message
should be computed:

1. `IV` is full of 0’s

2. `XOR` with each block of plaintext

<div class="imgblock">

![computing-mac](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331125/blog/treacherous-poodle/mac_azch33.webp)

<div class="title">

Figure 5. Compute MAC

</div>

</div>

And append it to the end of the message, then check if the length of the
message is a multiple of 8 (block-size), if not, add random padding
characters at the end until it hits a multiple of the block-size and the
final byte becomes the length of the padding, which output is like this:

<div class="imgblock">

![request-example](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331124/blog/treacherous-poodle/http-request-fixed_qsd2oi.webp)

<div class="title">

Figure 6. Padded message example with MAC code

</div>

</div>

> **Note**
>
> I will represent the random padding characters by "-", don’t get
> confused.

Then the process of encryption with `CBC` as described in the
[`BEAST`](../release-the-beast/) article. Which output is:

<div class="imgblock">

![Encrypted msg](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331125/blog/treacherous-poodle/cbc-in-action_u2oru6.webp)

<div class="title">

Figure 7. Output of encrypted message

</div>

</div>

The message is then sent to the server, and now consider the decryption
process on the server:

<div class="imgblock">

![cbc-enc](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331125/blog/treacherous-poodle/cbc-decryption_ylqkho.webp)

<div class="title">

Figure 8. CBC decryption

</div>

</div>

Taking on account that the exchange is being made with `SSL 3.0` and the
fact that when a `CBC` encryption algorithm is used, `SSL 3.0` does not
cover padding with `MAC`. Which means, that the mechanism used to verify
the authenticity of a message won’t be able to fully verify it while
decrypting it.

Did you spot something weird with this mechanism, but besides than the
stated flaw? No? Perhaps on encryption? Or before?

Well, if you didn’t, here is a clue: Authentication should be done after
encryption, **NOT** before. The
[Authenticate-then-Encrypt](https://moxie.org/blog/the-cryptographic-doom-principle/)
poses a problem, which by that time wasn’t that evident.

<div class="imgblock">

![what](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331125/blog/treacherous-poodle/you_fkwp1x.webp)

<div class="title">

Figure 9. SSL blames SSL

</div>

</div>

So, to process each block of the ciphertext, denoted as **C**, the
recipient determines each block of the plaintext, denoted as **P**,
using the following mathematical formula, [<sup>\[3\]</sup>](#r3):

**P<sub>i</sub>** = **D<sub>k</sub>(C<sub>i</sub>) XOR C<sub>i-1</sub>**

1. Where **C<sub>0</sub>** is the `Initialization Vector (IV)`

2. **C** ranges from **C<sub>1</sub>** to **C<sub>n</sub>**.

3. **P** ranges from **P<sub>1</sub>** to **P<sub>n</sub>**.

4. **D<sub>k</sub>** the block-cipher decryption using per-connection
    key **K** or

This in simple words means, that each current block is `XORed` with the
previous block, then checks and removes the padding at the end, and
finally checks and removes the `MAC`.

So how does the attack use decryption to get the plaintext without the
key?

1. Considering our padding block `[------7]`, **C<sub>n</sub>**.

2. And the block we want to decrypt, **C<sub>i</sub>**.

Replace **C<sub>n</sub>** by **C<sub>i</sub>**, usually this block
modification will be rejected, but only once on 256 request, it won’t,
the attacker will conclude that the last byte of **C<sub>n-1</sub>**
XORed with **C<sub>i</sub>** will yield, **7**.

Mathematically speaking **D<sub>k</sub>(C<sub>i</sub>)\[7\] XOR
C<sub>n-1</sub>\[7\] = 7**

As `SSL 3.0` doesn’t care for the rest of bytes on the padding block,
less for the block-length, it will accept it. And thus that
**P<sub>i</sub>\[7\] = 7 XOR C<sub>n-1</sub>\[7\] XOR C<sub>i-1</sub>**
a calculation which will reveal the bytes unknown on the block the
attacker wanted.

This can be seem like a duplication of certain block on the stream,
which will replace the last block, thus, the last byte will be `XORed`
with the last byte of the previous block, resulting in **7**,
[<sup>\[3\]</sup>](#r3). This is possible as the block is on the same
stream, thus when the message authentication is performed it will take
it as a valid block.

As stated before, this trick will be performed almost 256 request until
it’s accepted, each fail means the last byte has to be shifted.

Plus it has to be done byte by byte on the cipher stream or at least, in
each byte of the block the attacker wants to know.

## Requeriments

Although the attack seems quite similar with the `BEAST` attack, it
relies enterely on a flaw on `SSL/TLS` protocol.

The only requirements are:

1. Run a `Man-In-The-Middle Attack` against the victim.

2. Perform the Downgrade if `TLS` is used.

Once an attacker has done it, it can steal the cookies/session from a
user.

## Any patch?

Well, there is a funny quote by the researchers:

> disabling the **SSL 3.0** protocol in the client or in the server (or
> both) will completely avoid it. If either side supports only **SSL
> 3.0**, then all hope is gone, and a serious update required to avoid
> insecure encryption.

But there was and still exist an iniciative to [disable
ssl](http://disablessl3.com/) from all browsers and on any servers using
it.

## References

1. [Bodo Möller , Thai Duong, Krzysztof Kotowicz (Sept 2014). This
    POODLE Bites: Exploiting The SSL 3.0
    Fallback](https://www.openssl.org/~bodo/ssl-poodle.pdf)

2. [Assessing the risk of
    POODLE](https://isc.sans.edu/forums/diary/Assessing\`the\`risk\`of\`POODLE/19159/)

3. [Wikipedia, Block Cipher Mode of
    Operation](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)

4. [ImperialViolet (Oct 2014). POODLE attacks on
    SSLv3](https://www.imperialviolet.org/2014/10/14/poodle.html)
