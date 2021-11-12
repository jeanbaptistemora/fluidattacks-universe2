---
slug: embed-code-vector/
title: Embedding Code Into Vectors
date: 2020-01-10
subtitle: Vector representations of code
category: machine-learning
tags: machine-learning, security, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330869/blog/embed-code-vector/cover_ah0e4k.webp
alt: Arrows vector field
description: Here we discuss code2vec relation with word2vec and autoencoders
  to grasp better how feasible it is to represent code as vectors,
  which is our main interest.
keywords: Machine Learning, Neural Network, Encoding, Code2vec, Word2vec,
  Parsing, Classifier, Vulnerability, Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/N4gn-eLEIwI
---

As we have stated over and over in the past, the most critical step in
our ongoing project of building a machine learning (ML) based code
classifier will be that of representing the code as vectors. In our
[last article](../vector-language), we reviewed how this is done for
natural language. We looked at simple, though inconvenient methods, such
as one-hot and categorical encoding, which we actually used in our
[first classifier attempt](../vulnerability-classifier). We also took a
glimpse at the state of the art in vector representation of language,
which is based on neural networks, called `word2vec`.

Recall that this is a neural network which attempts to predict
neighboring words from the central word. Its dataset is made up from a
corpus, and the results will be very dependent on the sense of this
text. While the task is certainly useful, we don’t care so much about
the predictions, but rather about the weights which make up the network,
which give us an intermediate representation. These are the vectors we
are looking for to represent each word:

<div class="imgblock">

![Word2Vec network](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331138/blog/vector-language/word2vec-network_cn6omp.webp)

<div class="title">

Figure 1. The vectors are implicit in the middle layer.

</div>

</div>

In turn, `word2vec` is based on a more simple task: predict a vector
from that same vector. Well, isn’t that just an identity function,
mapping every object to itself? As it turns out, no, given that the
weights in a neural network are randomly or arbitrarily initialized and
will be optimized to the task in an iterative process. For this task,
with a single hidden layer, we get something similar to `word2vec`,
called an *autoencoder*:

<div class="imgblock">

![Autoencoder neural network](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330868/blog/embed-code-vector/autoencoder_yypcyp.webp)

<div class="title">

Figure 2. Autoencoder neural network via [Carnegie
Mellon](https://insights.sei.cmu.edu/sei_blog/blog_figure1_06102019.png).

</div>

</div>

Autoencoders turned out to be a foundational idea in neural network
based dimension reduction, the task of representing high-dimensional
objects (such as one-hot encoded words) as lower-dimensional vectors,
while still retaining most of the useful information contained in it.
Before that, most methods relied on matrix decompositions, but these
tend to be computationally expensive and not scalable, thus not fit for
representation of large codebases or natural language corpora.

Keeping these two neural network based ideas, namely that vector
representations can be obtained from middle layers in networks designed
for different, though seemingly frivolous tasks, one can begin to
understand how vector representations of code might come to be. What
will be the goal? Predicting the name of a function. What will be the
input data? Not too surprisingly, it will be the code of the function
whose name we would like to predict. In what form? That’s where the
waters get a little murky, since there are so many ways to structure
code, and so many representations to extract from it. Our readers might
already be familiar with the Abstract Syntax Tree, Version Control
(v.g., `git`) history and the [Control flow and program dependence
graphs](../exploit-code-graph). One can even simply choose not to
represent anything: consider the code as sequence of words without
exploiting its syntax, and represent them as bags of words, as we did in
our [previous run](../vulnerability-classifier). One could also look at
the [meta-code](../machine-learning-hack/#other-approaches): metrics
such as modified lines per commit, code churn, cyclomatic complexity,
all of those could be thought of as possible candidates for inputs to a
neural code classifier.

One of the most apt of such representations is the Abstract Syntax Tree
(`AST`), which is universal in the sense that it can be taken out of
every language in existence, and could potentially be standardized so as
to eliminate the language barrier. Indeed, this is the input
representation chosen by the `code2vec` authors. More specifically, they
sample some paths in the `AST` at random. The labels in the training
phase, which would be the prediction targets later, are the function
names. The objective is to predict meaningful function names from the
function’s content. If the body is `return input1 + input2`, it would
seem obvious to a human to call that function `add` or even `give_sum`.
However, this is not the case, as there are developers who give strange
names to their identifiers and methods, such as
`perform_binary_operation1`. Maybe to make their code [hilariously
unmaintainable](https://www.se.rit.edu/~tabeec/RIT_441/Resources_files/How%20To%20Write%20Unmaintainable%20Code.pdf)
and keep their jobs forever, since nobody else would understand it; or
just make it sound like it does more than in reality.

The network itself to predict the function names from the randomly-taken
paths in their abstract syntax trees is a little more complicated than
an autoencoder or a single-layer `word2vec` network:

<div class="imgblock">

![code2vec architecture. From ](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330868/blog/embed-code-vector/code2vec_b5e4ms.webp)

<div class="title">

Figure 3. code2vec architecture. From [Alon et al.
(2018)](#r1).

</div>

</div>

Notice that in this diagram, unlike most other seen here so far, the
layers are the arrows, thus the objects are the intermediate products
obtained after passing through the layers. Of course, we will be most
interested in the green circles above, which are the code vectors we are
looking for, and not so much in the final predictions. Not that the task
of predicting function names is uninteresting, but it is not related to
our interests. We only want the code vectors in order to pass them on to
our classifier to determine the likelihood of containing security
vulnerabilities.

Fortunately enough, `code2vec` offers pre-trained models and others that
can be further trained. So on my to-do list, the top priority now is to
figure out how this works in detail and how to remove the final layer,
the one that gives the prediction, and just keep the vectors. If that
sounds interesting, stay tuned to our blog.

## References

1. U. Alon, M. Zilberstein, O. Levy, and E. Yahav. [code2vec: Learning
    Distributed Representations of
    Code](https://urialon.cswp.cs.technion.ac.il/wp-content/uploads/sites/83/2018/12/code2vec-popl19.pdf)
    Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 40. January
    2019.

2. Z. Chen and M. Monperrus. *A literature study of embeddings on
    source code.* [arXiv](https://arxiv.org/pdf/1904.03061.pdf).
