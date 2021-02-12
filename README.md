# Fluid Attacks, Products repository

We are a [cyber-security company](fluidattacks.com) whose only purpose is
to make the world a safer place

We do this by:
- Performing comprehensive security testing over all of your assets
- Using cutting edge technologies and heavily trained human hackers
- Reporting vulnerabilities back to you as accurate and fast as possible

The source code of the technologies used is versioned in this repository
and is divided across many products:

| Product | [![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_product&metric=alert_status)](https://sonarcloud.io/dashboard?id=fluidattacks_product) |
|---------|-|
| Forces  |[![Docs](https://img.shields.io/badge/Docs-grey)](./forces/README.md) [![PyPI](https://img.shields.io/pypi/v/forces)](https://pypi.org/project/forces) [![Downloads](https://img.shields.io/pypi/dm/forces)](https://pypi.org/project/forces) [![License](https://img.shields.io/pypi/l/forces)](../LICENSE) |
| Integrates | [![Docs](https://img.shields.io/badge/Docs-grey)](./integrates/README.md) |
| Reviews | [![Docs](https://img.shields.io/badge/Docs-grey)](./reviews/README.md) |
| Skims | [![](https://img.shields.io/badge/Docs-grey)](https://fluidattacks.com/resources/doc/skims/) [![](https://img.shields.io/badge/Contributing-green)](./skims/README.md) |
| Sorts | [![](https://img.shields.io/badge/Docs-grey)](./sorts/README.md) |

# Installing

Most products are distributed as a standalone binary

Before proceeding make sure you have Nix installed in your system,
otherwise please install it as explained in the [tutorial](https://nixos.org/download.html)

You can install the products of your choice by using one or many of
the following commands:

- `bash <(curl -L fluidattacks.com/install/forces)`
- `bash <(curl -L fluidattacks.com/install/melts)`
- `bash <(curl -L fluidattacks.com/install/skims)`
- `bash <(curl -L fluidattacks.com/install/sorts)`

Once installed, you can test that they work by invoking the product
like `skims --help`, `forces --help`, and so on

You can see installed software with: `nix-env -q` and uninstall with: `nix-env -e`
