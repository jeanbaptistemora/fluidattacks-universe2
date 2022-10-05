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
1. Criteria is managed as-code using YAML documents
   whose schema is validated with [JSON schema](http://json-schema.org/)
   using [Ajv](https://ajv.js.org/),
   plus some metadata in its front-matter.

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common](./common-arch.dot.svg)
