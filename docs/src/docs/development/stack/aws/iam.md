---
id: iam
title: Identity and Access Management (IAM)
sidebar_label: IAM
slug: /development/stack/aws/iam
---

## Rationale

[AWS IAM][IAM] is the core [AWS][AWS] service
for managing [authentication and authorization](https://securityboulevard.com/2020/06/authentication-vs-authorization-defined-whats-the-difference-infographic/)
within the platform.
It allows us to have [least privilege][LEAST-PRIVILEGE]
compliance regarding
resource access.

The main reasons why we chose it over other alternatives are the following:

- It is a core AWS service,
  which means
  that one must use it
  to be able to access other AWS services.
- It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
  certifications from [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
  and [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
  Many of these certifications are focused on granting
  that the entity follows best practices
  regarding secure [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing)
  environments
  and information security.
- It supports [users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html),
  [groups](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html)
  and [roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html),
  providing full flexibility regarding access management.
- It supports a [wide range](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
  of policies.
  They can be identity-
  or resource-based policies,
  permissions boundaries,
  service control policies,
  access control lists
  and session policies.
- Policies are written using [JSON](https://www.json.org/json-en.html),
  making them very easy to understand.
- Policies are built based on the [specific actions](https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html)
  we want them to allow.
  Each [AWS][AWS] service has its own actions.
- Many [actions](https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html)
  support [condition keys](https://docs.aws.amazon.com/en_cn/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html),
  allowing further customization of authorization.
- It integrates with [Okta][OKTA]
  by using the [SAML](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)
  protocol.
  Roles can be assigned to Okta users and groups,
  giving us full granularity
  and [least privilege][LEAST-PRIVILEGE] compliance
  over the AWS resources.
- It supports [OIDC](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html),
  allowing our [Kubernetes Cluster](/development/stack/kubernetes/)
  to [perform actions](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/autoscaler.tf#L52)
  within AWS,
  like [automatically creating load balancers](https://github.com/kubernetes-sigs/aws-load-balancer-controller)
  when applications are deployed.
- Resources can be [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
  using [Terraform](/development/stack/terraform/).

## Alternatives

> **Note:**
> [GCP IAM](https://cloud.google.com/iam)
> and [Azure RBAC](https://docs.microsoft.com/en-us/azure/role-based-access-control/)
> are alternatives
> that did not exist at the time we migrated to the cloud.
> A review of each of them is pending.

## Usage

We use [AWS IAM][IAM] for managing

- [development and production users](https://gitlab.com/fluidattacks/product/-/tree/9ef43c3585a0871299117178d7fb4dceb129854b/makes/applications/makes/users)
  in all our products
  (every user has their own policies and permissions
  in order to grant [least privilege][LEAST-PRIVILEGE] compliance;
  access keys for users are [rotated on a daily basis](https://gitlab.com/fluidattacks/product/-/blob/017612ea61db1e2be1229a20e97d701be9b3894c/makes/applications/makes/users/integrates/rotate/even/default.nix));
- a [SAML trust relationship](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/makes/applications/makes/okta/src/terraform/aws-saml.tf)
  between IAM and [Okta][OKTA]
  to allow developers and analysts to assume
  [IAM Roles](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/makes/applications/makes/okta/src/terraform/aws-roles.tf)
  by authenticating with their Okta credentials;
- [S3 bucket policies](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/airs/deploy/production/terraform/bucket.tf#L25),
  to allow access through
  [Cloudflare](/development/stack/cloudflare) only;
- [KMS key policies](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/airs/deploy/secret-management/terraform/key-prod.tf#L1),
  to specify what users can use a key
  and what actions each of them can do;
- [service roles](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/makes/applications/makes/compute/src/terraform/aws_batch.tf#L59),
  to allow automated [CI/CD](/development/stack/gitlab-ci) processes
  to assume them,
  and execute specific actions within AWS.

## Guidelines

- You can access the AWS IAM console
  after [authenticating on AWS](/development/stack/aws#guidelines).
- Any changes to IAM infrastructure must be done via [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
- To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform),
  visit the [Terraform Guidelines](/development/stack/terraform#guidelines).

[AWS]: /development/stack/aws/
[IAM]: https://aws.amazon.com/iam/
[LEAST-PRIVILEGE]: /criteria/requirements/186
[OKTA]: /development/stack/okta
