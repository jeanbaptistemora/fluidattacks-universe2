# Introduction

## About Skims

Skims is a vulnerability scanner tool.
This means it scans your source-code and applications and shows you the security
problems it have.

Skims is able to constantly monitor the security state of your system.
It opens new security findings as they are introduced,
and closes security findings once they are no longer present in the system.

At all moments you can read awesome reports and analytics at Integrates:

- Description of the vulnerability

  ![docs_integrates_description](https://gitlab.com/fluidattacks/product/-/raw/master/skims/static/img/docs_integrates_description.png)

- Evidence that the vulnerability exists

  ![docs_integrates_evidences](https://gitlab.com/fluidattacks/product/-/raw/master/skims/static/img/docs_integrates_evidences.png)

- Aggregated analytics

  ![docs_integrates_analytics](https://gitlab.com/fluidattacks/product/-/raw/master/skims/static/img/docs_integrates_analytics.png)

- And many more features!

## Quick Start

1.  Install Nix as explained in the [tutorial](https://nixos.org/download.html).
1.  Run the following command:

    `nix-env -i product -f 'https://gitlab.com/fluidattacks/product/-/archive/master/product-master.tar.gz'`

1.  You should be able to execute skims now:

    `skims --help`

1. Should you wish to uninstall please run:

    `nix-env -e product`
