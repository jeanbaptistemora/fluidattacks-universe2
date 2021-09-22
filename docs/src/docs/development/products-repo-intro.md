---
id: products-repo-intro
title: Introduction
sidebar_label: Introduction
slug: /development
---

## Who we are

We are a
[cyber-security company](https://fluidattacks.com)
whose only purpose is
to make the world a safer place.

## What we do

- We perform comprehensive security testing
    over all of your assets.
- We use cutting edge technologies
    and heavily trained **human hackers**.
- We report vulnerabilities back to you
    as accurate and fast as possible.

The source code of the technologies used
is versioned in this repository
and is divided across many products.

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_product&metric=security_rating)](https://sonarcloud.io/dashboard?id=fluidattacks_product)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_product&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=fluidattacks_product)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_product&metric=sqale_index)](https://sonarcloud.io/dashboard?id=fluidattacks_product)
[![Code Grade](https://www.code-inspector.com/project/19186/score/svg)](https://www.code-inspector.com)

## Installing

1. Make sure that Nix is installed on your system.
    If it is not, please follow
    [this tutorial](https://nixos.org/download.html).

    If everything went well you should be able to run:

    ```bash
    $ nix --version
    ```

    We only support versions of Nix `>= 2.3` and `< 2.4`.

1. Install [Makes](https://github.com/fluidattacks/makes) with:

    ```bash
    $ curl -L fluidattacks.com/install/m | sh
    ```

    If everything went well you should be able to run:

    ```bash
    $ m
    ```

1. Use the products of your choice:

    ```bash
    $ m gitlab:fluidattacks/product@master /forces --help
    $ m gitlab:fluidattacks/product@master /melts --help
    $ m gitlab:fluidattacks/product@master /reviews --help
    $ m gitlab:fluidattacks/product@master /skims --help
    $ m gitlab:fluidattacks/product@master /sorts --help
    ```
