---
id: supply-chain-levels-for-software-artifacts
title: Supply chain Levels for Software Artifacts
sidebar_label: Supply chain Levels for Software Artifacts
slug: /about/security/integrity/supply-chain-levels-for-software-artifacts
---

The SLSA framework
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

These are the levels achieved by Fluid Attacks:

| Requirement                    | Level |
| :----------------------------- | :---: |
| Source - Version Controlled    |   4   |
| Source - Verified History      |   4   |
| Source - Retained Indefinitely |   4   |
| Source - Two Person Reviewed   |   3   |
| Build - Scripted Build         |   4   |
| Build - Build Service          |   4   |
| Build - Build As Code          |   4   |
| Build - Ephemeral Environment  |   4   |
| Build - Isolated               |   2   |
| Build - Parameter-less         |   4   |
| Build - Hermetic               |   4   |

For clarity,
this is how SLSA definitions map into our infrastructure:

- **Platform**: [GitLab CI/CD][gitlab_ci_cd],
  [Makes][makes],
  and the [Nix package manager][nix].
- **Build**: A Nix derivation.
- **Environment**: [Control Group](https://en.wikipedia.org/wiki/Cgroups)
  created by Nix
  that [Chroot](https://en.wikipedia.org/wiki/Chroot)s
  into an empty temporary directory,
  and provides no network
  or file system access
  outside of it.
- **Steps**: Instructions declared
  in the corresponding Makes configuration files
  written using the Nix programming language
  and shell scripting.

## Source Requirements

### Version Controlled

Every change to the source
is tracked in a version control system
that meets the following requirements:

- **Change history**: There exists a record
  of the history of changes
  that went into the revision.
  Each change contains:
  the identities of the uploader and reviewers (if any),
  timestamps of the reviews (if any) and submission,
  the change description/justification,
  the content of the change,
  and the parent revisions.

  For example: [MR 28742](https://gitlab.com/fluidattacks/universe/-/merge_requests/28742).

- **Immutable reference**:
  There exists a way to indefinitely reference a particular,
  immutable revision.
  For example:
  [1e1cb90fe224fb033b582829aad903cfef4ae9b9](https://gitlab.com/fluidattacks/universe/-/commit/1e1cb90fe224fb033b582829aad903cfef4ae9b9).

### Verified History

Every change in the revision’s history
need to pass through a Merge Request.

In order to create or approve a Merge Request
both the author and the reviewer
need to be strongly authenticated into GitLab.
The authentication process requires 2FA,
and the dates of the change
are recorded in the Merge Request.

Only users who were previously granted access
by a platform Admin can create or review Merge Requests.

For example:
[MR 28742](https://gitlab.com/fluidattacks/universe/-/merge_requests/28742).

### Retained Indefinitely

The revision and its change history
are preserved indefinitely
and cannot be deleted
or modified (not even with multi-party approval).

At the moment,
no legal requirement
impedes us to preserve indefinitely our change history,
and no obliteration policy is in effect.
In fact, our source code is Free and Open Source Software:
[Change History](https://gitlab.com/fluidattacks/universe/-/commits).

### Two person reviewed

<!-- TODO: We need two trusted persons for L4 -->

Every change in the revision’s history
is agreed to by at least one trusted person
prior to submission
and each of these trusted persons
are authenticated into the platform (using 2FA) first.

## Build Requirements

### Scripted Build

All build steps were fully defined
using GitLab CI/CD, Makes and Nix.

Manual commands are not necessary to invoke the build script.
A new build is triggered automatically
each time new changes are pushed to the repository.

For example:
[1](https://gitlab.com/fluidattacks/universe/-/blob/a567ebed88d68a1c18c3889b3a273ba1e9fa37a1/skims/gitlab-ci.yaml),
[2](https://gitlab.com/fluidattacks/universe/-/blob/a567ebed88d68a1c18c3889b3a273ba1e9fa37a1/skims/env/development/main.nix),
[3](https://gitlab.com/fluidattacks/universe/-/blob/a567ebed88d68a1c18c3889b3a273ba1e9fa37a1/skims/config/runtime/template.sh).

### Build Service

All build steps run on GitLab CI/CD.

### Build As Code

All build steps have been defined as-code using the
[GitLab CI/CD configuration file](https://gitlab.com/fluidattacks/universe/-/blob/trunk/.gitlab-ci.yml).

### Ephemeral Environment

<!-- Machines are reused, but this is OK. -->

Our build service
runs each build step
inside a container
that is provisioned solely for each build
and not reused from a prior build.
For example: [Container Image](https://gitlab.com/fluidattacks/universe/-/blob/aa44f91956d7aef7847a12cd971c14de9d0c8058/.gitlab-ci.yml#L39).

### Isolated

<!-- TODO: Caches if used need to be content-addressed to be L3 or L4 -->

Our build service
ensures that the build steps
run in an isolated environment
free of influence from other build instances,
whether prior or concurrent,
by using containerization technologies.

Builds are executed using the [Nix package manager][nix],
which prevents builds
from accessing any external environment variables,
network resources, sockets,
or paths in the file system.

Each build is created as a different OS process
inside a [Control Group](https://en.wikipedia.org/wiki/Cgroups)
making them isolated from each other.

Input-addressed build caches are used to speed-up the pipeline.

### Parameter-less

The build output cannot be affected by user parameters
other than the build entry point
and the top-level source location.

In order to modify the build output,
a change to the source code must happen first.

<!-- References -->

[gitlab_ci_cd]: https://docs.gitlab.com/ee/ci/
[makes]: https://github.com/fluidattacks/makes
[nix]: https://nixos.org/
