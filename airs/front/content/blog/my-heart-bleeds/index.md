---
slug: my-heart-bleeds/
title: My Heart Bleeds (But Not for You)
date: 2018-04-25
subtitle: Understanding the flaw behind Heartbleed
category: attacks
tags: vulnerability, bug, openssl
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330940/blog/my-heart-bleeds/cover_qf1nze.webp
alt: Computer showing a pirate flag
description: Here we talk about Heartbleed, the result of a buggy
  implementation of the TLS protocol on OpenSSL, which was tempted
  to be a severe threat to private data.
keywords: TLS, HeartBeat, HeartBleed, OpenSSL, Vulnerability, Bug,
  Ethical Hacking, Pentesting
author: Daniel Yepes
writer: cestmoi
name: Daniel Yepes
about1: '"If the doors of perception were cleansed everything would appear
  to man as it is, Infinite." William Blake.'
source: https://unsplash.com/photos/JJPqavJBy_k
---

Back in April 2014, one of the biggest vulnerabilities in recent history
was found: [`HeartBleed`](http://heartbleed.com/). The popular open
source cryptographic software library
[`OpenSSL`](https://www.openssl.org/), had a [critical
flaw](https://www.openssl.org/news/secadv/20140407.txt),
[<sup>\[1\]</sup>](#r1) in the implementation of a extension on the
Transport Layer Security `(TLS)` protocol.

The wide use of `OpenSSL` on several services such as **web**,
**email**, **instant messaging `(IM)`**, even **virtual private networks
`(VPNs)`**, [managed to affect
**17%**](http://apac.trendmicro.com/apac/security/heartbleed/index.html)
of all `SSL` servers, mostly **half a million** of trusted websites.

In this article we will see how it works, in a simple yet technical
language.

<div class="imgblock">

!["Heartbleed"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330939/blog/my-heart-bleeds/heartbleedxkcd_ycopyf.webp)

<div class="title">

Figure 1. xkcd Heartbleed

</div>

</div>

## TLS Protocol brief explanation

`TLS` protocol aims to provide **secure** communications between
**servers** and **web browsers**. Whenever you see in your web browser a
<span class="green"> green lock </span> next to the url, it means you
are visiting a secure website, indicating that your communication with
the website is **encrypted**, specially designed
to prevent <span class="red"> eavesdropping </span>
and <span class="red"> tampering</span>.

<div class="imgblock">

!["Green lock provided by TLS"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330938/blog/my-heart-bleeds/green-lock_z2mz3r.webp)

<div class="title">

Figure 2. Secure URL, Green lock sample

</div>

</div>

`TLS` accomplishes that by **encoding** your **data** in a way that only
the recipient knows how to **decode** it. If a third party is listening
to the conversation, it will only see seemingly a random string of
characters, not the **actual** message or **content** of your data.

## From Beat to Bleed

The **`HearBeat` extension** was a change proposed by [`Dr.
Seggelman`](https://www.robin-seggelmann.de/) in 2012, and the bug was
fully disclosed on April 7, 2014, by independent researchers at
`Codenomicon` and `Google Security`. According to the
[`RFC-6520`](https://tools.ietf.org/html/rfc6520), it’s a new extension
implemented over `TLS/DTLS`, which provides a way to perform a
**keep-alive** functionally.

Basically, a device sends an **echo** with a **message** to be **replied
back** with the **same information**, just to make sure if the other
device is **still alive**. If any of them goes down during the
transaction, the other will know it by using this `HearBeat` mechanism,
[<sup>\[2\]</sup>](#r2).

So, for example, you are reading this article, but you haven’t done
anything in a while, your web browser sends a message to the server
saying **"Hello - Repeat it back to me"**, the server receive it and
send it back to your browser.

## The bleeding flaw

Researchers found that if a **request** made had a **bigger length**
than what was **sent** on the message, **extra information** could be
<span class="red"> leaked </span> at the response sent back.

For example, the web browser sends the following message:
**"Hello - Repeat it back to me (28 kB)"**

But the length of the request is modified to **40 kB**, then it
becomes:
**"Hello - Repeat it back to me (40 kB)"**

Then the message is sent and the recipient device gets a message with a
length of **40 kB**.

But the message was suposed to be **28 kB** long, what about the
remaining **12 kB**? The recipient machine allocates in memory buffer
those extra **12 kB** of data and send back **28 kB** of the actual
message plus extra **12 kB** of whatever is stored in **RAM**.
Practically, you get more than the **beat**, instead, you can actually
make it <span class="red"> bleed</span>, literally.

<div class="imgblock">

!["Bad luck HeartBleed"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330939/blog/my-heart-bleeds/heartbleed-meme_n7nt5j.webp)

<div class="title">

Figure 3. Bad luck

</div>

</div>

Why? You may ask. The message can be up to **64 kB**, not a lot of
information leaked though, just **65536** characters taken from no other
place than **RAM**, but it’s **not** like if an attacker could
**control** which **portion** of the **RAM** wants, it just get whatever
the machine grabs in the subsequent block of memory.

But that doesn’t seem to be harmful, probably no more than random data
being sent, what’s the chance it can get something of real value? What
if I told you an attacker doesn’t have **any limit** to send
`HeartBeats`? It can stay **all day** long sending **requests**
analyzing each **64 kB** sent back and forth, and suddenly, the flaw
could yield some, if not all of the following:

- `SSL` private keys.

- Usernames and passwords that are submitted to applications and
  services running on the server.

- `Session tokens` and `cookie` values.

The worst of this vulnerability, is that there’s **no** way to **trace**
it, records for this kind of activity aren’t **logged** by the `OpenSSL`
daemon. Plus it’s not a client-server vulnerability, as malicious
**servers** were able to **exploit** it on **clients** using the
vulnerable version of `OpenSSL`, called a **Reversed HeartBleed's**.

<div class="imgblock">

!["Heartbleed"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330939/blog/my-heart-bleeds/heartbleed-explanation_csomni.webp)

<div class="title">

Figure 4. xkcd Heartbleed explanation

</div>

</div>
<div class="imgblock">

## What caused the bug?

This is a portion of the [code of the `OpenSSL`
library](https://git.openssl.org/gitweb/?p=openssl.git;a=blob;f=ssl/t1_lib.c;h=a2e2475d136f33fa26958fd192b8ace158c4899d#l3969)

- `v1.0.1f` (the vulnerable version). This fragment contains the bug and
  I’m gonna break it in the essentials details.

\+ .Fragment of the t1\_lib.c from `OpenSSL`.

``` c
tls1_process_heartbeat(SSL *s)
3966  {
3967  unsigned char *p = &s->s3->rrec.data[0], *pl;
3968  unsigned short hbtype;
3969  unsigned int payload;
3970  unsigned int padding = 16; /* Use minimum padding */
3971
3972  /* Read type and payload length first */
3973  hbtype = *p++;
3974  n2s(p, payload);
3975  pl = p;
3976
3977  if (s->msg_callback)
3978    s->msg_callback(0, s->version, TLS1_RT_HEARTBEAT,
3979      &s->s3->rrec.data[0], s->s3->rrec.length,
3980      s, s->msg_callback_arg);
3981
3982    if (hbtype == TLS1_HB_REQUEST)
3983    {
3984      unsigned char *buffer, *bp;
3985      int r;
3986
3987      /* Allocate memory for the response, size is 1 bytes
3988      * message type, plus 2 bytes payload length, plus
3989      * payload, plus padding
3990      */
3991      buffer = OPENSSL_malloc(1 + 2 + payload + padding);
3992      bp = buffer;
3993
3994      /* Enter response type, length and copy payload */
3995      bp++ = TLS1_HB_RESPONSE;
3996      s2n(payload, bp);
3997      memcpy(bp, pl, payload);
3998      bp += payload;
3999      /* Random padding */
4000      RAND_pseudo_bytes(bp, padding);
```

The line responsible for the vulnerability is this one:

\+

``` c
3997      memcpy(bp, pl, payload);
```

Looking at the documentation of
[`memcpy`](https://linux.die.net/man/3/memcpy), we see the following:

<div class="imgblock">

!["memcpy linux man page"](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330940/blog/my-heart-bleeds/memcpy_h7niiu.webp)

<div class="title">

Figure 5. memcpy function

</div>

</div>

The terms in parentheses behave like this: **bp** is the destination of
the memory copied from **pl**, **pl** is the source of that memory and
**payload** is the length of it, basically, the last one says how large
is the data.
If **payload** states that **pl** is of **64 kB**, when it really is of
**0 kB** we got a huge problem, because **bp** will be created with the
same size as **pl**, filled of garbage data, but then none of that data
at **bp** gets overwritten, because **pl** is empty or isn’t large
enough to fill it.

The **flaw** on the code is that the **length** of the **data** wasn’t
being validated, there were a **missing bounds** check before memcpy was
performed. We’ll see that in the following lines of code:

\+

``` c
/* Read type and payload length first */
3972         /* Read type and payload length first */
3973         hbtype = *p++;
3974         n2s(p, payload);
3975         pl = p;
```

The previous three lines of code just write the length of **p**, the
'\`HeartBeat\` request', into the variable **payload**, the **expected
length** of the payload. But notice there’s nothing checking if the
**expected length** of the message corresponds to the actual length of
the '\`HeartBeat\` request'.

The next line is responsible to set the **length** of the response back,
the **payload** variable holds the **expected length** of the
**payload**, thus that length will be written into the **bp** variable.

``` c
3996      s2n(payload, bp);
```

Now, the line containing the vulnerability explained before, takes a
little more sense, **pl** could have a length of **5 kB**, but
**payload** gets a value of **64 kB**, as it is not checked, **bp**
variable will allocate in memory those **64 kB** and send it just back,
[<sup>\[2\]</sup>](#r2).

``` c
3997      memcpy(bp, pl, payload);
```

### The fix

The vulnerability is only present in versions `1.0.1` until `1.0.1f` and
`1.0.2-beta` until `1.0.2-beta1` releases. A few days after the incident
a patch was released, the `OpenSSL` versions `1.0.1g` and `1.0.2-beta2`,
got rid of the flaw.

The **patch** is essentially a **bounds check**, to validate the actual
**length** of the **payload**.

``` c
hbtype = *p++;
n2s(p, payload);
if (1 + 2 + payload + 16 > s->s3->rrec.length)
return 0; /* silently discard per RFC 6520 sec. 4 */
pl = p;
```

The fully code patched can be seen here in this [`git
diff`](https://git.openssl.org/gitweb/?p=openssl.git;a=commitdiff;h=731f431497f463f3a2a97236fe0187b11c44aead).

This kind of vulnerability is named `buffer over-read`,
[<sup>\[3\]</sup>](#r3). For example, in the `Heartbleed` case, the
program tries to read data from memory, but due to no bounds check, it
tries to read adjacent memory, creating a special case of memory safety
violation.

### That was all?

Yes\! That single line you saw there was the demonic 'call of Cthulhu'.

Nah, not really like that, but it tempted to wreak havoc, several
companies like
[`Amazon`](https://aws.amazon.com/es/blogs/security/aws-security-and-cve-2014-0160-heartbleed/),
[`SoundCloud`](https://blog.soundcloud.com/tag/heartbleed/),
[`BitBucket`](https://community.atlassian.com/t5/Questions/Heartbleed-Serious-OpenSSL-vulnerability/qaq-p/94964),
[`Github`](https://blog.github.com/2014-04-08-security-heartbleed-vulnerability/),
the [Canada Revenue Agency
`(CRA)`](http://business.financialpost.com/personal-finance/taxes/cra-website-shutdown-security),
almost 78 devices from [`Cisco
Systems`](https://blogs.cisco.com/security/openssl-heartbleed-vulnerability-cve-2014-0160-cisco-products-and-mitigations),
[`Hewlett-Packard`](http://www8.hp.com/us/en/heartbleed.html), even
operating systems shipped with it, like [`Debian
Wheezy`](https://www.debian.org/security/2014/dsa-2896),
[`CentOS 6.5`](https://wiki.centos.org/Security/Heartbleed),
[`Ubuntu 12.04.4 LTS`](https://usn.ubuntu.com/2165-1/), and a big
etcetera had to shut online their services, warn or log out every user
and inform them to update their password, there were even possible cases
of the bug
[`exploited`](https://www.securityweek.com/hackers-exploited-heartbleed-bug-steal-45-million-patient-records-report).

Yet, despite 4 years have passed, there’s a high chance that a lot of
services are
[unpatched](https://www.theregister.co.uk/2017/01/23/heartbleed_2017/)
against `HeartBleed`, since there are plenty reports from 2017 showing
that at least 200,000 services are still
[affected](https://www.theregister.co.uk/2017/01/23/heartbleed_2017/).

## References

1. [Synopsys (2014).](https://heartbleed.com)

2. IBM (2014). A technical view of the OpenSSL HeartBleed
    vulnerability.

3. [CVE-2014-0160.](https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2014-0160)
