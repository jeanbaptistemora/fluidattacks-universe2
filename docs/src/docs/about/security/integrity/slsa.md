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

## Source Requirements

### Version controlled

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
