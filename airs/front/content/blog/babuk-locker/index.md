---
slug: babuk-locker/
title: Babuk Locker for the 2021
date: 2021-01-14
subtitle: The first ransomware (as a gift) for this new year
category: attacks
tags: software, security, vulnerability, hacking, mistake
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330676/blog/babuk-locker/cover_dy5uwm.webp
alt: Photo by Guido Hofmann on Unsplash
description: Here's a post dedicated to the new form of ransomware,
  Babuk Locker. I mention its encryption scheme, its injection,
  operation, and other basic things about it.
keywords: Ransomware, Babuk, Locker, Software, Security, Vulnerability,
  Hacking, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/iu6OOcloLvY
---

A new form of [ransomware](../ransomware/) has emerged to welcome the
new year, **2021**. We’re referring to the **Babuk Locker**. A malicious
software that is capable of encrypting some of your essential files to
deny you access to them, and for which you should pay a ransom. [Chuong
Dong](http://chuongdong.com), a Computer Science student at [Georgia
Tech](https://www.gatech.edu/) interested in cybersecurity, [reported it
on
January 3rd, 2021](http://chuongdong.com/reverse%20engineering/2021/01/03/BabukRansomware/).
(It seems that Dong saw Babuk mentioned in a tweet by
[Arkbird](https://twitter.com/Arkbird_SOLG) and, linked to it, finishing
this post, I found an earlier [article in Russian by
Amigo-A](https://id-ransomware.blogspot.com/2021/01/babuk-ransomware.html)
published on January 1st, 2021.)

According to Dong, this malware has not been obfuscated ([malware
obfuscation](https://securityboulevard.com/2020/02/what-is-malware-obfuscation/)
makes the data or code difficult to understand) and is quite 'standard,'
even amateurish in coding. Besides, it uses "techniques we see such as
multi-threading encryption as well as abusing the Windows Restart
Manager similar to Conti and REvil" (other forms of ransomware).
However, this ransomware’s encryption scheme allows it to stand out,
being enough to prevent victims from recovering their systems and files
efficiently and for free.

<div class="imgblock">

![January](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330673/blog/babuk-locker/january_x6we4g.webp)

<div class="title">

Figure 1. Photo by Glen Carrie on [Unsplash](https://unsplash.com/photos/TGeFx4x4NHU).

</div>

</div>

## Babuk Locker’s encryption scheme

The robust encryption scheme of Babuk Locker, as stated by Dong,
includes "SHA256 hashing, ChaCha8 encryption, and Elliptic-curve
Diffie-Hellman (ECDH) key generation and exchange algorithm."
[SHA256](https://xorbin.com/tools/sha256-hash-calculator) (SHA: Secure
Hash Algorithm) is dedicated to generating a 256-bit (32-byte) hash
value (we already saw what a *hash* is in [my first post on `Fluid
Attacks'` blog](../pass-cracking/)). ChaCha8, on the other hand, is a
[stream cipher](https://en.wikipedia.org/wiki/Stream_cipher), a better
variant of [Salsa20](https://en.wikipedia.org/wiki/Salsa20). These
ciphers —both developed by professor [Daniel J.
Bernstein](https://en.wikipedia.org/wiki/Daniel_J._Bernstein)— encrypt
plaintext messages (every bit of the message is encrypted one by one) by
applying an algorithm with a pseudorandom cipher digit stream or a
keystream. Finally, ECDH constitutes ["a key
agreement](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman)
protocol that allows two parties, each having an elliptic-curve
public-private key pair, to establish a shared secret over an insecure
channel." Undoubtedly, for many of us, it is sufficient with this
information instead of going into encryption details. Let’s keep an
overview of this ransomware currently occupying our attention.

## Babuk Locker’s injection and operation

Babuk Locker appears as a 32-bit *.exe* file (i.e.,
"[BABUK.exe](https://id-ransomware.blogspot.com/2021/01/babuk-ransomware.html)",
at least at first), but, as reported by [O’Donnell in
Threatpost](https://threatpost.com/ransomware-babuk-locker-large-corporations/162836/),
it is not clear how this malware "is initially spread to victims." It
seems, though, that the vehicle of infection, in this case, may not be
far from the typical [phishing](../phishing/) "similar to other
ransomware groups' approaches," said Dong. Indeed, for his part,
[Brendan Smith in Howtofix](https://howtofix.guide/babuk-locker/) talks
about *only two* forms of Babuk injection: email spam and trojans.

When the threat actors launch Babuk Locker, they can employ "a
command-line argument to control how the ransomware should encrypt
network shares and whether they should be encrypted before the local
file system," notes [Abrams in
BleepingComputer](https://www.bleepingcomputer.com/news/security/babuk-locker-is-the-first-new-enterprise-ransomware-of-2021/).
Babuk, following an assigned list, can close or terminate a wide variety
of Windows support services (e.g., system-monitoring services) and
running processes (e.g., Office apps, mail servers, and web browsers)
before encryption. Snuffing out these services and processes is
something necessary for successful encryption by the malware.
Additionally, Babuk tries to remove [shadow
copies](https://en.wikipedia.org/wiki/Shadow_Copy) (i.e., backup copies
or snapshots of files or volumes) before and after the encryption.

As Abrams also points out, "When encrypting files, Babuk Locker \[uses\]
a hardcoded extension and \[appends\] it to each encrypted file." The
specific extension currently used is "**.\_\_NIST\_K571\_\_**". So, for
example, if you have a file with the name "summary\_2020.docx", it is
transformed into "summary\_2020.docx.\_\_NIST\_K571\_\_". Also, a ransom
note named *How To Restore Your Files.txt* (see Figure 2) appears in the
folders containing encrypted files. It shows general information about
the attack and instructions to follow for recovering data, including a
link to a [Tor](https://www.torproject.org/) page (remember the *.onion*
domains we talked about [a few weeks ago](../dark-web/)) to establish
negotiation.

<div class="imgblock">

![RansomNote](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330670/blog/babuk-locker/ransomnote_cinngo.webp)

<div class="title">

Figure 2. Image taken from [chuongdong.com](http://chuongdong.com/uploads/RansomNote.PNG).

</div>

</div>

In addition, the ransomware operators can reveal the victims' names in
their notes and demonstrate through images that they have stolen
unencrypted files with data that they could expose (leak) on the Dark
Web, specifically on a hacker forum, in case no agreement is reached. It
seems that the subjects behind this Babuk Locker project do not
currently have their own leak site (that could be launched soon, says
Abrams). So, for now, they only resort to the forum to publish stolen
data.

When both parties are chatting on the Tor site, the criminals start with
two questions: "Are you a recovery company?" and "Do you have insurance
against ransomware programs?" Then, before discussing prices, they ask
the victim for some files (less than **10MB**) he/she wants to recover
and subsequently request the *ecdh\_pub\_k.bin* file, where they can get
the victims' public ECDH key that allows them to perform the decryption
test. By this, they perhaps intend to demonstrate that this is a serious
matter and that they are the party who calls the shots.

## You should be aware of Babuk Locker

Babuk Locker has already affected some companies (mainly manufacturers)
'worldwide,' which seemingly you could count on the fingers of one hand.
(Reviewing the article by Amigo-A, this ransomware had already shown
activity since last December, and it appears that the first known victim
was an Italian company.) Babuk operators have established a pay range
for the systems' release between **$60,000** and **$85,000** in Bitcoin.
In fact, it was this higher value that one of the victim companies
apparently agreed to pay, being the only one that has decided to do so,
at least as reported until last week.

Based on O’Donnell’s words, the number of ransomware attacks continues
to grow, "jumping by 350 percent since 2018." One of the most affected
has been the healthcare sector, and how could it not be, when, amid a
COVID-19 pandemic, its work has increased considerably, and its workers
may show difficulties in concentration. The latter is a factor that many
cybercriminals exploit nowadays. They send emails with files that some
of your employees or coworkers may not think twice before opening. Babuk
Locker, the 32-bit *.exe* file, is another ransomware to add to the
list, and everyone in your company should be aware of it\!

I hope you have enjoyed this post and remind you that we’re looking
forward to hearing from you here at `Fluid Attacks`. [Do get in touch
with us\!](../../contact-us/)
