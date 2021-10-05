# Table of contents

- [Architecture](#architecture)
- [Contributing](#contributing)
  * [Requirements](#requirements)
  * [Installing Nix](#installing-nix)
  * [Git repository](#git-repository)
  * [Git configuration](#git-configuration)
  * [Build system](#build-system)
  * [Credentials / Authentication](#credentials---authentication)
  * [Local back-end server](#local-back-end-server)
  * [Local web application](#local-web-application)

<!-- http://ecotrust-canada.github.io/markdown-toc -->

# Architecture

Checkout the [ADR](./arch/README.md)

# Contributing

## Requirements

The instructions presented below will work correctly in any
debian/alpine based x86_64-linux operating system with fabric configurations
in user-space and DNS set to 1.1.1.1, 8.8.8.8, and 8.8.4.4.

Additionally you'll require sudo access to root.

## Installing Nix

```bash
curl -sL https://nixos.org/nix/install | sh
```

## Git repository

1. Follow [these](https://gitlab.com/help/ssh/README#generating-a-new-ssh-key-pair)
   instructions to generate your SSH key pair
1. Follow [these](https://docs.gitlab.com/ee/user/project/repository/gpg_signed_commits/)
   instructions to generate a GPG key pair
1. Clone the repository into any folder

    ```bash
    $ git clone git@gitlab.com:fluidattacks/product.git
    Cloning into 'product'...
    # ...
    ```

## Git configuration

1. Tell Git who you are:

    ```bash
    $ git config --global user.name "Benito Martinez"
    $ git config --global user.email bmartinez@fluidattacks.com

    # These settings are useful, too
    $ git config --global commit.gpgsign true
    ```
2. Check if the changes were successfully registered with:

    ```bash
    $ git config --list
    commit.gpgsign=true
    user.email=bmartinez@fluidattacks.com
    user.name=Benito Martinez
    ```

## Build system

In general, everything can be achieved by running `./build.sh` and `./m`
inside the repository.
If no instruction is provided, the list of
available commands is displayed.

## Credentials / Authentication

Some commands can be run without authentication while others require you to login.
Please check out the [Get development keys](https://gitlab.com/fluidattacks/product/-/wikis/%5BIntegrates%5D-Get-development-keys) wiki for instructions.

## Local back-end server

Run each command in a different terminal:

```bash
m . /integrates/back
m . /integrates/cache
m . /integrates/db
./m integrates.storage
```

## Local web application

Run each command in a different terminal:

```bash
m . /integrates/front
```

## Local mobile application

Run each command in a different terminal:

```bash
m . /integrates/mobile
```
