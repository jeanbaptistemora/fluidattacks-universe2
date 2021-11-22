---
slug: pass-cracking/
title: Caution! Your Password Can Be Mine
date: 2020-01-17
subtitle: A very short introduction to password cracking
category: attacks
tags: password, security, vulnerability, hacking, mistake
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330973/blog/pass-cracking/cover_wslpjd.webp
alt: Photo by Arteum.ro on Unsplash
description: After I wrote this post, I decided to change some of my most
  important passwords, and after you read it, we think you might want
  to modify your passwords too.
keywords: Password, Cracking, Security, Vulnerability, Hacking, Dictionary,
  Brute Force, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/7H41oiADqqg
---

Passwords are currently the most popular authentication method in
computer systems and `IT`, and can serve as protection of our private
information in email and bank accounts, social networks, and many other
apps.

If someone obtains your passwords, for example, you could lose important
information or even lose a considerable amount of money. And, believe or
not —while it’s true that some applications disregard security
measures—, the fault is partly *yours\!*

<div class="imgblock">

![WTF](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330972/blog/pass-cracking/wtf_mofm5i.webp)

<div class="title">

Figure 1. Photo by [Bernard Hermant](https://unsplash.com/@bernardhermant) on Unsplash

</div>

</div>

Before we talk about **password cracking**, keep this in mind, there are
some different ways to store passwords on systems:

- The *plaintext* method is to store the password identically as
  entered.

- The *encryption* method combines the password with another secret
  key; it’s like storing the password protected by another one.

- The *hashing* method depends on a complex formula that modifies
  plaintext and produces a hash. Let’s talk about it.

## Hashes

Let’s say that we’ve created a password for our email account, and that
password is 'December' (brilliant, right?). This set of characters is
our plaintext, the input for the hashing method. This method employs a
cryptographic hash function —a one-way mathematical operation— and gives
us a hash as an output.

*But what is a **hash**?* It’s a fixed-lenght ciphertext, and an
arbitrary block of data. Look at this image:

<div class="imgblock">

![MD5](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330971/blog/pass-cracking/md5_ptpf4y.webp)

<div class="title">

Figure 2. Using [MD5](http://md5-hash-online.waraxe.us/) to get a hash

</div>

</div>

*And what does **one-way** mean?* Well, you can’t easily go back to the
plaintext (just reverse the formula) having only the hash.

Thus, with a specific plaintext, using a particular hash function, we
get just one specific hash, not two, the same each time. Further, the
same hash is *never* produced by two different inputs
([although…​](https://crypto.stackexchange.com/questions/1434/are-there-two-known-strings-which-have-the-same-md5-hash-value)),
and minimal changes in inputs generate substantial alterations in
outputs.

So, for our email account employing the password 'December' the hash
value is stored. When we log in again, the system will use the hash
function, and the output will be compared with the stored hash value.
Our authentication will be successful if those hash values are equal.

It’s in relation to those hashes that, in general terms, we describe the
password cracking.

## Password Cracking

Password cracking is based on the use of different techniques and tools
to guess passwords. Sometimes it can be used to recover lost passwords
or to test users' passwords within an organization but most commonly it
can operate as an **illicit activity**.

In this process, employing a cracking software, we take the possible
strings of characters and, with the hashing algorithm used for the
password, convert them into hashes. Then we compare them with the hash
that corresponds to the password.

Password cracking can be done both *online* and *offline*.

Online attacks take place with the constant protection of the system
attacked, and use its login mechanisms, that’s why they’re easy to
detect. After some failed attempts, the game is over for the cracker,
and the account is locked up.

Offline attacks depend primarily on someone’s ability to break system
security and obtain sets of hashes from databases. While there’s no
active defense, attackers can try with as many passwords as they want
and as long as they think necessary.

Here are some of the best-known methods:

### Brute Force

<div class="imgblock">

![Brute Force](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330972/blog/pass-cracking/bf_fwytnv.webp)

<div class="title">

Figure 3. Photo by [Olga Guryanova](https://unsplash.com/@designer4u) on Unsplash

</div>

</div>

Brute force (`BF`) attack, since the early 1990s, has been an exhaustive
method that takes for evaluation all possible combinations of characters
that can be part of the password to be found. `BF` can become difficult
and tedious considering the size of the search space and the time it
would take the system according to its processing power.

In summary, the attacker must guide the system to a one-by-one
comparison of hashes, testing millions of passwords, and that’s why this
option is not the best when time is short. Although it is recognized
that today’s advanced fast processors, and supplementary probability
methods, give an advantage to this meticulous technique.

### Dictionary

<div class="imgblock">

![Dictionary](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330972/blog/pass-cracking/dct_r1wei0.webp)

<div class="title">

Figure 4. Photo by [Pisit Heng](https://unsplash.com/@pisitheng) on Unsplash

</div>

</div>

Dictionary attacks use prearranged wordlists with fewer words than an
input space for `BF` attacks, which means less time spent but also the
possibility of not having the password searched. Lines of characters are
grabbed sequentially for subsequent processes of hashing and comparison
of values. Some wordlists are available online, constructed,
distributed, and updated by multiple attackers, and sometimes are
adapted for specials targets.

In addition to look for whole-words in passwords, crackers also search
for other patterns such as character substitutions (e.g., p@55word) and
additions (e.g., PassWord123), and predictable compositions and
distributions besides fashionable passwords.

### Other methods

Mixing `BF` with the dictionary attack we would get a *hybrid* attack,
that means, using a wordlist as a base to then take each entry and check
for some possible permutations (e.g., adding prefixes or suffixes).

We can also have *Rainbow tables*. Instead of using words it directly
employs hashes. So, the time required for computing the hash is saved,
but this technique needs large storage space (although powerful
compression schemes have been reported) and, besides, if you have to
create the table, well, that’s a lot of time. Websites like
[RainbowCrack](http://project-rainbowcrack.com/) can help with some of
those files.

As a next step for advancing in password cracking, and related with the
computing resources, there’s the `GPU`-based cracking (with a
performance 5-20 times that of `CPU`). This allows us to make massively
parallel calculations, increasing significantly the speed to complete an
attack.

### Tools

Hoping you’re not interested in password cracking for malevolent
purposes, here’s a list with some cracking software:

- [Cain and Abel](https://softfamous.com/cain-abel/)

- [Hashcat](http://hashcat.net/oclhashcat-plus/)

- [John the Ripper](http://www.openwall.com/john/)

- [L0phtCrack](https://www.l0phtcrack.com/)

- [Ophcrack](https://ophcrack.sourceforge.io/)

## Check your passwords

At `Fluid Attacks` we’re interested in `IT` security, and as [Julian
Arango](../do-not-read/) said once:

> "we know that information security is more than just focusing on
> software and `IT` infrastructure: it is about how we behave".

Hence, consider the following recommendations:

Being aware of the threat of password cracking is a good way to start to
make rational decisions, and to protect your personal information. As a
user, you can now be more cautious with your passwords, making them
stronger, to avoid that crackers take power over them in short time and
with little effort.

Specifically, try to be less predictable when choosing the elements that
constitute a password. You can substitute some letters with numbers and
add special characters, arbitrarily capitalize some letters, and make
the words longer and random enough. Don’t reuse passwords and make them
unique, change them every few months, and practice them enough to avoid
problems remembering.

Don’t forget that even if you’re not a 'big fish', you’re also a
potential victim, and *your password can be mine\!*
