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

<!--
### Two person reviewed - L4

This is required for L4, but not for L3

We need to change our policy for this if we want to be L4
-->
