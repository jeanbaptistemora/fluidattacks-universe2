---
id: supply-chain-levels-for-software-artifacts
title: Supply Chain Levels for Software Artifacts
sidebar_label: Supply Chain Levels for Software Artifacts
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

Our current SLSA level is 2.
The following is a detail of the levels achieved
on each of the requirements:

| Requirement                        | Level |
| :--------------------------------- | :---: |
| Source - Version Controlled        |   4   |
| Source - Verified History          |   4   |
| Source - Retained Indefinitely     |   4   |
| Source - Two Person Reviewed       |   3   |
| Build - Scripted Build             |   4   |
| Build - Build Service              |   4   |
| Build - Build As Code              |   4   |
| Build - Ephemeral Environment      |   4   |
| Build - Isolated                   |   2   |
| Build - Parameter-less             |   4   |
| Build - Hermetic                   |   4   |
| Build - Reproducible               |   3   |
| Provenance - Available             |   4   |
| Provenance - Authenticated         |   4   |
| Provenance - Service Generated     |   4   |
| Provenance - Non-Falsifiable       |   4   |
| Provenance - Dependencies Complete |   4   |
| Common - Security                  |   4   |
| Common - Access                    |   3   |
| Common - Superusers                |   3   |

For clarity,
this is how SLSA definitions map into our infrastructure:

- **Source**: Git repository at:
  [fluidattacks/universe](https://gitlab.com/fluidattacks/universe).
- **Platform**: [GitLab CI/CD][gitlab_ci_cd],
  [Makes][makes],
  and the [Nix package manager][nix].
- **Build service**:
  [GitLab CI/CD][gitlab_ci_cd]
  and related infrastructure.
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

### Two Person Reviewed

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

All build steps have been stored and versioned
in the Git Repository: [.gitlab-ci.yml](https://gitlab.com/fluidattacks/universe/-/blob/trunk/.gitlab-ci.yml).

### Ephemeral Environment

<!-- Machines are reused, but this is OK. -->

Our build service
runs each build step
inside a container
that is provisioned solely for each build
and not reused from a prior build.
For example: [Container Image](https://gitlab.com/fluidattacks/universe/-/blob/aa44f91956d7aef7847a12cd971c14de9d0c8058/.gitlab-ci.yml#L39).

Additionally,
the [Nix package manager][nix]
provides an ephemeral environment to each of the derivations.

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
and provides private versions
of `/proc`, `/dev`, `/dev/shm`, and `/dev/pts`,
and uses a private PID, mount, network, IPC, and UTS namespace
to isolate the build from other builds
happening concurrently in the system.

Input-addressed build caches are used to speed-up the pipeline.

### Parameter-less

The build output cannot be affected by user parameters
other than the build entry point
and the top-level source location.

In order to modify the build output,
a change to the source code must happen first.

### Hermetic

Builds are executed using the [Nix package manager][nix],
which prevents builds
from accessing any external environment variables,
network resources, sockets,
or paths in the file system.

All transitive build steps, sources, and dependencies
are fully declared up front with immutable references.
For example:
[makes.nix](https://gitlab.com/fluidattacks/universe/-/blob/cf4c6e37b76978f6ca9036f79602bca32383d61a/makes.nix#L93).

The [Nix package manager][nix]:

- Fetches all of the declared artifacts
  into a trusted control plane (the /nix/store).
- Mounts into the build sandbox
  the specific /nix/store paths required by it.
- Allows a build to fetch artifacts over the network
  if and only if the expected artifact integrity is specified.
- Validates the integrity of each artifact
  before allowing a build to use it,
  and fails the build if the verification fails.
- Denies network connectivity if no expected hash is specified.

### Reproducible

All of our build scripts are intended to be reproducible.

The reproducibility guarantees of our build scripts
are that of the [Nix package manager][nix].

If a build fails to be reproducible,
we do not explicitly define why.

## Provenance Requirements

In SLSA,
"Provenance" is a piece of verifiable information
about software artifacts
describing where,
when and how
they were produced.

The purpose of this requirement
is to protect consumers
from using a compromised package:

![Supply Chain Threat Model](https://res.cloudinary.com/fluid-attacks/image/upload/v1662151018/docs/about/security/integrity/slsa-supply-chain-threats.svg)

At Fluid Attacks consumers and builders are the same entity.
We don't use artifacts or packages as a mean of distribution.

Instead,
consumers use [Makes][makes],
a source identifier,
and the target artifact identifier,
and then all sources,
dependencies and intermediate artifacts
are built locally in the consumer machine
using the [Nix package manager][nix]
by following the steps and environment
defined as-code in the source.

### Available

Provenance is produced by Makes,
and exposed by the build service
as a JSON document
together with the artifacts produced by the build.

Only builds that produce artifacts generate provenance,
because if a build does not produce artifacts,
then there wouldn't be something to verify the provenance of.

### Authenticated

The authenticity of the provenance
comes from the fact
that it can be downloaded
from the build service itself,
and therefore the authenticity claim
is as strong as the _Build and Source Requirements_ are secure.

The integrity of the provenance
is displayed in the logs
and generated by Makes.

### Service Generated

The data in the provenance
is exposed by the build service,
and is generated by Makes.

Regular users of the service
are not able to inject
or alter the contents
because a build is fully determined
and automated by its configuration,
and the configuration comes directly from the source.

### Non-Falsifiable

The provenance
cannot be falsified by the build service's users:

- There is no secret material
  to demonstrate the non-falsifiable nature of the provenance
  (see _Provenance - Authenticated_).
- Even if such secret material existed,
  builds are run in an hermetic environment,
  and therefore they wouldn't be available to the build steps
  (see _Build - Hermetic_).
- Every field in the provenance is generated
  by the build service in a trusted control plane,
  which is fully defined by the build configuration,
  which comes directly from the Source,
  and therefore is as secure as the Source is
  (see _Source - Verified History_).

### Dependencies Complete

The provenance contains all of dependencies
that were available while running the build steps.

This is guaranteed by the fact
that builds are hermetic
(see _Build - Hermetic_).
So for a build to succeed,
all of its dependencies must be declared,
and therefore the build tool (Makes and Nix)
who fetched them at build time,
have strong knowledge of their existence.

## Common Requirements

### Security

For more information see:
[Fluid Attacks's security page](/about/security).

### Access

Our build service is SaaS,
which means physical access is not possible.
Administrators can access the build machines
through remote protocols
without multi-party approval.

### Superusers

Only a small number of platform admins may override the guarantees provided by SLSA.
Doing so does not currently require approval
of a second platform admin.

<!-- References -->

[gitlab_ci_cd]: https://docs.gitlab.com/ee/ci/
[makes]: https://github.com/fluidattacks/makes
[nix]: https://nixos.org/
