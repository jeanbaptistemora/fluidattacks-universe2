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
1. Common has many sub-products,
   which are documented below.

### /ci

1. Our CI/CD system is [GitLab CI](/development/stack/gitlab-ci).
1. Most of the infrastructure for this
   is implemented using
   [Niek Palm's terraform-aws-gitlab-runner module](https://github.com/npalm/terraform-aws-gitlab-runner).
1. The machine instances created by the CI have two sizes (small and large),
   and auto-scale on demand throughout the day.
1. The GitLab runner uses the GitLab OpenID provider
   in order to assume an
   [IAM role on Amazon Web Services (AWS)](/development/stack/aws/iam),
   like those provided by the [/users component of Common](#users).
1. A DynamoDB table is provided
   in order to allow other Developers
   to lock the terraform state,
   such that it's only modified by one actor (Developer, CI job, etc)
   at the same time,
   helping prevent state corruption.

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /ci](./common-ci-arch.dot.svg)

### /compute

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /compute](./common-compute-arch.dot.svg)

### /cluster

1. We have one [Kubernetes cluster](/development/stack/kubernetes)
   that is shared by all the products.
1. The cluster is hosted by
   [EKS on Amazon Web Services (AWS)](/development/stack/aws/eks).
1. The cluster is divided into namespaces,
   which keep resources in isolation from other namespaces.
   - The `default` namespace is unused,
     we try to put things into a namespace appropriate to the product.
   - The `dev` namespace
     currently holds the ephemeral environments of Integrates.
   - The `prod-integrates` namespace holds the production deployment
     of Integrates,
     and a Celery jobs server.
   - The `kube-system` namespace holds cluster-wide deployments
     for New Relic, DNS, the load balancer, and the auto-scaler,
   - Other `kube-*` namespaces exist,
     but they are not used for anything at the moment.
1. Every namespace runs in a specific worker group
   whose physical machine instances run
   on [EC2 on Amazon Web Services (AWS)](/development/stack/aws/ec2).
1. The cluster spawns machine instances
   on many subnets (prefixed with `k8s_`)
   in different availability zones.

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /cluster](./common-cluster-arch.dot.svg)

### /criteria

1. Criteria is managed as-code using YAML documents
   in order to make the information easily accessible
   to automated programs (most programming languages support YAML).
1. The YAML documents
   are validated using [JSON schema](http://json-schema.org/)
   with the [Ajv](https://ajv.js.org/) tool.

   This ensures information contains the required fields,
   and that it adheres to the expected specification.

1. End Users and Developers are expected to use the YAML documents directly.

   Note that for instance,
   Docs consumes this information
   and transforms it into the [online version of Criteria](/criteria).

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /criteria](./common-criteria-arch.dot.svg)

### /users

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

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /users](./common-users-arch.dot.svg)
