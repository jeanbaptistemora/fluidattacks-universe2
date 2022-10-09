---
id: users
title: Users
sidebar_label: Users
slug: /development/common/users
---

## Public Oath

1. There is `dev` role
   and a role with the name of each product
   but prefixed with `prod_`.
   Each role has a KMS key with the same name,
   and can access the keys of other less privileged roles,
   `prod_common` being the super-admin,
   and `dev` the less privileged user)
1. There is a `snowflake-user` user with a corresponding access key
   and the access key value doesn't change.
1. There is an `erika.bayona` user.
1. The ARN of the previous entities
   (IAM roles, IAM users, and KMS keys)
   is constant over time.

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

![Architecture of Common's /users](./users-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.
