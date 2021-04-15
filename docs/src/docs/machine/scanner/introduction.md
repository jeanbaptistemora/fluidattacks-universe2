---
id: introduction
title: Introduction
sidebar_label: Introduction
slug: /machine/scanner
---

Fluid Attacks' scanner is a security vulnerability detection tool.
This means it scans your source-code, infrastructure and applications and reports
to you the security problems they have.

Fluid Attacks' scanner is able to constantly monitor the security state of your system.
It opens new security findings as they are introduced,
and closes security findings once they are no longer present in the system.

At all moments you can read awesome reports and analytics at Fluid Attack's App:

- Description of the vulnerability

  ![description](/img/machine/scanner/introduction/description.png)

- Evidence that the vulnerability exists

  ![evidences](/img/machine/scanner/introduction/evidences.png)

- Aggregated analytics

  ![analytics](/img/machine/scanner/introduction/analytics.png)

- And many more features!

## Requirements

1.  A x86_64-linux system:

    ```bash
    $ uname -mo
    x86_64 GNU/Linux
    ```

1.  Bash v5, installed as explained in the
    [Bash's download page](https://www.gnu.org/software/bash/#download).

1.  Curl v7, installed as explained in the
    [Curl's download page](https://curl.se/download.html).

1.  Nix v2, installed as explained in the
    [Nix's download page](https://nixos.org/download).

## Installing

1.  Run the following command:

    `$ bash <(curl -L "https://fluidattacks.com/install/skims")`

1.  You should be able to execute the scanner now:

    `$ skims --help`
