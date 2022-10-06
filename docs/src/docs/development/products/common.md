---
id: common
title: Common
sidebar_label: Common
slug: /development/common
---

Common is a meta-product
that serves as a common place for resources and utilities
that can be used by two or more products.
Most of its code is infrastructure,
but it also contains some documentation
and build system libraries.

## Public Interface

End Users normally interact with Common through:

- The status page: [status.fluidattacks.com](https://status.fluidattacks.com/).
- [Criteria](/criteria).
- [The Virtual Private Network (VPN)](/development/stack/aws/vpn).

Developers usually interact with Common through (or to change something in):

- [Okta](/development/stack/okta).
- Users: [IAM on Amazon Web Services (AWS)](/development/stack/aws/iam).
- Compute: [Batch on Amazon Web Services (AWS)](/development/stack/aws/batch).
- [GitLab CI/CD](/development/stack/gitlab-ci).
- [Kubernetes Cluster](/development/stack/kubernetes).
- Domain Name System: [DNS on Cloudflare](/development/stack/cloudflare).

## Architecture

1. All of the infrastructure
   is managed as-code
   with [Terraform](/development/stack/terraform).

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

### Cluster

![Architecture of Common/Cluster](./common-cluster-arch.dot.svg)

### Criteria

1. Criteria is managed as-code using YAML documents
   whose schema is validated with [JSON schema](http://json-schema.org/)
   using [Ajv](https://ajv.js.org/),
   plus some metadata in its front-matter.

### Users

1. The "users" component of "Common"
   owns the authentication and authorization within
   [Amazon Web Services (AWS)](/development/stack/aws).
1. We divide our AWS account
   into production and development.

   For development,
   we have an [IAM](/development/stack/aws/iam) role
   called `dev`.

   For production,
   we have an [IAM](/development/stack/aws/iam) role
   named as the product, prefixed with `prod_`, for example: `prod_integrates`.
   The IAM role called `prod_common`
   is the super-admin role,
   and it's more privileged than any other role.

   We have one external user
   as part of our subscription with [Clouxter](https://clouxter.com/)
   called `erika.bayona`,
   and a user for accessing Snowflake on Amazon Web Services (AWS).

1. Secrets are encrypted
   and managed with [Mozilla's Secrets OPerationS (SOPS)](/development/stack/sops).

   Each product has a [KMS key](/development/stack/aws/kms)
   on [Amazon Web Services (AWS)](/development/stack/aws)
   that is used to encrypt and decrypt the SOPS file,

   - The `prod_common` role can access any product KMS key.
   - All `prod_*` roles can access the `dev` KMS key,
     and the KMS key of their respective product.
   - The `dev` role can access the `dev` KMS key only.

![Architecture of Common/Users](./common-users-arch.dot.svg)
