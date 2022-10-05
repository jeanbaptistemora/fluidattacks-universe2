---
id: intro
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
is versioned in the [Universe repository][universe]
and is divided across many products.
We also have a [GitHub account][github_fluidattacks]
where we publish projects
that are more oriented towards the community
and less coupled to our model of business.

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_universe&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fluidattacks_universe)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_universe&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fluidattacks_universe)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_universe&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fluidattacks_universe)
[![Code Grade](https://api.codiga.io/project/34008/score/svg)](https://www.code-inspector.com)
[![Security Scorecard](https://img.shields.io/badge/Security%20Scorecard-A-green)](https://securityscorecard.com/security-rating/fluidattacks.com?utm_medium=badge&utm_source=fluidattacks.com&utm_campaign=seal-of-trust)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/6313/badge)](https://bestpractices.coreinfrastructure.org/projects/6313)

## Our products

- **Airs**: Home page,
  live at [fluidattacks.com](https://fluidattacks.com/).
- **Docs**: Reference documentation,
  live at [docs.fluidattacks.com](https://docs.fluidattacks.com/).

- **Common**: Owner of critical,
  or company wide infrastructure and resources,
  and owner of the admin account.

- **Integrates**: The Attack Resistance Management platform:

  - Web interface: [app.fluidattacks.com](https://app.fluidattacks.com/).
  - API: [app.fluidattacks.com/api](https://app.fluidattacks.com/api).

- **Skims**: Security Vulnerability Scanner.
- **Forces**: The DevSecOps agent.
- **Sorts**: Machine Learning assisted tool,
  that sorts the list of files in a git repository
  by probability of it having vulnerabilities.

- **Melts**: CLI tool that allow Fluid Attack's security analysts
  to clone customer git repositories

- **Observes**: Company wide data analytics.

- **Reviews**: Small tool we use
  to enforce internal policies at Merge Request time.

## Our users

We have different kind of users,
we divide them by use case:

- **End Users**:
  They don't contribute code,
  but instead just interact with our products
  by installing them on their hosts and using the product's CLI,
  or through interacting with the product's public interface
  (an API, web interface, container image, etc).

  They are usually:

  - **Security Analysts of Fluid Attacks**:
    They usually use Sorts, Melts, and the ARM (Integrates), among others.
  - **Customers of Fluid Attacks**:
    They usually use the ARM (Integrates),
    the DevSecOps container image (Forces),
    read our blog (Airs),
    and sometimes our documentation (Docs).
  - **Community users**:
    They usually use tools like Skims in its Free and Open Source plan.

- **Developers**:
  The people who contribute code at [Universe][universe]
  and are usually hired by Fluid Attacks.
  They also contribute sometimes to our [projects on GitHub][github_fluidattacks].

## Installing

1. Make sure that Nix is installed on your system.
   If it is not,
   please follow [this tutorial](https://nixos.org/download.html).
   If everything goes well,
   you should be able to run

   ```bash
   $ nix --version
   ```

   We support versions of Nix `>= 2.6` but we recommend the latest version.

1. Install [Makes](https://github.com/fluidattacks/makes) with

   ```bash
   $ nix-env -if https://github.com/fluidattacks/makes/archive/22.09.tar.gz
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

<!--  -->

[universe]: https://gitlab.com/fluidattacks/universe
[github_fluidattacks]: https://github.com/fluidattacks
