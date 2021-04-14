---
id: reproducibility
title: Transparency matters
sidebar_label: Reproducibility
slug: /machine/scanner/reproducibility
---

Everything at [Fluid Attacks](https://fluidattacks.com) is
[Open Source](https://opensource.com/resources/what-open-source).
This means that you can download, inspect, modify and enhance the source code that powers it all. Everything is an open book that anyone can read and verify.

Going Open Source gives our customers the confidence that what we do is
[transparent](https://fluidattacks.com/about-us/values/) and
[secure](https://fluidattacks.com/security/).

In order to verify the OWASP benchmark results we'll need to:
1.  Be in a x86_64-linux system in user space with sudo access to root
    (Debian/ubuntu distributions normally already have this).

    ```bash
    $ uname -mo
    x86_64 GNU/Linux
    $ whoami
    fluid
    $ sudo whoami
    root
    ```

1.  Install nix as explained in the
    [Nix's download page](https://nixos.org/download).

    ```bash
    $ nix --version
    2.3.10
    ```

1.  Get a copy of our source code.
    In this tutorial we will clone it into ~/Downloads/product.,
    any folder owned by your user should work:

    ```bash
    $ git clone https://gitlab.com/fluidattacks/product fluidattacks
    $ cd fluidattacks
    ```

1.  Execute:

    ```bash
    $ ./m skims.owasp-benchmark
    ```

    This will:
    - Build and setup our vulnerability detection tool and its dependencies
    - Download the version 1.2 of the
      [OWASP Benchmark source code](https://github.com/OWASP/Benchmark)
    - Configure and execute the vulnerability detection tool to target
      the benchmark's source code
    - Report the score and results back to you

    The output is going to be something similar to this:

    ```
    [INFO] Computing score
    [INFO] false_negatives: 0
    [INFO] false_positives: 0
    [INFO] true_negatives: 1325
    [INFO] true_positives: 1415
    [INFO] true_positives_rate: 1.0
    [INFO] false_positives_rate: 0.0
    [INFO] score: 100.0
    ```
