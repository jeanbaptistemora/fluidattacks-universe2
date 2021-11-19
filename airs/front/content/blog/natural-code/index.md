---
slug: natural-code/
title: Natural Code
date: 2019-07-26
subtitle: Natural language processing for code security
category: machine-learning
tags: machine-learning, vulnerability, code
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330956/blog/natural-code/cover_vftkoh.webp
alt: 'Photo by Andres Urena on Unsplash. Credits: https://unsplash.com/photos/k1osF_h2fzA'
description: In this blog post, we present the use of Natural Language
  Processing in bug finding and coding conventions,
  both based upon the n-gram model.
keywords: Machine Learning, Vulnerability, Natural Language Processing,
  N-gram, Predict, Bug, Pentesting, Ethical Hacking
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/k1osF_h2fzA
---

Our return to the [Machine Learning (`ML`) for secure code
series](../tags/machine-learning) is [a bit of a
digression](../binary-learning), but one too interesting to resist. It
is not too far a digression though, because the [Natural Language
Processing](https://en.wikipedia.org/wiki/Natural_language_processing)
(`NLP`) field is also part of what [is
currently](https://en.wikipedia.org/wiki/AI_effect) considered to be
[Artificial
Intelligence](https://en.wikipedia.org/wiki/Artificial_intelligence).
And, as we will state in this article, it has great potential for
applications in information security.

Basically, every cell phone currently in use employs a predictive
keyboard. Besides completing words for you based on the first few
letters, they are also able to suggest entire words after you have
written some. And some of these combinations just make sense because
they are used more frequently in common phrasing. Certainly, "peanut" is
more likely to be followed by "butter" than "wrench". Extending that
idea to more words, such as "peanut butter and jelly" we see they are
definitely more likely to be followed by "sandwich" than "salad". The
same holds true for "star" followed by "trek", as seen in this demo for
the [Android Predictive
Keyboard](https://proandroiddev.com/android-predictive-keyboard-e6c9df01e527):

<div class="imgblock">

![Android Predictive Keyboard demo animation](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330955/blog/natural-code/ngram-keyboard_xogjer.gif)

<div class="title">

Figure 1. An n-gram based predictive keyboard at work

</div>

</div>

This is the basic idea behind *n*-gram analysis, a technique we have
mentioned before in passing. It has been applied to a couple of the
`ML`-powered vulnerability detectors we have discussed, most notably by
the binary static analysis tool [VDiscover](../binary-learning/).

An *n*-gram is simply a sequence of *n* consecutive words occurring in a
piece of real text, which we use as a basis for training. This text is
called a *corpus* in the Natural Language Processing context. This
training essentially consists of:

- Extracting all the possible *n*-grams in the corpus taking
  punctuation into account, so that "now. But before" will not be
  considered a valid 3-gram.

- Counting the occurrence of each *n*-gram vs the total, i.e., finding
  the relative frequency of each.

That’s it\! Now if you see "peanut butter and jelly", we look at all the
5-grams that contain this 4-gram, and see which one has the highest
relative frequency. Suppose the "peanut butter and jelly sandwich"
occurs the most in our training corpus. Then the first suggested word to
come after the given 4 is, of course, "sandwich", rather than "wrench".

If the corpus is good enough regarding the context in which such words
appear, then the suggestions should be just as good. The quality of
results, and hence the accuracy of our classifier, is highly dependent
on the training corpus' quality. Cell phone predictive keyboards exploit
this fact by learning from your typing habits. Depending on who you are
"machine" might be more likely followed by "shop", "head" or "learning".

If all this can be done on *natural* language, which has all sorts of
ambiguities, mistakes in the training corpus, irregularities, etc,
imagine what could be done if we applied this same idea to code, which
is highly regular, ordered and syntactically strict? The possible
applications are promising.

- Automatically complete code like the text above.

- Finding bugs in code via n-gram analysis.

- Make code more natural by enforcing coding conventions, i.e. a
  special kind of linting.

- Generate pseudo-code or documentation automatically.

Of course, all these applications require, as do the ones we have
previously presented, a useful representation of code in a way that it
is always referred to as "machine learning" algorithms. This comes as no
surprise if you have been following our previous series. The methods
chosen for this particular application are Abstract Syntax Trees, and an
adaptation of `word2vec` for code, aptly named `code2vec`.

With representation out of the way, let’s dive into the actual methods.
The main idea behind bug finding via n-gram analysis is to decompose
every function into n-grams that represent their elements, such as `API`
calls, variable names, etc. Then, compare them to one another for
similarity. If we find rare (with low-occurrence frequency) n-grams that
are highly similar to common (high-occurrence frequency) code, then the
rare ones are probably buggy and worthy of further analysis. Take for
example the following snippets from [Apache
Pig](https://pig.Apache.org).

<div class="imgblock">

![Snippets found by Bugram](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330955/blog/natural-code/bugram-pig_vjk4cc.webp)

<div class="title">

Figure 2. Snippets found by Bugram

</div>

</div>

The above snippet is buggy due to the lack of `toString`. In fact, it is
exactly the same as the other snippet, only without `toString`. `Bugram`
suggested it as a possible bug because it was so similar to a commonly
occurring snippet. The bug was reported to the `Pig` team and confirmed.
In the test proposed by the paper, `Bugram` was able to find 42
confirmed bugs plus 17 false positives across 16 well-known open source
`Java` projects such as `Pig`.

This approach, while simple and effective, is not without drawbacks,
namely, that the weapon cannot be focused on security-related bugs or
any specific kind of bug. The same authors later proposed an approach
based on [deep learning](../deep-hacking) rather than *n*-grams, but
again with the same aim of predicting sofware *defects* in general.

Another possible application of *n*-gram analysis that might indirectly
contribute to writing more secure code follows the idea that "cleaner
code leads to secure code". If a person’s writing style can be learned
by *n*-gram analysis, the same can be true of a particular coder’s
style, or even a whole software project. Take for example our very last
Asserts closure checker engine. Not only do we stick to the `Python`
guidelines when naming variables and methods, and separating words by
underscores, we also have a particular way of naming functions.

**Sample function names from `Asserts`.**

``` python
fluidasserts.proto.http.can_brute_force
fluidasserts.proto.http.has_dirlisting
fluidasserts.proto.smb.is_anonymous_enabled
fluidasserts.cloud.aws.iam.has_not_support_role
```

Do you see a tendency here? So did
[`Naturalize`](http://groups.inf.ed.ac.uk/naturalize/#), a project that
tries to "learn natural coding conventions" in order to improve naming
suggestions. The goal is to infer a good name for a function given its
code. That is to say, if I know what it does, I should be able to know
what its name is, assuming that the names are not entirely random or
[humorously
unmaintainable](https://www.se.rit.edu/~tabeec/RIT_441/Resources_files/How%20To%20Write%20Unmaintainable%20Code.pdf).

Behind the scenes `Naturalize` uses natural language processing
techniques, such as *n*-gram analysis to suggest more *natural-sounding*
names to identifiers. This is the one place where developers can get
creative, perhaps affecting the overall readability or fitting into
project conventions. The package can be integrated in the development
pipeline such as a `pre-commit` hook or during developing as an
`Eclipse` plugin.

<div class="imgblock">

![humorously unmaintainable](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330955/blog/natural-code/naturalize-eclipse_qynobj.webp)

<div class="title">

Figure 3. Naturalize Eclipse plugin at work.

</div>

</div>

As can be seen here `each` is not considered to be a very descriptive or
convention-conforming name, so `testClass` is suggested as a better
alternative.

---
Natural Language Processing has moved beyond the "natural language" line
and is moving increasingly into the "machine learning" or "artificial
intelligence" arena. Natural Language Processing will soon have a wider
scope of purposes, such as static code analysis, bug finding, and
potentially, vulnerability detection. In the future, we are more likely
to encounter more applications of NLP in the least expected places.

## References

1. S. Wang, D. Chollak, D. Movshovitz-Attias, and L. Tan. *Bugram: Bug
    detection with N-gram Language Models*.
    [ASE 2016](https://ece.uwaterloo.ca/~s446wang/paper/ase-16-1.pdf).

2. M. Allamanis, E. Barr, C. Bird, C. Sutton. *Learning Natural Coding
    Conventions*. [arXiv](https://arxiv.org/pdf/1402.4182.pdf).
