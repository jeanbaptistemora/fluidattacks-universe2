---
id: lambda
title: Lambda
sidebar_label: Lambda
slug: /development/stack/aws/lambda
---

## Rationale

[Lambda][LAMBDA] is the service we use for running
[serverless](https://en.wikipedia.org/wiki/Serverless_computing)
functions.

The main reasons why we chose it over other alternatives are the following:

- It allows us to execute tasks
  without having to design any infrastructure.
- It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
  certifications from [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
  and [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
  Many of these certifications are focused on granting
  that the entity follows best practices regarding secure
  [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing) environments
  and information security.
- It supports [many different runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html),
  allowing to run code for programming languages
  like [Python](https://www.python.org/),
  [Ruby](https://www.ruby-lang.org/en/),
  [Go](https://golang.org/),
  among others.
- It supports [lambda scheduling](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html),
  allowing to run lambdas
  on a scheduled basis.
  This is especially useful for tasks
  like [CI workers cleaning](https://gitlab.com/fluidattacks/product/-/blob/1f35599056b3bd800fcf4c109b471ec3597b2f8a/makes/applications/makes/ci/src/terraform/clean-lambda-schedule.tf).
- It [integrates](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html)
  with other [AWS][AWS] services,
  allowing us to easily manage
  [EC2](/development/stack/aws/ec2/) instances
  or sending emails via [SQS](https://aws.amazon.com/sqs/).
- Resources can be [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_alias)
  using [Terraform](/development/stack/terraform/).
- Lambda logs and performance can be monitored
  using [CloudWatch](/development/stack/aws/cloudwatch/).

## Alternatives

- **[Cloudflare Workers](https://workers.cloudflare.com/):**
  We use it to set up [security headers](https://gitlab.com/fluidattacks/product/-/blob/1f35599056b3bd800fcf4c109b471ec3597b2f8a/airs/deploy/production/terraform/js/headers.js)
  with [Cloudflare](/development/stack/cloudflare/).
  It does not easily connect with other [AWS][AWS] services.
- **[Google Functions](https://cloud.google.com/functions):**
  It does not easily connect with other [AWS][AWS] services.
- **[Azure Functions](https://azure.microsoft.com/en-us/services/functions/):**
  It does not easily connect with other [AWS][AWS] services.

## Usage

We use [Lambda][LAMBDA] for

- cleaning [GitLab CI](/development/stack/gitlab-ci)
  stale machines
  by using [scheduled lambdas](https://gitlab.com/fluidattacks/product/-/blob/1f35599056b3bd800fcf4c109b471ec3597b2f8a/makes/applications/makes/ci/src/terraform/clean-lambda.tf),
  and
- [sending emails](https://gitlab.com/fluidattacks/product/-/blob/1f35599056b3bd800fcf4c109b471ec3597b2f8a/integrates/deploy/terraform-resources/lambda/send_mail_notification.tf)
  on our [ASM](https://fluidattacks.com/categories/asm/).

## Guidelines

- You can access the AWS Lambda console
  after [authenticating on AWS](/development/stack/aws#guidelines).
- Any changes to Lambda's infrastructure must be done via [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
- To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform/),
  visit the [Terraform Guidelines](/development/stack/terraform#guidelines).

[AWS]: /development/stack/aws/
[LAMBDA]: https://aws.amazon.com/lambda/
