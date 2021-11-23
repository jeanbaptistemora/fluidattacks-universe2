---
slug: reverse-engineering/
title: Opening the Program's Box
date: 2020-03-11
subtitle: General ideas about Software Reverse Engineering
category: techniques
tags: revert, software, engineering, security, vulnerability, hacking
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331058/blog/reverse-engineering/cover_nsktcf.webp
alt: Photo by Erda Estremera on Unsplash
description: Here we review some basic concepts of reverse engineering within
  information technology and through what tools it can be used for ethical
  and malicious hacking.
keywords: Revert, Software, Reverse Engineering, Security, Vulnerability,
  Hacking, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/sxNt9g77PE0
---

Just by curiosity, a child today may take a device and disassemble it.
Possibly wondering what elements are inside and how they come together
to work. Something similar can be done by an adult in a workshop. But
with the intention of repairing an engine that for some unknown reason
has stopped working. We can also mention the woman who, in her
workplace, has the mission of deconstructing the program that others had
worked on before. Just in order to renew and improve some of its
performance features.

<div class="imgblock">

![child1](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331056/blog/reverse-engineering/child1_pwhnxl.webp)

<div class="title">

Figure 1. Photo by [Kelly Sikkema](https://unsplash.com/@kellysikkema)
on Unsplash

</div>

</div>

All of them have applied what is known as **reverse engineering**, which
is constituted as a process of deconstruction. It is a matter of
reversing the steps of development, in order to analyze and obtain
knowledge of anything [engineered and elaborated by human
beings](https://www.mitre.org/sites/default/files/publications/pr-15-2630-reverse-engineering-cognition.pdf).
That thing can be a chemical substance, a machine, a software code or
another type of object. [This process seeks to reveal and determine its
innermost
details](https://www.foo.be/cours/dess-20122013/b/Eldad_Eilam-Reversing__Secrets_of_Reverse_Engineering-Wiley\(2005\).pdf),
components and their relationships. It is intended to discover how the
object in question was designed and produced.

Here are [some of the
reasons](http://index-of.es/Varios-2/Penetration%20Testing%20and%20Reverse%20Engineering.pdf)
why reverse engineering is employed:

- Information on a product. Documentation may have been lost, is
  inaccessible, or simply never existed, and there is no contact with
  the producer.

- Analysis of a product. Knowing how it works, what components it has,
  defining costs, and identifying possible copyright violations.

- An update or correction of the product functioning.

- Security auditing or assessment of the product.

- Creation of duplicates of the product without a license.

- Competition issue. Understanding what competitors do and what
  characterizes their products.

- Simple curiosity and learning purposes about the structure of the
  product.

We can apply reverse engineering within Information Technology (IT),
[either for software or
hardware](https://www.youtube.com/watch?v=7v7UaMsgg_c). In this case we
focus on **Software Reverse Engineering** (`SRE`), which, as it is
understood, applies to the analysis of software, [the discovery of its
general
properties](https://www.mitre.org/sites/default/files/publications/pr-15-2630-reverse-engineering-cognition.pdf),
and the identification of its components, functions and relationships.
This is often done in the absence of its source code or relevant
documentation, [claiming its repair or
improvement](https://link.springer.com/chapter/10.1007/978-3-642-04117-4_31).
This process emerged from software maintenance and support, [largely
from malware
analysis](https://link.springer.com/chapter/10.1007/978-3-319-74950-1_6).

We can separate `SRE` [into two
phases](https://www.foo.be/cours/dess-20122013/b/Eldad_Eilam-Reversing__Secrets_of_Reverse_Engineering-Wiley\(2005\).pdf):
The first one can be seen as a large scale observation to determine the
general structure, and sometimes areas of special interest, of the
software under analysis. This phase implies the use of various tools and
several services of the operating system. This tools and services enable
the acquisition of information, tracking inputs and outputs, inspecting
executables, among other things. The second phase is deeper, and more
oriented to code fragments to understand them in their structure and
functionality.

## Tools

<div class="imgblock">

![child2](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331057/blog/reverse-engineering/child2_csnxly.webp)

<div class="title">

Figure 2. Photo acquired from
[Exploratorium](https://www.exploratorium.edu/sites/default/files/tinkering/files/open_make_april_18.jpg)

</div>

</div>

According to the above information, `SRE` depends considerably on the
use of tools, many of which were [not designed directly for this
purpose](https://www.foo.be/cours/dess-20122013/b/Eldad_Eilam-Reversing__Secrets_of_Reverse_Engineering-Wiley\(2005\).pdf).

Before continuing, it is wise at this point to make a parenthesis. And,
for those of us who are not used to the subject, briefly explain the
software languages on two general levels.

The lower level is generally made up of binary code (ones and zeros) or
hexadecimal code. This executable representation of software, what the
`CPU` reads, is known as **machine language** or also as byte code.

On the same level of languages, being a different form of representation
of the same thing, are the **assembly languages**. These are easier for
humans to understand, because they map or represent specific bit
patterns, machine instructions, using useful mnemonics (short but
memorable character sequences).

The upper level covers even more understandable languages, possessing
keywords and constructs that developers use as building blocks in their
programs. This is where, for example, `COBOL`, `Java` and `C` are
situated.

Now, in relation to the tools, one of the main ones in `SRE` is the
**disassembler**, which develops a process contrary to an assembler, and
which will be different [depending on the platform on which it is
used](https://link.springer.com/chapter/10.1007/978-3-319-74950-1_6).
The **disassembler** translates machine language (input) to assembly
language (output), [for the entire program or parts of
it](https://www.foo.be/cours/dess-20122013/b/Eldad_Eilam-Reversing__Secrets_of_Reverse_Engineering-Wiley\(2005\).pdf).

As an expansion of the **disassembler’s** work, and [in some reversing
tasks as the only necessary
tool](https://www.foo.be/cours/dess-20122013/b/Eldad_Eilam-Reversing__Secrets_of_Reverse_Engineering-Wiley\(2005\).pdf),
appears the **debugger**. With this, over the disassembled code, we can
establish breakpoints —and check the current state of the program within
them— in locations of interest, go through the code running line by line
in its analysis, and even [make edits at run
time](http://index-of.es/Varios-2/Penetration%20Testing%20and%20Reverse%20Engineering.pdf).
That is, unlike the **disassembler**, the **debugger** does not work in
static program code, but allows us to observe the behavior of the
program as it runs. And to a flow suitable for human perception, with
[pauses in execution as
required](https://link.springer.com/chapter/10.1007/978-3-319-74950-1_6).

Thus, after the action of the **disassembler**, it is expected to
translate the assembly language into a high-level language, easier to
read and understand. This would be more appropriate for subsequent
modification of the program in question. However, [this task is
complex](https://link.springer.com/chapter/10.1007/978-3-642-04117-4_31).

Lastly, let us address the **decompiler**, which is the opposite of a
compiler. This tool tries to recreate the original source code, in
high-level language, through the analysis of the binary code or
sometimes the assembly language. Nevertheless, the information obtained
is complex to understand. High-level concepts like classes, arrays,
sets, and lists may not be easily recreated. And comments and variable
names may have been completely lost (omitted during compilation), even
the name of the high-level language used.

Still, the **decompiler** is valuable and useful because it reveals all
the basic information [about the operation of the
program](https://link.springer.com/chapter/10.1007/978-3-319-74950-1_6).
The **decompiler** retrieves high-level language of the program from the
machine code, while the **disassembler** stays in the assembly language
instructions reconstruction.

For more information on the tools and exhibition of the most used, visit
[Medium](https://medium.com/@vignesh4303/reverse-engineering-resources-beginners-to-intermediate-guide-links-f64c207505ed)
and
[Apriorit](https://www.apriorit.com/dev-blog/366-software-reverse-engineering-tools).

## SRE for Security

`SRE` can be useful for modifying software structures, altering code,
adding or removing commands and changing functions, thus affecting their
logical flow. From the security area, the `SRE` provides techniques for
hacking, whether it is malicious or ethical. In other words, it is
useful to do damage or to generate protection and prevent it.

On the positive side, `SRE` has involved finding flaws and
vulnerabilities in, for example, systems and encryption algorithms.
There is also the analysis of the behavior and properties of malware on
test systems or on already infected foreign systems (hence the
development of antivirus software). Likewise, there is prevention of
piracy of the program and the information contained, thus protecting the
digital rights.

On the negative side, through `SRE` criminals find vulnerabilities in
systems, and well…​ they take advantage of them.

Ethical hacking is what we do within `Fluid Attacks`, with our security
experts, and with the permission of the client organizations. Thus, in
their programs and systems, we discover and compel the remedy of
weaknesses in security. Therefore, we protect them from future attacks
by cyber-criminals. Our hackers, in their ethical stance, and as part of
reverse engineering, must simulate the behavior of malicious hackers,
and thus understand their intentions and design parameters in the
attack. All this in order to establish a proper defense or
counterattack.

[Contact us](../../contact-us/), and learn more about our services\!
