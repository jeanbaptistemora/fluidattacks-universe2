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

## Updating

No actions are required from you.

Updates are rolled out automatically to your machine
with a delay of at most 1 day.
But anyway,
if you want to force an update right away,
just run `$ rm -rf ~/.cache/makes`

## Troubleshooting

### General considerations

1. A stable internet connection is required
1. A stable DNS resolver is required. Please consider using:
    - IPv4: `1.1.1.1`, `8.8.8.8`, `8.8.4.4`
    - IPv6: `2001:4860:4860::8888`, `2001:4860:4860::8844`

### Checklist

If the installation failed while installing Nix (step 1):

1. Checkout the
    [Nix manual](https://nixos.org/manual/nix/stable/#chap-installation)
    for more detailed installation instructions.
1. If the problem persists,
    please let us know at help@fluidattacks.com.

If the installation failed while installing Makes (step 2):

1. Please let us know at help@fluidattacks.com.

If the installation failed while using `$ m gitlab:xxx /yyy` (step 3):

1. Repeat step two (installing Makes) and try again.

1. Refresh the cache: `$ rm -rf ~/.cache/makes` and try again.

1. If the problem persists,
    please let us know at help@fluidattacks.com.
