---
id: benchmark
title: Benchmark
sidebar_label: Benchmark
slug: /machine/scanner/benchmark
---

At Fluid Attacks,
we care about the accuracy of security testing results.
This means we want to make sure
that the automated tools and security analysts involved
make as few mistakes as possible in their reports.
To the purpose of checking tool accuracy,
Fluid Attacks uses the Benchmark
established by the [Open Web Application Security Project (OWASP)](https://owasp.org/).

The OWASP
is a non-profit foundation
committed to helping improve
software security.
It acts as an open,
online community where anyone
can contribute to the production of material
in the field of web application security
and benefit from the information available.

The [OWASP Benchmark Project](https://owasp.org/www-project-benchmark/)
is a free Java test suite
created in 2015 to assess the accuracy,
speed and coverage of automated
software vulnerability detection tools.
It helps determine the strengths
and weaknesses of different
application security testing programs
and allows objective comparisons between them.

By running different security testing tools
over the OWASP benchmark
we can put under evaluation different
open-source or commercial
static ([SAST](https://www.gartner.com/en/information-technology/glossary/static-application-security-testing-sast)),
dynamic ([DAST](https://www.gartner.com/en/information-technology/glossary/dynamic-application-security-testing-dast))
and interactive ([IAST](https://www.comparitech.com/net-admin/what-is-iast/))
software vulnerability detection tools.
A tool's score will depend on the amount of truthful
and erroneous claims
in its reports.
A truthful claim can be either a true positive or a true negative,
whereas an erroneous claim can be either a false positive or a false negative.

By comparing the results of different products
offered in the market,
we get an important indicator
for choosing what tool to include
in our software development lifecycle.
