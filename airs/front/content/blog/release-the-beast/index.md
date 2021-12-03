---
slug: release-the-beast/
title: Release the BEAST!
date: 2018-04-27
subtitle: Understanding the BEAST
category: attacks
tags: tls, cbc, vulnerability
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331051/blog/release-the-beast/cover_lcrn2e.webp
alt: Release the beast
description: How does a theorized attack become practical after more
  than 10 years? Find out here.
keywords: TLS, CBC, Injection, Vulnerabilty, BACPA, CPA,
  Ethical Hacking, Pentesting
author: Daniel Yepes
writer: cestmoi
name: Daniel Yepes
about2: '"If the doors of perception were cleansed everything would appear
  to man as it is, Infinite." William Blake.'
source: https://unsplash.com/photos/QZ2EQuPpQJs
---

The **Browser Exploit Attack on SSL/TLS (B.E.A.S.T)**, - bet you thougth
it was a rampage hack that launched nukes - it is a practical attack
[demonstrated](https://vnhacker.blogspot.com.co/2011/09/beast.html) by
`Thai Duong` and `Julian Rizzo` at `ekoparty` in 2011.

That was the lamest introduction ever, it’s not because the attack
doesn’t deserve it, it’s because it is quite a `BEAST` to ride. As a
warning to all `mathemagicians` i will try to avoid most if not all math
terms.

Shall we begin\!?

## SSL/TLS Implementation flaw

The core of the attack starts here, with the **Secure Socket Layer
`(SSL)`** and **Transport Layer Security `(TLS)`**, it’s successor,
both, essential protocols to transmit our data secured by implementing
cryptography, in this case, symmetric cryptography using **Cipher Block
Chaining (CBC)** mode, plus one single but significant change introduced
on the `CBC` mode on `TLS 1.0`, the way how **`Initialization Vectors
(IV)`** were computed.

Back in 2004, an [attack](https://www.openssl.org/~bodo/tls-cbc.txt) was
theorized, `SSL 3.0` and `TLS 1.0` could be **exploited** by a variation
of the [`Chosen Plaintext
Attack`](https://simple.wikipedia.org/wiki/Chosen-plaintext_attack) on
`CBC`, if the `IV` is **known** or can be **predicted** by the
**attacker**, **attempting** to **inject plaintext** to be **encrypted**
with the `IV` and **if** the **output** of the **injected plaintext** is
**identical** as the **output** of one of the **packets** sent by the
client, then the attack was **succesfull**\!, [<sup>\[1\]</sup>](#r1).

Breathe\! I know it’s hard to assimilate, but let’s crumble it into
small pieces:

### Symmetric encryption with CBC mode

For the sake of simplicity, let’s take the Data Encryption Standard
(DES) for this sample. Short explaination, **symmetric encryption**
algorithm, where a **plaintext** comes in **along** with a **key**, the
plaintext it’s chopped into a **fixed-length**, **blocks** of **8
bytes** to be precise. Then each block along the key is **encrypted** to
**result** in a **ciphertext** made of **8 bytes blocks**,
[<sup>\[2\]</sup>](#r2).

Now, the `CBC mode`. Each block of **plaintext**, is `XORed` (Bit a bit
operation) with the **previous** `ciphertext` block **before** being
**encrypted**. This way each ciphertext block depends on all plaintext
blocks processed up to that point, [<sup>\[3\]</sup>](#r3).

Almost there, we gotta need to know what is a block cipher. It is a
**deterministic** algorithm **operating** on fixed-length groups of
bits, called a **block**, [<sup>\[4\]</sup>](#r4). The overall purpose
of a block cipher is to ensure the **transformation** of each block,
while on encryption or decryption, it means, giving it more
**randomness**, which in this terms means more **security**.

<div class="imgblock">

!["CBC Mode Encryption"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331048/blog/release-the-beast/cbcmode_koiybd.webp)

<div class="title">

Figure 1. CBC Mode - Wikipedia

</div>

</div>

Last but not least, the `initialization vector (IV)` In a few words, it
is the first **block cipher** which, makes each message **unique**, the
`IV` is made entirely of **random** data.

What is so special about this? let’s join all of that.

**Alice (Client)** and **Bob (Server)** are going to chat, but **D
(Attacker)** is an active stalker with feelings for Alice and he wants
to learn about her habits.

<div class="imgblock">

!["Stalker"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331048/blog/release-the-beast/stalker_mirszv.webp)

<div class="title">

Figure 2. It was a mistake…​

</div>

</div>

**Alice** sends a message **"I’m hungry, send me pizza"** to **Bob**.
The only thing **D knows** is that Alice most of the time **starts** the
message with **"I’m hungry"**. The message encrypted with `DES` is:

<div class="imgblock">

!["DES"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331048/blog/release-the-beast/message-encrypted_z3gaad.webp)

<div class="title">

Figure 3. Message encrypted with DES

</div>

</div>

Remeber, encryption is done on the message splitted in **8 bytes
blocks**, just to make it simple we will take the first two blocks:

<div class="imgblock">

!["DES sample"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331049/blog/release-the-beast/des-example_airbwt.webp)

<div class="title">

Figure 4. DES sample

</div>

</div>

**D** somehow can see **Alice’s** encrypted connection, whilst **D**
does **not know** **Alice’s key**, **knows** how the **"I’m hung"**
looks like **after** **encrypted**, after all **knows** how the
**message starts**. But does not know the rest, **D** only has to
**guess and trick** Alice into **encrypt** several **messages** until it
**matches** the second block.

Notice, that this **guess and trick** game does **not compromise the
key**, this is pure Chosen-Plaintext Attack, you know barely some
portion of the message and you just try to craft more combinations until
it mathches.

Here is where `CBC` comes in **action**. Is specially **designed** to
overcome this kind of situations, the **addition** of the block cipher
before encrypting each block **invalidates** the `Chosen-Plaintext
Attack`, let’s see that with this simple example:

<div class="imgblock">

!["CBC sample"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331047/blog/release-the-beast/cbc-sample_jr8tbr.webp)

<div class="title">

Figure 5. CBC sample

</div>

</div>

As you may see, it’s quite hard to guess the block that came before it,
specially when the `IV` it’s random. You migth think this made it
secure, isn’t?

But hey, if things were easy like that, i wouldn’t be writting this
article. Remeber i mentioned a theorized vulnerabilty that came up in
2004? There is a variation called **Blockwise-Adaptive Chosen-Plaintext
Attack (BACPA)**, [<sup>\[4\]</sup>](#r4).

The attack derives from the way `SSL/TLS` transmit data: Any plaintext
sent is fragmented into blocks of length less than or equal to
**2<sup>14</sup> bytes**, [<sup>\[5\]</sup>](#r5).

Which is then processed and sent as follow:

**Unencrypted Portion:**

1. Message type (8 bits);

2. Major/minor version number (16 bits);

3. Length counter(16 bits);

**Encrypted Portion:**

1. Plaintext fragment (\< = 2<sup>14</sup> bytes);

2. Message authentication code (160 bits);

3. Padding (0-56 bits);

4. Padding length (8 bits);

But why do we care about how `SSL/TLS` sends data? Well, if a message is
splitted into several chunks, following the description above, a **100
bytes message** is **splitted** into **10-10 bytes blocks** of messages,
which during transmision **each** packet will be **encrypted**, were the
**first** package will be the **only** one who’s `IV` it’s **random**,
then the **last 8 bytes** of **each** former packet (or **n-1 package**)
will be the `CBC` **residue** of the first **8 bytes** of packet **n**.

Practically, it means, the **residue** of the **last** package
**becomes** the `IV` of the **current** package, technique ofently
referred as `Chaining IV’s across messages`.

Thus, an attacker can perform the **Blockwise-Adaptive Chosen-Plaintext
Attack** by injecting his own packets into the `SSL` stream, he’ll know
what `CBC` will be used to encrypt the beginning of his message.

Perhaps this example will clarify all of this:

Alice and Bob will start their communication, we already know Alice will
send **"I’m hungry, send me pizza"**, here we can see how the process
starts, with a random `IV`, Then the message is splitted into **8-bytes
chunks**, each block after the first will use the `CBC` residue and
lastly will be encrypted:

<div class="imgblock">

!["DES+CBC in action"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331048/blog/release-the-beast/tls-cbc-des_lutehd.webp)

<div class="title">

Figure 6. DES encryption CBC mode

</div>

</div>

The only thing D can see from there is:

<div class="imgblock">

![Output](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331048/blog/release-the-beast/output_vcdc41.webp)

<div class="title">

Figure 7. Output

</div>

</div>

But performing the packet injection rigth there would throw an output
not worth considering, because `TLS` will `XOR` the injected plaintext
with the previous residue `CBC`, - The next CBC is just a supossition,
for the sake of not extending the example -\
as seen here:

<div class="imgblock">

!["Failed injection attempt"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331047/blog/release-the-beast/fail-injection_iecchu.webp)

<div class="title">

Figure 8. Initial injection

</div>

</div>

The attacker to be able to inject succesfully it’s own packet must `XOR`
the guessed plaintext with that `CBC` Residue as seen here:

<div class="imgblock">

!["Xoring with next block"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331049/blog/release-the-beast/xor-injection_wy4obh.webp)

<div class="title">

Figure 9. Xoring with next block

</div>

</div>

Then `XOR` that output with the second `CBC` residue. That remaining
output is then substracted with `XOR` properties, the commutativity
propertie to be exact, `A xor B = B xor A`

<div class="imgblock">

!["CBC Residue XORing"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331048/blog/release-the-beast/stream-injection_v1qkgt.webp)

<div class="title">

Figure 10. CBC Residue XORing with injected packet

</div>

</div>

And if the **attacker** is **able** to **inject** it’s **packet** on the
stream **Alice** would end up **encrypting** it with her **key**, thus
**revealing** the **message**, well, at least a fragment:

<div class="imgblock">

!["Injection matched"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331048/blog/release-the-beast/injection-success_tb5xxc.webp)

<div class="title">

Figure 11. Injection succed

</div>

</div>

## Where is the Browser attack?

Perhaps you migth be thinking how this can be exploited? Well, the **B**
in `BEAST`, stands for Browser if you remember, is not there because
it’s fancy.

An attacker is entitled to perform a `Man-In-The-Middle-Attack` on a
user using an `HTTPS` connection, which allows the attacker to get the
ciphered message, splitted as seen previously.

`Rizzo` and `Duong` wrote a Java Applet Agent, which purpose was to
intercept `HTTPS` request and trick the user into visiting their `Java
Applet`. Once the user were in the `Applet web site` they took advantage
of the [`Same-Origin Policy
(SOP)`](http://resources.infosecinstitute.com/bypassing-same-origin-policy-sop)
vulnerabilty, although it worked only for the time the user was logged
in.

Basically, `SOP` is meant to prevent `cross-site` issues, like **evil
site** trying to access session and cookies from your bank account
stored within the same browser using `JavaScript`. But back then several
browsers were affected by this vulnerability.

To be fair, i will not expand on all the possible ways to exploit it
besides than the mention of `SOP`, plus as stated by the authors:

> We wanted to focus on more important parts of BEAST such as the actual
> crypto attack and optimizations, so we stopped looking for
> alternatives, and used the SOP vulnerability to make an agent.

Besides than the browser vulnerabilties, the exploitation is thanks to
how `TLS` handles communication, where each packet sent requires an
specific format.

For example,

<div class="imgblock">

!["HTTP Format sample"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331048/blog/release-the-beast/http-request_qrmgpg.webp)

<div class="title">

Figure 12. HTTP Request format sample

</div>

</div>

As we can observe there are values an attacker cannot easily guess, but
there a lot of parameters which can be predicted, just by knowing the
format of an [HTTP
request](http://www.tcpipguide.com/free/t_HTTPRequestMessageFormat.htm).

What if the last parameters is a password field within its value? Or
what if the attacker can predict which block contains cookies?

When the attacker has predicted it, it can act in two ways:

1. Reassure that certain block has what predicted or not.

2. Determine the value of the block. Notice, that this values on the
    stream ranges from 256 characters in ASCII, plus 8 bytes per block,
    which means 256<sup>8</sup> possibilities.\
    Of course fewer, if special characters are removed and other
    advanced mechanisms are used, which are out of the scope here.

## Attack requeriments

Although this attack seems dangerous, it only works when the following
requeriments are met:

1. `JavaScript` enabled in browser.

2. Encryption using `SSL 3.0` or `TLS 1.0`.

3. Able to packet capture communications.

4. Able to modify packets sent from you.

5. Browsing with multiple tabs/sessions.

6. Attacker must have an idea where you are going to browse.

7. Attacker must be able to perform their action(s) within the time you
    are logged in.

## Conclusion

Again, although it was dangerous, when both researchers found it and
spend several weeks on demonstrating the attack they informed browser
vendors and TLS devs about such vulnerability, no harm was done. Sadly,
they never released their code nor an official paper describing each
phase of the attack.

At least it is unknown if somebody before them took advantage of it.

## References

1. [CommandLine (2014). An Illustrated Guide to the BEAST
    Attack](http://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art027)

2. [J. Orlin Grabbe. The DES Algorithm
    Illustrated](http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm)

3. [Block cipher mode
    (CBC)](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)

4. [Block cipher](https://en.wikipedia.org/wiki/Block_cipher)

5. [Gregory V. Bard (2014). A Challenging but feasible
    Blockwise-Adaptive Chosen-Plaintext Attack on
    SSL](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.61.5887&rep=rep1&type=pdf)
