---
id: nix
title: Nix
sidebar_label: Nix
slug: /development/stack/nix
---

## Rationale

We use the [Nix ecosystem](https://nixos.org/)
for building and deploying all of our [Products](/development/products).

## Alternatives

## Usage

### Installing Nix

Please follow the steps
in the [official Nix Download Page](https://nixos.org/download.html).

If everything goes well,
you should be able to run:

```bash
$ nix --version
```

### Uninstalling Nix

Run the command with root privileges if needed:

```sh
$ rm -fr /nix ~/.nix* ~/.cache/nix ~/.config/nix
```

## Guidelines

Please refer to the official manuals:

- The [Nix Package Manager](https://nixos.org/manual/nix/stable/).
- The [Nix Packages collection](https://nixos.org/manual/nixpkgs/stable/).
- The [NixOS Operative System](https://nixos.org/manual/nixos/stable/).
