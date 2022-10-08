---
id: users
title: Users
sidebar_label: Users
slug: /development/common/users
---

## Architecture

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
   and a user for accessing Snowflake by Amazon Web Services (AWS).

1. Secrets are encrypted
   and managed with [Mozilla's Secrets OPerationS (SOPS)](/development/stack/sops).

   Each product has a [KMS key](/development/stack/aws/kms)
   on [Amazon Web Services (AWS)](/development/stack/aws)
   that is used to encrypt and decrypt the SOPS file,

   - The `prod_common` role can access any product KMS key.
   - All `prod_*` roles can access the `dev` KMS key,
     and the KMS key of their respective product.
   - The `dev` role can access the `dev` KMS key only.

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /users](./common-users-arch.dot.svg)
