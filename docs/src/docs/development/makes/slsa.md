---
id: supply-chain-levels-for-software-artifacts
title: Supply Chain Levels for Software Artifacts
sidebar_label: Supply Chain Levels for Software Artifacts
slug: /development/makes/supply-chain-levels-for-software-artifacts
---

The [SLSA framework](https://slsa.dev/)
helps organizations measure
the level of assurance
that the Software Artifacts they produce
actually contain and use what they intended (integrity),
by ensuring that the whole build and release process,
and all of the involved sources and dependencies
cannot be tampered with.

In this document,
we use the
[version 0.1 of the specification](https://slsa.dev/spec/v0.1/requirements).

Our current SLSA level is 0.
The following is a detail of the levels achieved
on each of the requirements:

| Requirement | Level |
| :---------- | :---: |

For clarity,
this is how SLSA definitions map into our infrastructure:

- **Source**: Git repository at:
  [github.com/fluidattacks/makes][makes].
- **Platform**: [GitHub Actions][github_actions],
  [Makes][makes],
  and the [Nix package manager][nix].
- **Build service**:
  [GitHub Actions][github_actions],
  using GitHub hosted runners.
- **Build**: A Nix derivation.
- **Environment**: A sandbox
  that [Chroot](https://en.wikipedia.org/wiki/Chroot)s
  into an empty temporary directory,
  provides private versions
  of `/proc`, `/dev`, `/dev/shm`, and `/dev/pts`,
  and uses a private PID, mount, network, IPC, and UTS namespace
  to isolate itself from other processes in the system.
- **Steps**: Instructions declared
  in the corresponding Makes configuration files
  written using the Nix programming language
  and shell scripting, versioned as-code in the _source_.

<!-- References -->

[github_actions]: https://docs.github.com/en/actions
[makes]: https://github.com/fluidattacks/makes
[nix]: https://nixos.org/
