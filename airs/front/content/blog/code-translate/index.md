---
slug: code-translate/
title: Can Code Be translated?
date: 2020-01-31
subtitle: From code to words
category: machine-learning
tags: machine-learning, security, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330835/blog/code-translate/cover_wmd0zp.webp
alt: Book in two languages
description: Here we talk about Code2seq, which differs in adapting neural
  machine translation techniques to the task of mapping a snippet of code
  to a sequence of words.
keywords: Machine Learning, Neural Network, Encoding, Parsing, Classifier,
  Vulnerability, Code2seq, Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/r8H8K3w9AzA
---

Now that we have a better undestanding of how natural language and code
embeddings work, let us take a look at a work by the same authors of
`code2vec`, entitled `code2seq`: generating sequences from code
[\[1\]](#r1). What sequences? you might ask. Sequences of natural
language, which might have different applications according to the given
training data. In the original paper, they propose some applications:

- Code summarization, i.e., explain in a few words what a snippet of
  code does, although not necessary in articulate language.

- Code captioning, which is pretty much the same, only properly
  written.

- Even automatic code documentation, in particular, generate `JavaDoc`
  documentation given a `Java` method.

A picture says more than a thousand words:

<div class="imgblock">

![Sample prediction and generated AST](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330833/blog/code-translate/example_piygbl.webp)

<div class="title">

Figure 1. Sample prediction and generated AST via [demo
site](https://code2seq.org/).

</div>

</div>

Notice that the `AST` says *even less* about what this snippet does than
the code itself, in my opinion. And yet `code2seq` sort of manages to
*understand the intent* of this function, which is to generate a prime
number for an `RSA` key. The prediction for the summary of this method
is: `generate prime number`. Not too shabby.

So, how does it work? Again, as in `code2vec` they use randomly taken
`AST` paths from one leaf token to another leaf for the initial
representation of code,

<div class="imgblock">

![Paths in an AST](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330832/blog/code-translate/ast-paths_bkk3wi.webp)

<div class="title">

Figure 2. Paths in an AST. From [\[1\]](#r1).

</div>

</div>

This representation, according to them, is fairly standard
representation of code for machine learning purposes, and has a few
advantages, namely:

- It does not require semantic knowledge.

- Works across programming languages.

- It is not needed to hard-code human knowledge into features.

However, as with `code2vec`, one requires a specific *extractor*
(essentially a tool to parse the code and extract the `AST` in a
specific format understandable by `code2*`) for each language one
intends to analyze. One key difference with `code2vec` is the use of the
long short-term memory (`LSTM`) neural network architecture, which is
used to encode each `AST` path from the previous step as a sequence of
nodes. Otherwise the architecture is pretty similar:

<div class="imgblock">

![Code2seq architecture](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330833/blog/code-translate/network_cprp7q.webp)

<div class="title">

Figure 3. `code2seq` architecture. From [\[1\]](#r1).

</div>

</div>

As with `code2vec`, their main secret sauce lies in the *attention*
mechanisms, and the encoding and decoding layers which sort of resemble
the inner workings of an *autoencoder*, which we met
[earlier](../embed-code-vector/) and serves as a stepping stone into
understanding the vector representation of code and other objects.

Another intersesting under the hood idea of `code2seq` is to take after
`seq2seq` models, which are widely used in natural language translation
with neural networks (*neural machine translation*). The idea is to
connect two separate neural networks: one for encoding the source
language and one for decoding into the target language. This already
suggests an *intermediate* representation, a 'universal language' of
sorts, that only these kind of networks understand. Again, this is a bit
reminiscent of the autoencoder example and most likely stemmed from that
seminal idea.

<div class="imgblock">

![seq2seq diagra](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330833/blog/code-translate/seq2seq_gdwcwt.webp)

<div class="title">

Figure 4. `seq2seq` diagram, via [d2l.ai](https://d2l.ai/_images/seq2seq.svg).

</div>

</div>

Needless to say that this kind of translator networks achieve better
than deterministic methods, and are in fact used in production
translators nowadays. Not just that: they can be used not only for
translation, for also v.g. for chatbots, by changing the training data:
instead of giving pairs of sentences in different languages, just match
questions with their answers, or sentences that naturally follow one
another.

And, as we see here, with careful adjustment, the idea can be applied
even to more structured languages, such as programming languages. The
results are better than the current benchmarks, including the authors'
own previous work, `code2vec`:

<div class="imgblock">

![code2seq results](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330832/blog/code-translate/results_b9vy81.webp)

<div class="title">

Figure 5. `code2seq` results

</div>

</div>

The image to the left refers to the results from the summarization task
with `Java` source code. Different methods (right) are compared using
the F1 score (see discussion in our [last article](../further-code2vec/)
for details, but keep in mind this score balances how much is actually
found and how much escapes). The one on the right does the same for the
`C` captioning application, this time comparing the
bilingual evaluation understudy (`BLEU`) scores, which are specific to
machine translation. Clearly, for both tasks, `code2seq` beats the
current state of the art.

As far as using it for our purpose and testing the accuracy, `code2seq`
provides pretty much the same interface as `code2vec`, which you can
check out in our [last article](../further-code2vec/), so we might
expect the same ease of use. Only further experiments with the
embeddings produced by this and `code2vec` will let us decide which one
to go with for our classifier.

While code ummarization and captioning are the only two applications
researched by the authors, and documentation generation is proposed,
this might have applications beyond that. One idea of the top of my
head: while our code classifier is supposed to only give a probability
of a file or function containing a vulnerability, it could also produce
a list of the *possible* specific types of vulnerabilities. To reuse the
example above, imagine that instead of predicting the words "generate
prime number", it would predict "buffer overflow", assuming the function
contained such a vulnerability, and perhaps other kinds of
vulnerabilities with lower probabilities, such as "lack of input
validation". That is an interesting direction to research, i.e., being
more specific in the predictions, one that has been asked a lot during
the [talks](https://www.youtube.com/watch?v=CRoQZDmRvoE), and one that
we will certainly keep in mind.

Overall, `code2seq` is an innovative way of looking at the code-natural
language relations, bringing into the game sophisticated techniques from
the field of neural machine translation, and exploiting the rich syntax
of code in the form of its `AST`, which as we haven seen throughout the
series, is one of the simplest and most succesful ways of representing
code features. Stay tuned for more of this.

## References

1. U. Alon, M. Zilberstein, O. Levy, and E. Yahav. [code2seq:
    Generating Sequences from Structured Representations of
    Code](https://openreview.net/pdf?id=H1gKYo09tX). ICLR'2019
