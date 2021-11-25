---
slug: trapdoors/
title: Don't Let the Cat Out!
date: 2019-01-08
subtitle: Trapdoor functions and their importance in security
category: math
tags: encryption, math, security
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331107/blog/trapdoors/cover_p6rsfq.webp
alt: Cats in a forest
description: This blog post is an overview of the mathematical
  concept 'Trapdoor,' the basis of information security.
keywords: Trapdoor, AES, Asymmetric, Encryption, Math, Symmetric, RSA,
  Ethical Hacking, Pentesting
author: Sebastian Villalobos
writer: sevilla
name: Sebastian Villalobos
about1: Electronic Engineer
about2: Programming, Electronics, Math
source: https://unsplash.com/photos/LMnk4WPwo-w
---

Functions\! I’m sure you have heard this concept in many ways: math,
programming, economics, etc. And they all can be reduced to the same
basic thing: something that takes some inputs and produces some outputs.
Math is the case here, however, there is a lot to add to that short
definition, specially when we apply it to computer security, because
despite you might be unaware, your security totally depend on a special
kind of functions called `Trapdoors`. [<sup>\[1\]</sup>](#r1%20) Let’s
talk about trapdoor functions and how they save you from "letting the
cat out".

When we talk about inputs producing an output we usually talk about the
reverse process: given the outputs deduce the inputs, this is really
useful in many applications…​ but not in security\! knowing an input
from an output is a serious problem, you will see why.

A `Trapdoor` is essentially something taking an input and producing an
output, but it is extremely difficult to do the reverse process, this is
because to do so you need to know a "secret" called a private key and
you have to be the luckiest guy in all universes to guess it or to guess
the input.

Suppose:

|                                                                                          |
| ---------------------------------------------------------------------------------------- |
| <p> **P** : Plain text data <br /> **E** : Encrypted data <br /> **K** : Secret key </p> |

A `Trapdoor` is a function that encrypts with the properties:

|                                                                                                                                                      |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p> **E** = f(**P**) (Easy to do) <br /> **P** = f<sup>-1</sup>(**E**) (Really hard to do!) <br /> **P** = f<sup>-1</sup>(**E,K**) (Easy to do) </p> |

Now, `Trapdoors` are not the same as the well known hash functions, hash
functions are one-way functions as well, but they are not reversible by
any means, whereas `Trapdoors` are reversible with the key. This is what
makes them fundamental for `Encryption` of shared information.

Your lifesaving, precious data is always put in a `Trapdoor`, encrypted
and transmitted and no one (except the possessor of the secret and the
luckiest guy in all universes) can figure out the data.

## Symmetric and Asymmetric Encryption

When two ends have to exchange sensitive data, they must agree on the
key they both use, this is called `Symmetric Encryption`
[<sup>\[2\]</sup>](#r2) where the same key is used to encrypt and to
decrypt. This key has to be transmitted first for agreement before any
other communication, but how can they prevent a third party sniffs and
retrieve the key? they use a type of `Encryption` called `Asymmetric
Encryption`: It encrypts the data with one public key and decrypts it
with a different private key

|                                                                               |
| ----------------------------------------------------------------------------- |
| <p> **K<sub>p</sub>** : Public key<br /> **K<sub>s</sub>** : Private key </p> |

The data is encrypted with

|                                             |
| ------------------------------------------- |
| <p> **E** = f(**P**,**K<sub>p</sub>**) </p> |

And decrypted with

|                                                          |
| -------------------------------------------------------- |
| <p> **P** = f<sup>-1</sup>(**E**,**K<sub>p</sub>**) </p> |

This `Encryption` is slow and it’s not commonly used in data
transmission. It’s only used between parties to agree on a shared key
that they use for `Symmetric Encryption` which is the one used for large
data exchange as it’s faster. The shared key for `Symmetric Encryption`
is transmitted over `Asymmetric Encryption` so no attacker can retrieve
this symmetric key.

## RSA Encryption

Rivest, Shamir, Adleman, also know as `RSA` algorithm
[<sup>\[3\]</sup>](#r3%20) is the most common algorithm for `Asymmetric
Encryption` and it’s based on a `Trapdoor` function called *modular
exponentiation* :

|                                                                  |
| ---------------------------------------------------------------- |
| <p> **E** = **P**<sup>**K**<sub>**P**</sub></sup> mod **N** </p> |

In this case knowing **P** from **E** is impossible, you need to know a
secret **K**<sub>**S**</sub> in order to compute it.

`RSA` algorithm uses prime number arithmetics and modular exponentiation
to encrypt a message, the algorithm can be summarized like this :

1. Choose two prime numbers ***p*** and ***q***.

2. Compute ***n*** = ***pq***.

3. Compute Euler’s function ***ϕ*** = (***p* - 1**)(***q* - 1**).
    [<sup>\[5\]</sup>](#r5%20)

4. Choose a number ***e*** smaller and *coprime*
    [<sup>\[6\]</sup>](#r6%20) to ***ϕ***.

5. Choose a number ***d*** such that (***ed* - 1**) mod ***ϕ* = 0**,
    This is know as the *modular multiplicative
    inverse*,[<sup>\[7\]</sup>](#r7%20) in other words, ***ed* - 1**
    must be divisible entirely by ***ϕ***.

6. (***e***,***n***) are the public key whereas (***s***,***n***) are
    the private key.

A message ***m*** is encrypted into ***c*** by

|                                                          |
| -------------------------------------------------------- |
| <p> ***c*** = ***m***<sup>***e***</sup> mod ***n*** </p> |

And decrypted by

|                                                            |
| ---------------------------------------------------------- |
| <p> ***m*** = ***c***<sup>***d***</sup> mod ***n*** </supmod> |

Thus, anyone can know the public key value ***e*** to encrypt but not
the private key value ***d*** used to decrypt. What about ***n*** ?
could not they use it to come up with ***d*** ? Yes, they can, they will
just take tenths of years to do it as ***n*** is chosen to be a very big
number, so breaking it into the prime factors ***p***, ***q*** used to
get ***e*** and therefore ***d***, would take long enough that an
attacker cannot crack the key.

## AES Encryption

`AES` (Advanced Encryption System) [<sup>\[4\]</sup>](#r4%20) algorithm,
is usually the chosen one for `Symmetric Encryption`. This algorithm is
rather procedural than hard mathematical formula computation, it
basically encrypts a table of data in four steps:

1. `SubBytes` : Each value in a table is substituted by another using a
    table.

2. `ShiftRows` : Rows of the table are shifted by some offset.

3. `MixColumns` : Columns are mixed by a matrix operation.

4. `AddRoundKey` : The public key is performed over the table with an
    `XOR` operation.

All operations performed are reversible and they are made in order to
eliminate or diffuse any possible pattern or relationship of the
ciphered message to the original one and to the key that might hint an
attack.

## Conclusion

You can be sure your data is very well protected and that the
communication won’t be disclosed to any attacker thanks to a `Trapdoor`,
of course, as computing power continues to develop, we might need to
create new traps, but now the assurance of your privacy on communication
is really high, so every time you browse your social networks, bank
accounts, etc; remember there is a `Trapdoor` that won’t let any cat
out.

## References

1. [`Trapdoor`
    functions](http://mathworld.wolfram.com/TrapdoorOne-WayFunction.html)

2. [`Symmetric` and `Asymmetric`
    `Encryption`](https://hackernoon.com/symmetric-and-asymmetric-encryption-5122f9ec65b1)

3. [`RSA`
    Explained](https://hackernoon.com/how-does-rsa-work-f44918df914b)

4. [`AES`
    Explained](https://thebestvpn.com/advanced-encryption-standard-aes/)

5. [Euler’s
    function](https://en.wikipedia.org/wiki/Euler%27s_totient_function)

6. [Coprime number](https://simple.wikipedia.org/wiki/Coprime)

7. [Modular multiplicative
    inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse)
