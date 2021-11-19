---
slug: machine-learning-hack/
title: Machine-Learning to Hack
date: 2018-11-07
subtitle: Machine learning for vulnerability discovery
category: machine-learning
tags: machine-learning, vulnerability, discovery
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330936/blog/machine-learning-hack/cover_q6ydtc.webp
alt: Can machines learn to hack?
description: This post is a bird's eye view of machine learning techniques
  applied to vulnerability discovery in source code, reviewing papers
  from 2011 to 2018.
keywords: Machine Learning, Vulnerability, Anomaly Detection,
  Pattern Recognition, Deep Learning, Security, Ethical Hacking, Pentesting
author: Rafael Ballestas
writer: raballestasr
name: Rafael Ballestas
about1: Mathematician
about2: with an itch for CS
source: https://unsplash.com/photos/iar-afB0QQw
---

To date the [most](../libssh-bypass-cve/)
[important](../treacherous-poodle/) [security](../release-the-beast/)
[vulnerabilities](../my-heart-bleeds/) have been found via laborius code
auditing. Also, this is the only way vulnerabilities can be found and
fixed during development. However, as software production rates
increase, so does the need for a reliable, automated method for checking
or classifiying this code in order to prioritize and organize human
efforts in manual checks. We’re living in an age where machine learning
is [playing
well](https://www.forbes.com/sites/forbestechcouncil/2018/09/27/15-business-applications-for-artificial-intelligence-and-machine-learning/#1ac831c579f2)
in several other technological fields, how about applying it to our
bug-finding appetite?

In this and upcoming articles, we are interested in the use of machine
learning (`ML`) techniques to find security vulnerabilities in source
code. It is important to specify this since, as we will see, there are
many other related, but different, approaches such as:

- Automatically fixing vulnerabilities

- Vulnerability detection (`VD`) in binary code

- `ML`-aided dynamic testing

- Other automated techniques that don’t involve `ML`

- Exploitability prediction

The idea of using `ML` techniques for `VD` is not new. There are papers
on the matter as old as 2001. Here we’ll try to describe in simple
terms:

- what has been done in this area,

- what the current state-of-the-art is and

- try to ellucidate new research paths.

We will be following and building on top of two previous
state-of-the-art papers

We feel the grouping by semantic features extracted from code approach
makes more sense, as do Ghaffarian and Shahriari
(2017)[<sup>\[2\]</sup>](#r2%20), These are further subdivided into:

- Vulnerable code pattern recognition. Usually based on labeled data
  (samples of faulty and safe code) determine patterns that explain
  that, and

- Anomaly detection. This means, based upon a large code base, extract
  models of what "normal code" should look like and determining pieces
  of code that do not fit in with this model.

## Anomaly detection approaches

Most of the papers in this category are not security-focused, but their
ideas can be used for `VD`. Also most of these works revolve around
extracting features such as:

- proper `API` usage patterns, v.g. the pair `malloc` and `free`,

- missing checks, like ensuring a number is non-zero before dividing
  by it,

- lack of input validation, leading to injections, buffer overflows,
  …​

- lack of access controls, which may lead to confidential information
  being leaked, altered or denied access to.

The system [Chucky](../anomaly-serial-killer-doll/) by [Yamaguchi et al.
(2013)](https://user.informatik.uni-goettingen.de/~krieck/docs/2013-ccs.pdf)
is the one that interests us the most since it is more compatible with
our interests, i.e., lightening the burden of manual code auditors;
also, they achieve both the aforementioned objectives: detecting missing
checks through security logic (v.g. access control) and secure `API`
usage (v.g. checking buffer size). It uses the
[bag-of-words](https://en.wikipedia.org/wiki/Bag-of-words_model) model
to represent the code and the
[k-nearest-neighbors](../crash-course-machine-learning/#anomaly-detection-via-k-nearest-neighbors)
technique to analyze it. 'Chucky' discovered 12 new vulnerabilites in
high-profile projects such as [Pidgin](https://pidgin.im/) and
[LibTIFF](http://libtiff.org/). See our [article on
Chucky](../anomaly-serial-killer-doll) for details.

A year later, [Yamaguchi et al.
(2014)](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6956589)
reuse this idea of [exploiting graph representations of
code](../exploit-code-graph/) in order to find vulnerable code patterns.
This time they propose automating the design of effective traversals
which might lead to vulnerability detection using the unsupervised
[clustering](../crash-course-machine-learning/#k-means-clustering)
approach. This resulted in the tool
['Joern'](http://www.mlsec.org/joern/), which was able to find 5
zero-day vulnerabilities in products like Pidgin.

Most of the papers in this category are not security focused. All of
them use [frequent itemset
mining](https://en.wikipedia.org/wiki/Association_rule_learning), only
with different features to mine and different targets to extract. We
summarize them here for the sake of completeness:

<div class="tc">

**Table 1. Other anomaly-seeking approaches**

</div>

| Paper                                                                                                                          | Mined elements                   | Target                              |
| ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- | ----------------------------------- |
| <p> [Livshits and Zimmermann (2005)](http://www.doc.ic.ac.uk/~livshits/papers/pdf/dynamine_ext.pdf)                       </p> | <p> Commit logs             </p> | <p> App-specific patterns      </p> |
| <p> [Li and Zhou (2005)](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/PRMiner.pdf)                               </p> | <p> Source code             </p> | <p> Implicit coding rules      </p> |
| <p> [Wasylowski et al. (2007)](https://www.st.cs.uni-saarland.de/edu/recommendation-systems/papers/p35-wasylkowski-1.pdf) </p> | <p> Function call sequences </p> | <p> Object usage models        </p> |
| <p> [Acharya et al. (2007)](https://www.cs.sfu.ca/~jpei/publications/APIMining_FSE07.pdf)                                 </p> | <p> `API` usage traces      </p> | <p> `API` usage orderings      </p> |
| <p> [Chang et al. (2008)](https://www.computer.org/csdl/journal/ts/2008/05/tts2008050579/13rRUxAAT2W)                     </p> | <p> Neglected conditions    </p> | <p> Implicit conditional rules </p> |
| <p> [Thummalapenta et al (2009)](https://link.springer.com/article/10.1007/s10515-011-0086-z)                             </p> | <p> Programming rules       </p> | <p> Alternative patterns       </p> |
| <p> [Gruska et al (2010)](https://www.st.cs.uni-saarland.de/publications/files/gruska-issta-2010.pdf)                     </p> | <p> Function calls          </p> | <p> Cross-project anomalies    </p> |

In general terms, anomaly detection approaches have the following
limitations:

- they only apply to mature software, where we assume wrong `API`
  usage are rare occurrences,

- that particular usage must be relatively infrequent in the codebase
  to be identified as an anomaly (otherwise the rule becomes the
  norm),

- they generally cannot identify the type of the vulnerability, or
  even 'if' the anomaly is a security vulnerability, only that it is a
  deviant element, and

- false-positive rates are generally high.

## Pattern recognition approaches

The aim is to take a large dataset of vulnerability samples and extract
vulnerable code patterns using (usually
[supervised](../crash-course-machine-learning/)) machine learning
algorithms. The key is the technique used for extracting features, which
range from convential [parsers](../pars-orationis-secura/), data-flow
and control-flow analysis, and even directly text mining the source
code. Most of these papers use
[classification](../crash-course-machine-learning/) algorithms.

Once more Yamaguchi et al.
([2011](https://media.blackhat.com/bh-us-11/Yamaguchi/BH_US_11_Yamaguchi_Vulnerability_Extrapolation_WP.pdf),
[2012](https://www.researchgate.net/publication/233997025_Generalized_Vulnerability_Extrapolation_using_Abstract_Syntax_Trees))
take the lead, mimicking the mental process behind the daily grind of
the code auditor: searching for similar instances of recently discovered
vulnerabilities. They sensibly call this 'vulnerability extrapolation'.
The gist: parse, embed into vector space via a bag-of-words-like method,
perform semantic analysis to obtain particular matrices, and then
compare to known-vulnerable code using standard [distance
functions](https://en.wikipedia.org/wiki/Similarity_learning).

Other approaches in this category are [Scandariato et al.
(2014)](https://core.ac.uk/download/pdf/34611720.pdf) and [Pang et al.
(2015)](https://ieeexplore.ieee.org/document/7424372), who attempted to
use techniques such as [n-gram](https://en.wikipedia.org/wiki/N-gram)
analysis using bag-of-words, but with limited results, probably due to
shallow information and simple methods.

The binary analysis tool [VDiscover](http://www.vdiscover.org/) doesn’t
exactly fit our definition, but deserves mentioning. They identify each
trace of a call to the standard `C` library as a text document and
process them as [n-grams](https://en.wikipedia.org/wiki/N-gram) and
encode them with [word2vec](https://en.wikipedia.org/wiki/Word2vec).
They have tested several `ML` techniques such as [logistic
regression](https://en.wikipedia.org/wiki/Logistic_regression),
[MLP](../crash-course-machine-learning/#artificial-neural-networks-and-deep-learning)
and [random forests](https://en.wikipedia.org/wiki/Random_forest).

In the last few months, some in-scope papers have appeared. Li et al.
propose two systems: [VulDeePecker
(2018a)](https://arxiv.org/pdf/1801.01681.pdf) and [SySeVR
(2018b)](https://arxiv.org/abs/1807.06756v2), which claim to extract
both syntactic and semantic information from the code, thus also
considering both data and control flow. They report good results with
low false positives and 15 zero-day vulnerabilities in high-profile open
source libraries. See our [article on these systems](../deep-hacking).

[Lin et al. (2017)](https://dl.acm.org/citation.cfm?id=3138840) propose
a different variant which simplifies the feature extraction, going back
to just `AST` with no semantic information, using [deep
learning](../crash-course-machine-learning/#artificial-neural-networks-and-deep-learning)
in the form of [bidirectional long short-term memory (BLSTM)
networks](https://en.wikipedia.org/wiki/Long_short-term_memory), plus a
completely new element: unlike the vast majority of previous works,
which work in the within-project domain, `POSTER` involves software
metrics (see below) in order to compare to other projects.

However interesting these approaches seem, they are not without
limitations:

- Most of these models aren’t able to identify the type of the
  vulnerability. They only recognize patterns of vulnerable code. This
  also means that most do not pinpoint the exact locations of the
  potential flaws.

- Any work in machine learning for `VD` should take into account
  several aspects of the code for richer descriptions, such as syntax,
  semantics and the flow of data and control.

- The quality of the results is believed to be mostly due to the
  features that are extracted and fed to the learning algorithms.
  Ghaffarian calls this 'feature engineering'. Features extracted from
  graph representations, according to them, have not been fully
  exploited.

- Unsupervised machine learning algorithms, especially deep learning,
  are underused, although this has started to change in recent years.

## Other approaches

Software metrics such as:

- [size](https://en.wikipedia.org/wiki/Source_lines_of_code) (logical
  lines of code),

- [cyclomatic
  complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity),

- [code churn](http://iedaddy.com/2017/09/devops-metrics-code-churn/)
  and

- developer activity

have been proposed as 'predictors' for the presence of vulnerabilities
in software projects. These studies use mostly manual procedures based
on publicly available vulnerability sources such as
[NVD](https://nvd.nist.gov/). According to [\[2\]](#r2%20) and [Walden
et al.
(2014)](https://faculty.cs.nku.edu/~waldenj/papers/issre2014-php-prediction.pdf),
predicting the existence of vulnerabilities based on software
engineering metrics could be thought of as a case of "confusing symptoms
and causes":

<div class="imgblock">

![Correlation vs causation. Via
.](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330935/blog/machine-learning-hack/correlation_bethz4.webp)

<div class="title">

Figure 1. Correlation vs causation. Via
[XKCD](https://imgs.xkcd.com/comics/correlation.png).

</div>

</div>

Hence, most papers reviewed in this category present high false positive
rates and hardly one of them has explored automated techniques.

---
That was the panorama of machine learning in software vulnerability
research as of late 2018. Some limitations that are common:

- The problem of finding vulnerabilities is 'undecidable' in view of
  [Rice’s theorem](https://en.wikipedia.org/wiki/Rice%27s_theorem),
  i.e., a universal algorithm for finding vulnerabilities cannot
  exist, since a program cannot identify semantic properties of
  another program in the general case.

- Limited applicability.

- Coarse granularity and lack of explanations.

- A higher degree of automation is desirable, not in order to replace,
  but to guide, manual code auditing. Purely automated approaches are,
  in view of Rice’s theorem, imposible or misguided.

Thus our good old [pentest is not dead](../importance-pentesting/). Even
at the level of cutting-edge research, automated vulnerability
discovery, and especially confirmation and exploitation, are tasks for
human experts.

## References

1. T. Abraham and O. de Vel (2017). 'A Review of Machine Learning in
    Software Vulnerability Research'.
    [DST-Group-GD-0979](https://www.dst.defence.gov.au/sites/default/files/publications/documents/DST-Group-GD-0979.pdf).
    Australian department of defence.

2. S. Ghaffarian and H. Shahriari (2017). [Software Vulnerability
    Analysis and Discovery Using Machine-Learning and Data-Mining
    Techniques: A Survey](https://dl.acm.org/citation.cfm?id=3092566).
    'ACM Computing Surveys (CSUR)' 50 (4)
