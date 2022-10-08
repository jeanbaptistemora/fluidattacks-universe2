---
id: intro
title: Common
sidebar_label: Introduction
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

- [Criteria](/development/common/criteria): Live at [Criteria](/criteria).
- Status: Live at [status.fluidattacks.com](https://status.fluidattacks.com/).
- VPN (Virtual Private Network):
  [VPN by Amazon Web Services](/development/stack/aws/vpn)
  and [Ubiquiti](/development/stack/ubiquiti).

Developers usually interact with Common through (or to change something in):

- [CI](/development/common/ci) (Continuous Integration):
  [GitLab CI/CD](/development/stack/gitlab-ci).
- [Cluster](/development/common/cluster):
  [Kubernetes](/development/stack/kubernetes)
  and [EKS by Amazon Web Services (AWS)](/development/stack/aws/eks).
- [Compute](/development/common/compute):
  [Batch by Amazon Web Services (AWS)](/development/stack/aws/batch).
- DNS (Domain Name System): [Cloudflare](/development/stack/cloudflare).
- [Okta](/development/stack/okta).
- [Users](/development/common/users):
  [IAM by Amazon Web Services (AWS)](/development/stack/aws/iam).
- VPC (Virtual Private Cloud):
  [VPC by Amazon Web Services (AWS)](/development/stack/aws/vpc).
