---
id: ci
title: CI
sidebar_label: CI
slug: /development/common/ci
---

## Architecture

1. Our CI/CD system is [GitLab CI](/development/stack/gitlab-ci).
1. Most of the infrastructure for this
   is implemented using
   [Niek Palm's terraform-aws-gitlab-runner module](https://github.com/npalm/terraform-aws-gitlab-runner).
1. The machine instances created by the CI have two sizes (small and large),
   and auto-scale on demand throughout the day.
1. The GitLab runner uses the GitLab OpenID provider
   in order to assume an
   [IAM role on Amazon Web Services (AWS)](/development/stack/aws/iam),
   like those provided by the [Users component of Common](/development/common/users).
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
