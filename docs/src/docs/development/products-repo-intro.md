---
id: products-repo-intro
title: Introduction
sidebar_label: Introduction
slug: /development
---

## Who we are

We are a [cybersecurity company](https://fluidattacks.com)
whose only purpose is to make the world
a safer place.

## What we do

- We perform comprehensive security testing
    over all of your assets.
- We use cutting-edge technologies
    and heavily trained **human hackers**.
- We report vulnerabilities back to you
    as accurately and quickly as possible.

The source code of the technologies used
is versioned in this repository
and is divided across many products.

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_universe&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fluidattacks_universe)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_universe&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fluidattacks_universe)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_universe&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fluidattacks_universe)
[![Code Grade](https://api.codiga.io/project/34008/score/svg)](https://www.code-inspector.com)

## Installing

1. Make sure that Nix is installed on your system.
   If it is not,
   please follow [this tutorial](https://nixos.org/download.html).
   If everything goes well,
   you should be able to run

    ```bash
    $ nix --version
    ```

    We only support versions of Nix `>= 2.3` and `< 2.4`.

1. Install [Makes](https://github.com/fluidattacks/makes) with

    ```bash
    $ nix-env -if https://github.com/fluidattacks/makes/archive/22.08.tar.gz
    ```

    If everything goes well,
    you should be able to run

    ```bash
    $ m
    ```

1. Use the products of your choice:

    ```bash
    $ m gitlab:fluidattacks/universe@trunk /forces --help
    $ m gitlab:fluidattacks/universe@trunk /melts --help
    $ m gitlab:fluidattacks/universe@trunk /reviews --help
    $ m gitlab:fluidattacks/universe@trunk /skims --help
    $ m gitlab:fluidattacks/universe@trunk /sorts --help
    ```

## Updating

No action is required on your part.
Updates are automatically rolled out to your machine
with a delay of at most one day.
But anyway,
if you want to force an update right away,
just run `$ rm -rf ~/.makes`.

## Troubleshooting

### General considerations

- A stable internet connection is required
- A stable DNS resolver is required.
  Please consider using the following:
    - IPv4: `1.1.1.1`, `8.8.8.8`, `8.8.4.4`
    - IPv6: `2001:4860:4860::8888`, `2001:4860:4860::8844`

### Checklist

1. If the installation failed while installing Nix,

    1. checkout the [Nix manual](https://nixos.org/manual/nix/stable/#chap-installation)
       for more detailed installation instructions, and
    1. if the problem persists,
       please let us know at help@fluidattacks.com.

1. If the installation failed while installing Makes,
   please let us know at help@fluidattacks.com.

1. If the process failed while using `$ m gitlab:xxx /yyy`,

    1. repeat the installation of Makes and try again,

    1. refresh the cache with `$ rm -rf ~/.makes` and try again, and

    1. if the problem persists,
       please let us know at help@fluidattacks.com.
