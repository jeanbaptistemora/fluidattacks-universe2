---
id: iam
title: Identity and Access Management (IAM)
sidebar_label: IAM
slug: /development/stack/aws/iam
---

## Rationale

[AWS IAM][IAM] is the core [AWS][AWS] service
for managing
[authentication and authorization](https://securityboulevard.com/2020/06/authentication-vs-authorization-defined-whats-the-difference-infographic/)
within the platform.
It allows us to have
[least privilege][LEAST-PRIVILEGE]
compliance regarding
resource access.

The main reasons why we chose it
over other alternatives are:

1. It is a core [AWS][AWS]
    service,
    which means that in order to be able to
    access other [AWS][AWS] services,
    one must use [IAM][IAM].
1. It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
    certifications from
    [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
    and
    [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
    Many of these certifications
    are focused on granting that the entity
    follows best practices regarding secure
    [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing) environments
    and information security.
1. It supports
    [users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html),
    [groups](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html)
    and
    [roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html),
    providing full flexibility regarding
    access management.
1. It supports a
    [wide range](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
    of policies.
    They can be
    identity-based,
    resource-based,
    permissions boundaries,
    service control policies,
    access control lists
    and session policies.
1. Policies are written using
    [JSON](https://www.json.org/json-en.html),
    making them very easy to understand.
1. Policies are built based on the
    [specific actions](https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html)
    we want them to allow.
    Each [AWS][AWS] service
    has its own actions.
1. Many
    [actions](https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html)
    support
    [condition keys](https://docs.aws.amazon.com/en_cn/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html),
    allowing to further customize
    authorization.
1. It integrates with [Okta][OKTA]
    by using the
    [SAML](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)
    protocol.
    [Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
    can be assigned to
    [Okta][OKTA]
    users and groups,
    giving us full granularity and
    [least privilege][LEAST-PRIVILEGE]
    compliance over
    the AWS resources.
1. It supports [OIDC](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html),
    allowing our [Kubernetes cluster](/development/stack/kubernetes/)
    to [perform actions](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/autoscaler.tf#L52)
    within [AWS][AWS] like
    [automatically creating load balancers](https://github.com/kubernetes-sigs/aws-load-balancer-controller)
    when applications are deployed.
1. Resources can be
    [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
    using
    [Terraform](/development/stack/terraform/).

## Alternatives

1. [GCP IAM](https://cloud.google.com/iam):
    It did not exist at the time we migrated to the cloud.
    Pending to review.
1. [Azure RBAC](https://docs.microsoft.com/en-us/azure/role-based-access-control/):
    It did not exist at the time we migrated to the cloud.
    Pending to review.

## Usage

We use [AWS IAM][IAM] for:

1. Managing
    [development and production users](https://gitlab.com/fluidattacks/product/-/tree/9ef43c3585a0871299117178d7fb4dceb129854b/makes/applications/makes/users)
    for all our products.
    Every user has its own policies and permissions
    in order to grant [least privilege][LEAST-PRIVILEGE] compliance.
    Access keys for such users are
    [rotated on a daily basis](https://gitlab.com/fluidattacks/product/-/blob/017612ea61db1e2be1229a20e97d701be9b3894c/makes/applications/makes/users/integrates/rotate/even/default.nix).
1. Managing a
    [SAML trust relationship](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/makes/applications/makes/okta/src/terraform/aws-saml.tf)
    between [IAM][IAM] and [Okta][OKTA]
    in order to allow developers and analysts to assume
    [IAM Roles](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/makes/applications/makes/okta/src/terraform/aws-roles.tf)
    by authenticating with their [Okta][OKTA]
    credentials.
1. Managing
    [S3 bucket policies](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/airs/deploy/production/terraform/bucket.tf#L25)
    for only allowing access through
    [Cloudflare](/development/stack/cloudflare).
1. Managing
    [KMS key policies](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/airs/deploy/secret-management/terraform/key-prod.tf#L1)
    for specifying what users can use a key
    and what actions each of them can do.
1. Managing
    [service roles](https://gitlab.com/fluidattacks/product/-/blob/9ef43c3585a0871299117178d7fb4dceb129854b/makes/applications/makes/compute/src/terraform/aws_batch.tf#L59)
    for allowing automated
    [CI/CD](/development/stack/gitlab-ci) processes
    to assume them and executing
    specific actions within [AWS][AWS].

## Guidelines

1. You can access the
    [AWS IAM][IAM] console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. Any changes to
    [IAM][IAM]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. To learn how to test and apply infrastructure via
    [Terraform](/development/stack/terraform),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).

[AWS]: /development/stack/aws/
[IAM]: https://aws.amazon.com/iam/
[LEAST-PRIVILEGE]: /criteria/requirements/186
[OKTA]: /development/stack/okta
