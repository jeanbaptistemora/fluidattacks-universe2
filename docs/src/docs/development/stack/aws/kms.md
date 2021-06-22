---
id: kms
title: Key Management Service (KMS)
sidebar_label: KMS
slug: /development/stack/aws/kms
---

## Rationale

[AWS KMS][KMS]
is the service we use
for storing and using
cryptographic keys.
It allows us to have
non-readable
symmetric and asymmetric
private keys
hosted in the
[cloud](https://en.wikipedia.org/wiki/Cloud_computing).

The main reasons why we chose it
over other alternatives are:

1. It
    [integrates](https://aws.amazon.com/kms/features/#AWS_Service_Integration)
    with other [AWS][AWS]
    services like
    [DynamoDB](https://aws.amazon.com/dynamodb/),
    [EKS](/development/stack/aws/eks/),
    [S3](/development/stack/aws/s3/),
    [EBS][EBS],
    among others.
1. It uses a state-of-the-art approach
    for both encryption and decryption
    in which keys are never exposed.
    It accomplishes this
    by making users send the data
    they want to encrypt/decrypt
    and then returning it
    encrypted/decrypted.
    By doing so,
    it grants that keys never
    leave [KMS][KMS].
    This approach greatly reduces
    the chances of key leakage,
    as plaintext keys can only be
    obtained via
    [brute-force attacks](https://en.wikipedia.org/wiki/Brute-force_attack).
1. It uses
    [hardware security modules](https://aws.amazon.com/kms/features/#Secure)
    validated under [FIPS 140-2](https://en.wikipedia.org/wiki/FIPS_140-2)
    so that no one can retireve the existant keys.
    Such keys are never written to disk and
    only exist within volatile memory for the time
    needed to process requests.
1. It provides a centralized key vault with complete
    [API support](https://docs.aws.amazon.com/kms/latest/APIReference/API_Operations.html)
    where you can store both
    [AWS and customer managed keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html),
    [rotate them](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html),
    [log and monitor them](https://docs.aws.amazon.com/kms/latest/developerguide/security-logging-monitoring.html),
    [set deleting waiting periods](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html#deleting-keys-how-it-works),
    etc.
1. It supports a
    [fully granular](https://docs.aws.amazon.com/kms/latest/developerguide/control-access-overview.html)
    authentication and access control model,
    where each key has a policy that specifies
    what actions users can
    execute.
    Aditionally, when combined with
    [AWS IAM](https://aws.amazon.com/iam/),
    it allows us to specify permissions
    over general actions like
    creating keys.
1. Keys and permissions can be
    [written as code](https://gitlab.com/fluidattacks/product/-/blob/6416b9035e089b575336c3ba074ff5fd39575306/makes/applications/makes/secrets/src/terraform/key-production.tf)
    using
    [Terraform](/development/stack/terraform/).
1. It integrates with [Sops](/development/stack/sops/),
    allowing us to use its keys for encrypting
    our versioned secrets.

## Alternatives

1. [Google Cloud Key Management](https://cloud.google.com/security-key-management):
    It did not exist at the time we migrated to the cloud.
    It does not integrate
    with other [AWS][AWS] services,
    meaning that an entire platform migration would be required.
1. [Azure Key Vault](https://azure.microsoft.com/en-us/services/key-vault/):
    It did not exist at the time we migrated to the cloud.
    It does not integrate
    with other [AWS][AWS] services,
    meaning that an entire platform migration would be required.

## Usage

We use [AWS KMS][KMS] for:

1. [DynamoDB Encryption at rest](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table#server_side_encryption).
1. [S3 Server side encryption](https://gitlab.com/fluidattacks/product/-/blob/a089fc93ce78b5a073a9ef35c46ec59f7d622e2c/airs/deploy/production/terraform/bucket.tf#L5).
1. [Encrypting and decrypting](https://gitlab.com/fluidattacks/product/-/blob/a089fc93ce78b5a073a9ef35c46ec59f7d622e2c/makes/applications/makes/secrets/src/production.yaml#L14)
    our
    [Sops](/development/stack/sops/) secrets.
1. [Encrypting and decrypting](https://gitlab.com/fluidattacks/product/-/blob/a089fc93ce78b5a073a9ef35c46ec59f7d622e2c/integrates/deploy/secret-management/terraform/forces-secrets.tf#L4)
    our [Secrets Manager](https://aws.amazon.com/secrets-manager/) secrets.
1. [Encrypting and decrypting](https://gitlab.com/fluidattacks/product/-/blob/a089fc93ce78b5a073a9ef35c46ec59f7d622e2c/makes/applications/makes/k8s/src/terraform/cluster.tf#L42)
    our [Kubernetes](/development/stack/kubernetes) workers
    [EBS][EBS] disks.
1. Encrypting and decrypting our
    [ERP](https://en.wikipedia.org/wiki/Enterprise_resource_planning)
    data [EBS][EBS] disk.
1. Encrypting and decrypting our
    [Okta RADIUS](/development/stack/okta#usage)
    Agent [EBS][EBS] disk.

We do not use [AWS KMS][KMS] for:

1. [Redshift](https://aws.amazon.com/redshift/):
    The database is not encrypted at rest. Pending to implement.
1. [CI Bastion](/development/stack/gitlab-ci/):
    It does not use [EBS][EBS]
    encrypted disks as only the base
    [Operating system][OS]
    and other minor dependencies
    are stored there, as described
    [here][EBS-USAGE].
1. [CI Workers](/development/stack/gitlab-ci/):
    They do not use [EBS][EBS]
    encrypted disks as only the base
    [Operating system][OS]
    is stored there, as described
    [here][EBS-USAGE].
1. [Batch workers](https://aws.amazon.com/batch/):
    They do not use [EBS][EBS]
    encrypted disks as only the base
    [Operating system][OS]
    is stored there, as described
    [here][EBS-USAGE].

## Guidelines

1. You can access the
    [AWS KMS][KMS] console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. Any changes to
    [KMS's][KMS]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).

[AWS]: /development/stack/aws/
[KMS]: https://aws.amazon.com/kms/
[EBS]: /development/stack/aws/ebs/
[OS]: https://en.wikipedia.org/wiki/Operating_system
[EBS-USAGE]: /development/stack/gitlab-ci
