---
id: products-repo-intro
title: Introduction
sidebar_label: Introduction
slug: /development
---

## Fluid Attacks, Products repository

We are a [cyber-security company](https://fluidattacks.com) whose only purpose is
to make the world a safer place

We do this by:
- Performing comprehensive security testing over all of your assets
- Using cutting edge technologies and heavily trained human hackers
- Reporting vulnerabilities back to you as accurate and fast as possible

The source code of the technologies used is versioned in this repository
and is divided across many products:

| Product | Badges |
|---------|-|
| Licence | [![License](https://img.shields.io/pypi/l/forces)](https://gitlab.com/fluidattacks/product/-/blob/master/LICENSE) |
| Documentation | [![Docs](https://img.shields.io/badge/Docs-grey)](https://doc.fluidattacks.com/) |
| Quality | [![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_product&metric=alert_status)](https://sonarcloud.io/dashboard?id=fluidattacks_product) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_product&metric=security_rating)](https://sonarcloud.io/dashboard?id=fluidattacks_product)[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_product&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=fluidattacks_product)[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_product&metric=sqale_index)](https://sonarcloud.io/dashboard?id=fluidattacks_product)[![Code Grade](https://www.code-inspector.com/project/19186/score/svg)](https://www.code-inspector.com) |
| Contributing | [![](https://img.shields.io/badge/Contributing-green)](https://gitlab.com/fluidattacks/product/-/blob/master/skims/README.md) |

## Installing

Most products are distributed as a standalone binary

Before proceeding make sure you have Nix installed in your system,
otherwise please install it as explained in the [tutorial](https://nixos.org/download.html)

You can install the products of your choice by using one or many of
the following commands:

- `bash <(curl -L fluidattacks.com/install/asserts)`
- `bash <(curl -L fluidattacks.com/install/forces)`
- `bash <(curl -L fluidattacks.com/install/melts)`
- `bash <(curl -L fluidattacks.com/install/reviews)`
- `bash <(curl -L fluidattacks.com/install/skims)`
- `bash <(curl -L fluidattacks.com/install/sorts)`

Once installed, you can test that they work by invoking the product
like `skims --help`, `forces --help`, and so on

You can see installed software with: `nix-env -q` and uninstall with: `nix-env -e`
