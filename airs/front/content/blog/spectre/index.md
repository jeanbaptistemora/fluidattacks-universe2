---
slug: spectre/
title: What's the Perfect Crime?
date: 2021-05-27
subtitle: 'The one that leaves no trace: the Spectre one?'
category: attacks
tags: cybersecurity, exploit, mistake, risk, technology, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1627388863/blog/spectre/cover-spectre_ldoml1.webp
alt: Photo by Sammy Williams on Unsplash
description: Spectre has reappeared! It has returned full of surprises and can transform
  the way processors are made. Here is what we know about it.
keywords: Spectre, Vulnerability, Software, Cybersecurity, Speculative Execution,
  Ethical Hacking, Processor, Pentesting, CPU
author: Felipe Zárate
writer: fzarate
name: Felipe Zárate
about1: Cybersecurity Editor
source: https://unsplash.com/photos/ocvLVIrC7c0
---

**Spectre** was in the spotlight of cyber threat news in 2018. Its name
is a direct reference to the only agent capable of attacking in that
way: a specter. Since every ghost always comes back, Spectre has
reappeared\! To start talking about it, we have prepared a story and a
challenge for you. **Can you solve it?**

Imagine the following scenario: one businessman increased his company’s
efficiency by hiring different people to perform routine tasks even
before someone asked them to do so. If a posteriori instruction
contradicted what the employees had done, they reversed and forgot those
failed actions.

Some years later, the businessman’s lifeless body appeared in his
library. He had a deep wound in his heart with an undue pool of blood.
There was nothing nearby that could have been used to kill him. The room
had doors and windows closed from the inside with no openings in walls,
ceiling, or floor. The only suspect was an employee who was with him two
hours before his death. However, after drinking the infallible truth
serum, it was confirmed his innocence. The victim’s sister claims the
assassin was a ghost. But was it?

Clues are already given, and we can suggest a solution. But, before
that, if you think that this story is merely fiction, I invite you to
read what happened with the Spectre case.

<div class="imgblock">

![ghosts](https://res.cloudinary.com/fluid-attacks/image/upload/v1622051254/blog/spectre/ghosts_ec3lsn.webp)

<div class="title">

Figure 1. Photo by [Kirill Sharkovski](https://unsplash.com/photos/jZ9TPXjoZQk)
on Unsplash

</div>

</div>

## Spectre

[Since 2004](https://www.ieee-security.org/TC/SP2019/SP19-Slides-pdfs/Paul_Kocher_01_-_Spectre_Attacks-IEEE-SecurityPrivacy_v05.pdf)
the 3.8GHz Pentium 4 has been allowed to ["bump in speed from the
already available 6xx line of
processors."](https://www.anandtech.com/show/1695) Computers and devices
that work with microchips increased their efficiency. Behind that
increased performance, there was an effort [to boost pipeline in average
cases](https://www.youtube.com/watch?v=zOvBHxMjNls), reduce memory
delays by using caches, and work during delays using **speculative
execution**. That allowed routine processes ([such as move data from one
memory location to another, or jump to a different
address](https://turbofuture.com/computers/What-are-the-basic-functions-of-a-CPU))
to be much more efficient. Now, how did this advantage become a
vulnerability?

To answer that, we will explain what **speculative execution** is by
referring to Paul Kocher’s talk: [*Spectre Attacks Exploiting
Speculative Execution*](https://youtu.be/zOvBHxMjNls). In fact, Spectre
was brought out into the open for the [first
time](https://meltdownattack.com/) in May 2019 at the [**40th IEEE
Symposium on Security and
Privacy**](https://www.ieee-security.org/TC/SP2019/).

## Speculative execution

A CPU could start a course of action without confirming that it is the
correct path. In other words: ["the CPU guess likely future execution
directions and prematurely execute instructions on these
paths."](https://www.computer.org/csdl/pds/api/csdl/proceedings/download-article/19skfbE9KUw/pdf)
This means that even before the value that executes an instruction
appears, the CPU is already performing it.

This solution responded to the limited number of processes a CPU can
execute at the same time. That number is conditioned by each CPU [clock
cycle](https://techterms.com/definition/clockcycle#:~:text=A%20clock%20cycle%2C%20or%20simply,processes%20require%20multiple%20clock%20cycles.).
To avoid waiting,

<div class="imgblock">

![Figure1](https://res.cloudinary.com/fluid-attacks/image/upload/v1622204109/blog/spectre/figure1_uygv6x.webp)

<div class="title">

Figure 2. [(Text fragment from: Kocher et
al., 2019)](https://www.computer.org/csdl/pds/api/csdl/proceedings/download-article/19skfbE9KUw/pdf)

</div>

</div>

When the value is known, a CPU identifies if the speculation was
correct. If so, "the code continues as supposed, and the result would
come faster." If the assumption was wrong,

<div class="imgblock">

![Figure2](https://res.cloudinary.com/fluid-attacks/image/upload/v1622204893/blog/spectre/figure2_gqvslb.webp)

<div class="title">

Figure 3. [(Text fragment from: Kocher et
al., 2019)](https://www.computer.org/csdl/pds/api/csdl/proceedings/download-article/19skfbE9KUw/pdf)

</div>

</div>

There is no cost in time or resources since the alternative option is to
wait for the value to be revealed. Then either the CPU expects data to
execute orders or "get ahead of the job" and perform the process before
the command. However, over time it was seen that [there were security
implications from speculative
execution](https://www.ieee-security.org/TC/SP2019/SP19-Slides-pdfs/Paul_Kocher_01_-_Spectre_Attacks-IEEE-SecurityPrivacy_v05.pdf).
In fact, the CPU was opening a vulnerability on its own: a **fault
attack** hardware was built-in.

## Branch Predictor and Out-of-bounds

One way to change instructions is by taking advantage of **Branch
predictors**. These are architectural units used ["to guess where guess
where the next instruction, after a branch, will come
from."](https://spectrum.ieee.org/computing/hardware/how-the-spectre-and-meltdown-hacks-really-worked)
Through them, the CPU speculates whether a conditional branch will be
taken and the possible outcome of the instruction if it is executed. If
the speculation is wrong, the CPU will reverse all registry contents
back to where they were before proceeding.

Now, the CPU performs a legal
[out-of-bounds](https://docs.fluidattacks.com/criteria/vulnerabilities/111),
i.e., ["the software reads data past the end, or before the beginning,
of the intended
buffer."](https://cwe.mitre.org/data/definitions/125.html) The Buffer is
a memory piece in the processor that allows returning from cache or
temporary memory to complete long-lasting memory addresses. Here is
where a security breach is performed. In Kocher’s words, the problem is
that:

<div class="imgblock">

![Spectre Attacks Exploiting](https://res.cloudinary.com/fluid-attacks/image/upload/v1622464150/blog/spectre/quote_dynn0w.webp)

<div class="title">

Figure 4. [(Fragment from Kocher’s
presentation)](https://youtu.be/zOvBHxMjNls?t=331)

</div>

</div>

What is astonishing is that it is not only allowed, but it is integrated
into CPU operations\!

This vulnerability has been widely known and analyzed. Since 2018, when
it first came to light, Intel and AMD, two of the world’s biggest
processor companies, ["adjusted their microcode to change the behavior
of some assembly-language instructions in ways that limit
speculation."](https://spectrum.ieee.org/computing/hardware/how-the-spectre-and-meltdown-hacks-really-worked)
Their solution was to limit "spaces" in which speculation is allowed. By
doing so, they made specific processing moments safer but slower.

## Spectre reappearance

A paper published by the University of Virginia concludes that this
threat is not over yet. [Researchers
have](https://engineering.virginia.edu/news/2021/04/defenseless-uva-engineering-computer-scientists-discover-vulnerability-affecting)
"uncovered a line of attack that breaks all Spectre defenses," which
means that "billions of computers and other devices across the globe are
just as vulnerable today as they were when Spectre was first announced."

Specifications of this new threat can be reviewed in their [article (Ren
et al., 2021).](https://www.cs.virginia.edu/venkat/papers/isca2021a.pdf)
However, the main risk identified in their study is that Spectre
vulnerability is not in the software but in the hardware. Notably,
Intel, AMD, and AMR processors use
[micro-ops](https://erik-engheim.medium.com/what-the-heck-is-a-micro-operation-e991f76209e)
to process complex instructions into small micro-op caches. And
[published
research](https://www.cs.virginia.edu/venkat/papers/isca2021a.pdf)
describes "attacks that exploit the micro-op cache as a timing channel
to transmit secret information." As a result of those attacks, criminals
can leak secrets in three primary settings (see those settings in detail
[here](https://www.cs.virginia.edu/venkat/papers/isca2021a.pdf)).

Although this finding is recent and will be publicly discussed this year
in June at the [**International Symposium on Computer
Architecture**](https://www.iscaconf.org/isca2021/program/), the team
that wrote the paper has already talked to Intel and AMD about their
findings. On May 4, an [Intel spokesman
said](https://itwire.com/security/us-researchers-find-flaw-affecting-processors-made-since-2011.html):
"that existing mitigations were not being bypassed and that this
scenario was addressed in its secure coding guidance." Still, that
response is disappointing because the problem should not be solved using
constant-time programming. Instead, it should be fixed from its source:
processors.

## Not-so-perfect crime

Let us go back to our crime scene. The key is in the truth serum test.
Is it possible that the employee does not remember what he did? Why did
he act this way, if he is the assassin? What did he use to get through
the victim’s heart? The answer is, perhaps, in the excessive pool of
blood. If there is a way to make an object disappear in a couple of
hours… Can you think of what it could be?

<div class="imgblock">

![Ice](https://res.cloudinary.com/fluid-attacks/image/upload/v1622051251/blog/spectre/ice_ounl8h.webp)

<div class="title">

Figure 5. Photo by [Yannic Kress](https://unsplash.com/photos/zwd_QW8JB7g)
on Unsplash

</div>

</div>

We hope you have enjoyed this post, and we look forward to hearing from
you. [Contact us\!](../../contact-us/)
