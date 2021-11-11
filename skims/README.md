# Contributing

As a cybersecurity product we want to make the world a safer place

We do this by:
- Finding all vulnerabilities possible
- Using different attack vectors and cutting edge technologies
- Reporting only true positives

You can help us achieve these goals by the following means:
- Telling your friends
- Using the product
- Creating [issues](https://gitlab.com/fluidattacks/product/-/issues) with ideas, feature requests,
  problems, use cases, or feedback
- Helping us solve those issues

Code contributions or direct bug fixes can be submitted as a patch to
development@fluidattacks.com
or directly as a PR request to this repository.

Should you have any questions we'll be happy to help you: help@fluidattacks.com

## From zero to running a development version of skims

- Install Nix as explained in the [tutorial](https://nixos.org/download.html)
- Clone this repository
- Run: `./m skims --help`

Changes made to the source code are reflected on each invocation

## Executing quality checks locally (lint, benchmark, test, security, structure, docs, etc)

- Run: `./m`, a list of available commands will be displayed.
  Relevant commands begin with `skims` prefix

- Some tests require a local instance of integrates, to deploy a local instance of integrates,
  run each command in a different terminal.

  ```bash
  m . /integrates/back
  m . /integrates/cache
  m . /dynamoDb/skims
  m . /integrates/storage
  ```
