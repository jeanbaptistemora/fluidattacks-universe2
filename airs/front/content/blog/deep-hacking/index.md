---
slug: deep-hacking/
title: Deep Hacking
date: 2019-01-25
subtitle: Deep learning for vulnerability discovery
category: machine-learning
tags: machine-learning, vulnerability, discovery
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330846/blog/deep-hacking/cover_oww6xm.webp
alt: 'Depiction of a deep neural network. Credits:
  https://unsplash.com/photos/R84Oy89aNKs'
description: Here we describe the first systematic framework for using
  deep learning to detect vulnerabilities in source code by cutting
  the program into slices.
keywords: Machine Learning, Vulnerability, Deep Learning, Discovery,
  Static Detection, Security, Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/R84Oy89aNKs
---

If we have learned anything so far in our quest to understand how
[machine learning](../crash-course-machine-learning/) (`ML`) can be used
to [detect vulnerabilities](../machine-learning-hack) in source code,
it’s that what matters the most in this process are the different
representations of source code which are later fed to the actual `ML`
algorithms. Especially, that these representations should include both
semantic and syntactic information about the code.

Also, that one `ML` technique seems particularly promising, but hardly
exploited, namely, [deep
learning](../crash-course-machine-learning/#artificial-neural-networks-and-deep-learning).
Methods such as [Recurrent Neural
Networks](https://en.wikipedia.org/wiki/Recurrent_neural_network)
(`RNN`), [Convolutional Neural
Networks](https://en.wikipedia.org/wiki/Convolutional_neural_network)
(`CNN`), and [Deep Belief
Networks](https://en.wikipedia.org/wiki/Deep_belief_network) (`DBN`)
have been succesful in image and natural language processing, but never
applied to vulnerability discovery in a systematic fashion.

The aim of the project [`SySeVR`](https://github.com/SySeVR/SySeVR) is
to apply deep learning techniques to the discovery of sofware
vulnerabilities in source code, considering not only the *form* (syntax)
which might induce a vulnerability, but also the flow of data and
control in the program. They also tried to produce results as finely
granular as possible, i.e., tell us exactly at which line or function
the flaw arises. If that’s not enough, they also promise to explain the
cause of false positives, if there are any.

When working with images and pattern recognition, objects of interest
have a natural representation as vectors, which are suitable for machine
learning algorithms. In that case it is easy to propose where an object
in the image might be: just take smaller pieces of the image, and test
their inherent features such as texture and color to determine if they
are or not what we want to detect.

In order to translate this idea to code, the authors can leverage
well-known patterns in previously identified vulnerabilites. Simply
patterns that might trigger dangerous situations, such as the use of
`malloc` and pointers in `C`, [concatenating user
input](../pars-orationis-secura/#specifying-the-targets), [importing
flawed libraries](../stand-shoulders-giants/), etc. Anything that a
regular [static analysis tool](../replaced-machines/) might look for,
but probably with false positives. They call these *Syntactic
Vulnerability Candidates* (`SyVC`). These can be either a single token
(`malloc`) taken from the program’s [Abstract Syntax
Tree](../oracle-code/#databases-out-of-programs) or a set of tokens
(`memset(dataBuffer…​`) or a whole statement which involves one of the
mentioned danger situations.

<div class="imgblock">

![Comparison of image vs code recognition](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330846/blog/deep-hacking/comparison_cd5exl.webp)

<div class="title">

Figure 1. Comparing image vs. code recognition

</div>

</div>

In order to avoid false positives, the next logical step is to use
semantic information about the program, i.e., how data and control flows
in it in order to expand our knowledge about what happens before and
after executing a particular line of code. And where does this
information lie? As we know by know, this can be found in the [`Control
Flow` and `Program Dependency`
graphs](../exploit-code-graph/#combining-standard-code-representations).
Armed with these two graphs, one can find the whole "influence zone" of
a particular token or line, with a technique they call *program
slicing*. Basically it means to take all nodes in the semantic graph
representations that are reachable from the token of interest, the
`SyVC`. In other words, all lines of code that are executed before and
after this particular token or are somehow altered if its value were to
change. They call this a "Semantic Vulnerability Candidate". Usually if
the `SyVC` is a whole function, then the corresponding `SeVC` will
include all functions called by it and all the function that call it.

The next problem to be solved is: Having already identified a piece of
the program that might contain a vulnerability as a `SeVC`, how do we
encode that as a vector or something that can be understood by machine
learning algorithms? The approach chosen by the authors is to first give
generic names to all the functions and variables (thus sort of
*obfuscating* it lightly), then perform a lexical analysis on it (i.e.,
breaking it up into symbols) and finally representing that strings as a
bag of words, a procedure we have already referred to in past articles.
A fixed length must be chosen and vectors that don’t fit must be padded
or truncated, since the chosen neural networks take vectors of a fixed
length as input. Here is a depiction of the process for a particular
piece of code:

<div class="imgblock">

![Illustration of the process](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330845/blog/deep-hacking/process_w5rzss.webp)

<div class="title">

Figure 2. Illustration of the process

</div>

</div>

All that remains is to train and test the neural networks. One of the
goals of `SySeVR` was to be able to work with different types of
networks. Six (\!) different types of networks were implemented in
`Python` with the [Theano](http://www.deeplearning.net/software/theano/)
library: `CNN`, `DBN`, and four types of `RNN`: (Bidirectional)
[Long-short term
memory](https://en.wikipedia.org/wiki/Long_short-term_memory)
(`(B)LSTM`) and (Bidirectional) [Gated Recurrent
Unit](https://en.wikipedia.org/wiki/Gated_recurrent_unit) (`(B)GRU`).
They validated their results against a vulnerability dataset combining
[`NVD`](https://nvd.nist.gov/) and
[\`SARD](https://ws680.nist.gov/publication/get_pdf.cfm?pub_id=923127),
labeled either as vulnerable or not, ideally some with the corresponding
diff and the vulnerability type.

But which syntactic patterns to look for? Who will be the syntactic
vulnerability candidates? For this, they used standard static detection
tools such as [`Checkmarx`](https://www.checkmarx.com/),
[`Flawfinder`](https://dwheeler.com/flawfinder/) and
[`RATS`](https://security.web.cern.ch/security/recommendations/en/codetools/rats.shtml).
From these results, they decided to focus on four main vulnerability
types, out of the 126 different *kinds* of vulnerabilities contained in
the dataset:

- Insecure `API` usage, v.g. `malloc` without `free`.

- Array usage.

- Pointer usage

- Improper arithmetic expressions.

For this particular "experiment", the graph code representations were
obtained with the tool [Joern](http://mlsec.org/joern/) by Yamaguchi et
al., a sister project of [`Chucky`](../anomaly-serial-killer-doll/) of
sorts. The `SeVC` to vector encoding was performed with
[`word2vec`](https://radimrehurek.com/gensim/models/word2vec.html).

The results of the experiment can be summarized as follows:

- `BGRU` networks appear to be the best fit for vulnerability
  discovery, as long as the training data is good. In general the
  effectiveness of deep neural networks is a open research problem.

- For any kind of neural network used, it is better to tailor them to
  the specific kind of vulnerability that is sought, rather than try
  to use a catch-all type of model.

- `SySeVR` results are way better than those of current, commercial,
  well-established static detection tools such as mentioned
  `Checkmarx`.

`SySeVR` was able to identify 15 vulnerabilities new to `NVD` in open
source projects like `Thunderbird` and `Seamonkey`, all of which were,
as it should, [responsibly disclosed](../vulnerability-disclosure/).
Some of them got listed in `CVE`. Others were silently patched by their
manufacturers. These are, of course, the most important product of this
idea and are summarized in the following table:

<div class="imgblock">

![SySeVR results](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330845/blog/deep-hacking/table_gyimhe.webp)

<div class="title">

Figure 3. New vulnerabilities found by `SySeVR`.

</div>

</div>

---
Thus, the idea of applying deep learning techniques to vulnerability
discovery in source apparently does deliver the promised results.
However as mentioned earlier, these are to be taken with a grain of
salt, until the results are peer-reviewed and cross-validated by the
academic and security communities, or, at least, by [us](../../).

## References

1. Z. Li, D. Zou, Shouhuai X., H. Jin, Y. Zhu and Z. Chen (2018).
    *SySeVR: A framework for using deep learning to detect software
    vulnerabilities*. [`arXiv:1807.06756
    [cs.LG`](https://arxiv.org/pdf/1807.06756.pdf)\</literal\>\]
