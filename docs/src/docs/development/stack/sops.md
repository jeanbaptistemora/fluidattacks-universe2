---
id: sops
title: Sops
sidebar_label: Sops
slug: /development/stack/sops
---

## Rationale

[Sops][SOPS]
is the tool we use for managing most of our
organizational secrets like passwords,
access keys,
[PII](https://en.wikipedia.org/wiki/Personal_data),
among others.
It allows us to version
encrypted files within our
[Git](https://git-scm.com/) repositories
in a stateless approach.

The main reasons why we chose
it over other alternatives are:

1. It is [Open source](https://opensource.com/resources/what-open-source).
1. it is [Serverless](https://en.wikipedia.org/wiki/Serverless_computing),
    meaning that it does not require maintaining servers, firewalls,
    load balancers, or any other typical infrastructure required for
    common [Secrets Engines][SECRET-ENGINES].
1. It supports [AWS KMS][KMS],
    which allows to encrypt files
    using symmetric
    [AES256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
    keys
    that only exist within the KMS boundaries,
    granting almost-impossible key leakage.
    Access to such keys can be easily managed
    with a user-level granularity
    by using [AWS IAM](/development/stack/aws/iam/).
1. It is free.
    Only costs for decrypting secret files
    using [AWS KMS][KMS] are incurred.
1. As secrets are
    [written as code](https://hackernoon.com/everything-as-code-explained-0ibg32a3),
    it allows
    [software versioning](https://en.wikipedia.org/wiki/Software_versioning),
    as encrypted secret files can be
    [securely pushed to git repositories](https://gitlab.com/fluidattacks/universe/-/blob/f0a6de7eee664aee9794d677083a19f45fff4ffb/makes/applications/makes/okta/src/terraform/data.yaml).
1. It allows reproducibility and auditability
    as secrets are versioned.
1. It is [DevOps](https://aws.amazon.com/devops/what-is-devops/) friendly,
    as secret management is now done through
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/),
    allowing to run
    [CI/CD](https://docs.gitlab.com/ee/ci/introduction/) integrations
    on the secrets.
1. Secret's [KMS][KMS] keys
    are [very easy to rotate](https://github.com/mozilla/sops#key-rotation).
1. It integrates with other services like
    [PGP](https://github.com/mozilla/sops#test-with-the-dev-pgp-key),
    [Age](https://github.com/mozilla/sops#encrypting-using-age),
    [GCP KMS](https://github.com/mozilla/sops#encrypting-using-gcp-kms),
    [Azure Key Vault](https://github.com/mozilla/sops#encrypting-using-azure-key-vault),
    and [Hashicorp Vault](https://github.com/mozilla/sops#encrypting-using-hashicorp-vault).
1. It supports
    [Yaml, Json, Env, Ini and Binary](https://github.com/mozilla/sops/tree/2395f07610e45d507ec0d4b3ad48dbf502ed5bed#sops-secrets-operations)
    formats.

## Alternatives

The following alternatives were considered
but not chosen for the following reasons:

1. [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/):
    They charge on a per-secret basis.
    It is a common
    [Secrets Engine][SECRET-ENGINES],
    meaning that secrets are not stored as code,
    losing versioning, auditability, automation
    and reproducibility capabilities.
1. [HashiCorp Vault](https://www.vaultproject.io/):
    It did not have a
    [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service)
    solution at the time we tried it.
    We had to maintain the entire service on our
    [Kubernetes](https://kubernetes.io/) cluster.
    It is a common
    [Secrets Engine][SECRET-ENGINES],
    meaning that secrets are not stored as code,
    losing versioning, auditability, automation
    and reproducibility capabilities.
1. [Torus](https://www.torus.sh/):
    We used it a few years ago but it got discontinued.
    One year later they relaunched their service.
    It is a common
    [Secrets Engine][SECRET-ENGINES],
    meaning that secrets are not stored as code,
    losing versioning, auditability, automation
    and reproducibility capabilities.

## Usage

Used for managing most of our organizational secrets.
Some examples are:

1. [Airs](https://gitlab.com/fluidattacks/universe/-/blob/f0a6de7eee664aee9794d677083a19f45fff4ffb/airs/deploy/secret-management/production.yaml).
1. [ARM](https://gitlab.com/fluidattacks/universe/-/blob/f0a6de7eee664aee9794d677083a19f45fff4ffb/integrates/secrets-production.yaml).
1. [Docs](https://gitlab.com/fluidattacks/universe/-/blob/f0a6de7eee664aee9794d677083a19f45fff4ffb/docs/secrets/prod.yaml).
1. [Makes](https://gitlab.com/fluidattacks/universe/-/blob/f0a6de7eee664aee9794d677083a19f45fff4ffb/makes/applications/makes/secrets/src/production.yaml).
1. [Okta](https://gitlab.com/fluidattacks/universe/-/blob/f0a6de7eee664aee9794d677083a19f45fff4ffb/makes/applications/makes/okta/src/terraform/data.yaml).

We do not use [Sops][SOPS] for:

1. [Gitlab CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/):
    Although most of the secrets contained here were already migrated,
    there are still some that need review.
1. Automatic secret rotation:
    As [Sops][SOPS] secrets are versioned,
    automatically rotating them would require
    to directly push automated commits to our main branches.
    We have declined to do this until today
    mainly due to consistency and stability concerns.
    Secrets that require automatic rotation
    are kept within our
    [Gitlab CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/).

## Guidelines

1. You can install
    [Sops][SOPS] with `nix-env -i sops`.
1. In order to be able to decrypt a secrets file,
    first you must assume an [IAM](/development/stack/aws/iam/) role
    with access to the [KMS][KMS] key
    that encrypted it.
    You can follow [this guide](/development/stack/aws#get-development-keys)
    to do so.
1. Once authenticated with a role,
    you can decrypt a file with `sops <file>`.
1. You can encrypt a plain file
    with `sops -ei --kms <kms-arn> <file>`.

[SOPS]: https://github.com/mozilla/sops
[SECRET-ENGINES]: https://www.vaultproject.io/docs/secrets
[KMS]: /development/stack/aws/kms
