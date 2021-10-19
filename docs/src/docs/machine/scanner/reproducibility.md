---
id: reproducibility
title: Reproducibility
sidebar_label: Reproducibility
slug: /machine/scanner/reproducibility
---

Everything at [Fluid Attacks](https://fluidattacks.com)
is [Open Source](https://opensource.com/resources/what-open-source).
This means that you can download,
inspect, modify and enhance the
[source code](https://gitlab.com/fluidattacks/product)
that powers it all.

Going Open Source
gives our customers the confidence
that what we do is
[transparent](https://fluidattacks.com/about-us/values/)
and [secure](https://docs.fluidattacks.com/about/security/).

In order to verify
the OWASP benchmark results
we'll need to:

1. Meet the
    [requirements for installing Fluid Attacks' scanner](/machine/scanner/plans/foss#requirements).

1. Install the scanner
    as explained in the
    [Fluid Attack's scanner installation guide](/machine/scanner/plans/foss#installing).

1. Clone the **OWASP Benchmark 1.2**.

    We are using a Fluid Attack's fork
    in order to add support
    for parsing the scanner results.

    ```bash
    git clone https://github.com/fluidattacks/Benchmark.git benchmark
    cd benchmark
    ```

    There is an open
    [pull request](https://github.com/OWASP-Benchmark/BenchmarkJava/pull/146)
    at the OWASP Benchmark official repository
    in order to add support natively.

1. Create a config file as follows:

    ```yaml title="config.yaml"
    checks:
    - F004
    - F008
    - F021
    - F034
    - F042
    - F052
    - F063
    - F089
    - F107
    - F112
    namespace: OWASP
    output: results/Benchmark_1.2-Fluid-Attacks-v2021.csv
    path:
      include:
      - .
    ```

1. Execute:

    ```bash
    m f /skims scan config.yaml
    ```

    This will take some time,
    enough for drinking a coffee &#x2615;.

    When this ends,
    the results file will be located
    in the results/ folder
    with the name of Fluid Attacks
    and CSV extension.

1. At this point you can generate
    a scorecard for the tool:

    ```bash
    mvn compile
    ./createScorecards.sh
    ```

1. Open the results in your browser.

    Example:

    ```bash
    firefox scorecard/OWASP_Benchmark_Home.html
    ```

    Or:

    ```bash
    google-chrome-stable scorecard/OWASP_Benchmark_Home.html
    ```
