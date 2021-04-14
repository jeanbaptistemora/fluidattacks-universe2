---
id: our-score
title: OWASP Benchmark at Fluid Attacks
sidebar_label: Our score
slug: /owasp-benchmark/our-score
---

At [Fluid Attacks](https://fluidattacks.com)
we decided to test our primary automated software vulnerability detection tool,
this solution is included in all of our [plans](https://fluidattacks.com/plans/)
of the [Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/) service.

Long story short, this is how we compare to other vulnerability detection tools:

![Fluid Attacks Score](/img/owasp-benchmark/our-score/fluid-attacks-score.png)

# Transparency matters

Everything at [Fluid Attacks](https://fluidattacks.com) is
[Open Source](https://opensource.com/resources/what-open-source).
This means that you can download, inspect, modify and enhance the source code that powers it all. Everything is an open book that anyone can read and verify.

Going Open Source gives our customer the confidence that what we do is
[transparent](https://fluidattacks.com/about-us/values/) and
[secure](https://fluidattacks.com/security/).

In order to verify the OWASP benchmark results we'll need to:
1.  Be in a x86_64-linux system in user space with sudo access to root
    (Common debian/ubuntu distributions should have this already).

1.  Install nix as explained in the
    [Nix's download page](https://nixos.org/download).

1.  Get a copy of our source code:

    `$ git clone https://gitlab.com/fluidattacks/product.git`

    And locate yourself inside the root of the repository:

    `$ cd product`

1.  Execute:

    `$ ./m skims.owasp-benchmark`

    This will:
    - Build and setup our vulnerability detection tool and its dependencies
    - Download the version 1.2 of the
      [OWASP Benchmark](https://github.com/OWASP/Benchmark source code)
    - Configure and execute the vulnerability detection tool to target
      the benchmark's source code
    - Report the score and results back to you
