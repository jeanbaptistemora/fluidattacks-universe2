---
slug: vulnerabilities-in-deep/
title: Vulnerabilities in Deep Learning
date: 2019-09-23
category: machine-learning
subtitle: Deep Learning for vulnerability disclosure
tags: machine-learning, detect, software
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331140/blog/vulnerabilities-in-deep/cover_ihaxpf.webp
alt: Photo by Franki Chamaki on Unsplash
description: In this blog post, we discuss an article from Boston University
  that presents new applications of Artificial Intelligence
  in the security field.
keywords: Machine Learning, Deep Learning, Detection, Vulnerability, Code, AI,
  Ethical Hacking, Pentesting
author: Oscar Uribe
writer: oscardjuribe
name: Oscar Uribe
about1: Software and Computer Engineering undergrad student
about2: '"Behind every successful Coder there is an even more successful
  De-coder to understand that code." Anonymous'
source: https://unsplash.com/photos/z4H9MYmWIMA
---

Currently, data scientists have begun using `AI` (Artificial
Intelligence) algorithms to solve problems from the data perspective.
Data scientists have been working on problems related to areas like
medicine, data mining, robotics, etc.

Some researches have been exploring how Artificial Intelligence can be
used in cybersecurity. For example, how we can use Artificial
Intelligence for vulnerability detection inside source code.

Most vulnerabilities are a result of using bad practices at the time of
programming. When these vulnerabilities are not detected in a timely
manner, they can later be discovered and exploited by attackers. So, it
is important to detect vulnerabilities in the early stages of a system’s
development.

There are tools that can perform static analysis of the source code.
These tools check the source code for problems without the need for
compiling and executing it. There are also dynamic analysis tools that
send information to the system inputs with presets or random values in
order to check for failures or improper exceptions handling.

## Initial Thoughts

In a Boston University [article](https://arxiv.org/pdf/1807.04320.pdf),
the authors discuss the possibility of using Artificial Intelligence and
algorithms for Deep and Machine Learning to automatically detect source
code vulnerabilities. The idea stems from the fact that there is a large
amount of open-source code available to be analyzed. After all, code is
just text and it is possible to use data mining algorithms on source
code to extract training data.

Static and dynamic code analyzers do not get the most out of source
code. The algorithms that they use are based on preset rules that do not
take into account small variations in the original rule. The result is
that some vulnerabilities and failures may remain undiscovered.

The purpose of this exercise was to use data mining, and deep and
machine learning techniques to automate a process frequently susceptible
to human errors, which can then result in unnoticed vulnerabilities in
applications or within operating systems. These unnoticed
vulnerabilities may then be exploited by hackers.

## Data

For data, they used `C` and ` C`` ` codes from different sources, such
as `SATE IV Juliet Test Suite`, a code recompilation used for test cases
that contains some known vulnerabilities, code from `Debian`
distributions, and some `GitHub` public repositories.

<div class="imgblock">

![Vulnerable code distribution.](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331139/blog/vulnerabilities-in-deep/code-distribution_c8mxlz.webp)

<div class="title">

Figure 1. Vulnerable code distribution
[\[1\]](https://arxiv.org/pdf/1807.04320.pdf).

</div>

</div>

## Labeling

In labeling, a custom lexer was created to capture only the important
information and label the rest as generic. The labels already provided
by the test database were used. For the `Debian` and `GitHub` codes,
they used dynamic analyzers in order to search outputs that later could
be interpreted by security professionals as one of the known
vulnerabilities from the Common Weakness Enumeration (`CWE`) list. Also
in the `GitHub` repositories, they searched inside the commits, words
like *“buggy”*, *“error”*, *“fixed”*, *“broken”*, and others, in order
to classify each block of source code as vulnerable or non-vulnerable.

<div class="imgblock">

![Found vulnerabilities.](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331139/blog/vulnerabilities-in-deep/found-vulnerabilities_ygqecc.webp)

<div class="title">

Figure 2. Statistics CWE vulnerabilities detected
[\[1\]](https://arxiv.org/pdf/1807.04320.pdf).

</div>

</div>

## Feature Extraction

In the feature extraction step, two types of [Neural
Networks](../crash-course-machine-learning/#artificial-neural-networks-and-deep-learning)
were tried,
[`CNN`](https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53)
(Convolutional Neural Network) and
[`RNN`](https://towardsdatascience.com/recurrent-neural-networks-d4642c9bc7ce)
(Recurrent Neural Network).

Despite the neural network working fine for the data extraction used by
the model, classification was not the best. To solve that, after the
Neural Networks feature extraction was made, they passed the output
through a [Random
Forest](https://towardsdatascience.com/understanding-random-forest-58381e0602d2)
classifier. They then obtained better results and avoided overfitting.

<div class="imgblock">

![Convolutional Neural Model](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331138/blog/vulnerabilities-in-deep/model_wrrngs.webp)

<div class="title">

Figure 3. Convolutional Neural Network Model and Random Forest
[\[1\]](https://arxiv.org/pdf/1807.04320.pdf).

</div>

</div>

## Results

Vulnerability detection using Data mining, and [Deep and Machine
Learning](../deep-hacking/) added some advantages compared with lexical
analyzers since they do not need to be compiled to work, and they can be
adjusted to obtain the desired precision.

Static analyzers have a limited number of findings because of preset
rules and the fact that they do not take into account the variations of
the rules. Static analyzers only identify a small portion of the real
vulnerabilities present in the source code.

<div class="imgblock">

![Detections](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331138/blog/vulnerabilities-in-deep/detections_kktube.webp)

<div class="title">

Figure 4. Detection of vulnerabilities
[\[1\]](https://arxiv.org/pdf/1807.04320.pdf).

</div>

</div>

This algorithm can underline code blocks that might introduce a
vulnerability. This allows suggestions that can be used to solve
problems. It can also simply notify the person in charge to determine
whether there is a vulnerability present or not.

## Conclusions

[Deep and Machine Learning](../deep-hacking/) techniques are used to
problem-solve from a different perspective, the perspective of the data.
The previous article illustrates several functions where using
Artificial Intelligence in security is helping to automate functions
previously done by humans. Using Artificial Intelligence allows humans
to focus on the analysis of problems rather than their detection.

Before these tools can be widely used within the industry, they need
some improvement. However, they demonstrate the potential this type of
tool has during the process of vulnerability disclosure. It is also
important to evaluate the possibility of integrating them into
continuous software development via continuous integrations to detect
vulnerabilities in [early stages](../../services/continuous-hacking/)
and avoid the spread of known security issues on latter versions of the
system.

## References

1. [Russell et al. (2018). Automated Vulnerability Detection in Source
    Code Using Deep Representation
    Learning](https://arxiv.org/pdf/1807.04320.pdf).

2. [Saha (2018). A Comprehensive Guide to Convolutional Neural
    Networks — the ELI5
    way](https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53).

3. [Venkatachalam (2019). Recurrent Neural
    Networks](https://towardsdatascience.com/recurrent-neural-networks-d4642c9bc7ce).

4. [Yiu (2019). Random
    Forest](https://towardsdatascience.com/understanding-random-forest-58381e0602d2).
