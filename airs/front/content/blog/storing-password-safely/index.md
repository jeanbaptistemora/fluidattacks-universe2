---
slug: storing-password-safely/
title: Storing Passwords Safely
date: 2017-01-02
category: challenges
subtitle: Solving Yashira hash challenge 3
tags: password, security, challenge
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331103/blog/storing-password-safely/cover_qrhopx.webp
alt: Code with hashed data on the side
description: Hash algorithms can be cracked using huge databases with hashed
  common words. It's essential to know how to properly secure your
  data before storing it.
keywords: Hash, Security, Password, SHA , MD5, HMAC, Ethical Hacking,
  Pentesting
author: Jonathan Armas
writer: johna
name: Jonathan Armas
about1: Computer Engineer, Security+
about2: '"Be formless, shapeless like water" Bruce Lee'
source: https://unsplash.com/photos/zvHhKiVuR9M
---

By the end of the year, we witnessed a huge increase in the amount of
attacks that extracted large quantities of personal information, emails
and passwords. Even one of the biggest email services, Yahoo, suffered
an attack by cyber-criminals and they robbed more than 500000 accounts,
in doing so, accessing to everyone’s passwords. One of the most common
methods of storing passwords on rest is hashing, it’s a mathematical
function that transforms data into a fixed-length value or key that
represents the original data.

You can use hashing algorithms to reinforce integrity and also to store
passwords, as long as the data never changes. The resulting hash will
always be the same. By comparing hashes created at two different times
you can determine if the original data is still the same. Passwords are
often stored as hashes, when a user creates a new password, the system
calculates the hash and stores it. Later, when a user logs-in, the
system calculates the hash of the password entered and compare it with
the one stored, if it is the same then the person entered the correct
password. The most common hashing algorithms are MD5 (Message Digest 5),
SHA (Secure Hash Algorithm) and HMAC (Hash-based Message Authentication
Code).

However, hashing has a vulnerability, rainbow tables. Which are huge
databases of precomputed hashes, and it helps crackers to discover
passwords comparing thehash of a stolen password with the database. Some
of these tables are bigger that 160 GB in size, and they include hashes
for almost every possible combination of characters.

## Challenge Yashira Hash 3

In this challenge, they give us a hash that needs to be cracked, and
then answered it with the password on clear text.

<div class="imgblock">

![reto](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331102/blog/storing-password-safely/reto_my4yzp.webp)

<div class="title">

Figure 1. Challenge on
[Yashira](http://www.yashira.org/index.php?mode=Retos&resp=inforeto&level=3)

</div>

</div>

We could use a rainbow table to crack this hash but it will need a huge
database or an algorithm that uses every hash and password to compare.
On the contrary, we could use [crackstation](https://crackstation.net/)
to do this task. It only needs the hash and the site cracks it with its
own database.

<div class="imgblock">

![crackstation](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331101/blog/storing-password-safely/crackstation_xfn4yc.webp)

<div class="title">

Figure 2. crackstation hashing solver

</div>

</div>

It then discovers the clear text password of the hash given, telling us
that it is SHA1. It uses colors to indicate if the search was
successful, if a partial a partial match was found or if no password was
found at all

<div class="imgblock">

![solved](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331102/blog/storing-password-safely/solved_vookhd.webp)

<div class="title">

Figure 3. Solution given by crackstation

</div>

</div>

To protect against these types of attacks, developers and systems
administrators should add security measures additional to hash such as
salt. Salting passwords prevent rainbow table attacks adding a set of
random data at the end of the password before hashing it. These
additional characters add complexity to the password and cause that
password attacks that compare hashes to fail. Some of the common methods
of salting are Bcrypt and PBKDF2 (Password-Based Key Derivation Function
2).
