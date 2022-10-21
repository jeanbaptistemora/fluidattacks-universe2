---
id: skims
title: Skims
sidebar_label: Skims
slug: /development/skims
---

Skims is the product responsible
for the security vulnerability scanner
used in the [Machine's Scanner](/machine/scanner).
It is configured to analyze the desired attack surface,
and then it produces detailed reports
with the security vulnerabilities found.

## Public Oath

1. Skims has a low rate of [False Positives](https://en.wikipedia.org/wiki/Binary_classification),
   meaning that it only reports vulnerabilities that have an impact.
1. When deciding between a False Positive and a False Negative,
   Skims will favor the False Negative.

   In other words,
   it favors failing to report a vulnerability that has a real impact
   over reporting a vulnerability that has no impact.
   The rationale for this is that the [Squad Service](/squad/reattacks)

## Architecture

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Skims](./skims-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.

### Development Environment

Follow the steps
in the [Development Environment](/development/setup) section of our documentation.

When prompted for an AWS role, choose `dev`,
and when prompted for a Development Environment, pick `skims`.

### Local Environment

Just run:

```sh
universe $ m . /skims
```

This will build and run the Skims CLI application,
including the changes you've made to the source code.
