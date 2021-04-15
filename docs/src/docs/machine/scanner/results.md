---
id: results
title: Results
sidebar_label: Results
slug: /machine/scanner/results
---

At [Fluid Attacks](https://fluidattacks.com)
we decided to test our primary automated software vulnerability detection tool,
this solution is included in all of our [plans](https://fluidattacks.com/plans/)
of the [Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/) service.

Long story short, this is how we compare to other vulnerability detection tools:

![Fluid Attacks Score](/img/owasp-benchmark/our-score/fluid-attacks-score.png)

Statistically the results can be divided into the following groups:
- **True positives**: Real impacts to your business reported by the tool

  Very nice! this is what you are looking for
- **False negatives**: Real impacts to your business not reported by the tool

  Undesirable: the tool fails to identify vulnerabilities.
  This gives you a false sense of security and you will
  likely deploy undiscovered vulnerabilities to production
- **False positives**: False impacts to your business reported by the tool

  Undesirable: the tool makes you waste time in filtering the false information out
- **True negatives**: False impacts to your business correctly omitted by the tool

  very nice! you don't want a tool lying to you

![Sensitivity and Specificity](/img/owasp-benchmark/our-score/results-categories.png)

In the OWASP Benchmark this is measured with two key values:
- **True Positives Rate (TPR)** also known as **sensitivity**:
  How much of the vulnerable code is reported to you
- **False Positives Rate (FPR)** also known as **specificity**:
  How much of the safe code is identified as really safe

![Sensitivity and Specificity](/img/owasp-benchmark/our-score/sensitivity-and-specificity.png)

Statistically you can compare different tools by using the
[Youden's J statistic](https://en.wikipedia.org/wiki/Youden%27s_J_statistic):

![Sensitivity and Specificity](/img/owasp-benchmark/our-score/youdens-index.svg)

When our automated vulnerability detection tool is run over the code of the
[OWASP Benchmark](https://github.com/OWASP/Benchmark),
we score a clean 100% True Positives Rate and 0% False Positives Rate.

This accounts for a total **OWASP Benchmark Score of 100%**,
four times higher than the commercial (paid) average score in the study,
and more than two times higher than the best non-commercial (free)
vulnerability detection tool.

What is most important,
[Fluid Attacks](https://fluidattacks.com) cares about what you care:
- Finding all the vulnerabilities before they impact your business
- Keeping your team fast with zero false positives
