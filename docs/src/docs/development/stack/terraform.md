---
id: terraform
title: Terraform
sidebar_label: Terraform
slug: /development/stack/terraform
---

## Rationale

[Terraform](https://www.terraform.io/)
is used for writing our entire
[infrastructure stack as code](https://en.wikipedia.org/wiki/Infrastructure_as_code).

## Alternatives

- [AWS Cloudformation](https://aws.amazon.com/cloudformation/):
Not chosen as it is platform-bounded.

## Usage

Used for every infrastructure piece. Some examples are:

- [Continuous Integrator](https://gitlab.com/fluidattacks/product/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/makes/applications/makes/ci/src/terraform)
- [DNS](https://gitlab.com/fluidattacks/product/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/makes/applications/makes/dns/src/terraform)
- [Kubernetes](https://gitlab.com/fluidattacks/product/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/makes/applications/makes/k8s/src/terraform)
- [Okta](https://gitlab.com/fluidattacks/product/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/makes/applications/makes/okta/src/terraform)
- [Website](https://gitlab.com/fluidattacks/product/-/tree/2a1e5fc66bcf675fd4249cdf3faf31d3a414a85d/airs/deploy/production/terraform)

## Guidelines

- Test an infrastructure module with `./m <product>.<module>.test`
- Deploy an infrastructure module with `./m <product>.<module>.apply`
