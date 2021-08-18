# Fluid Attacks Continuous Integrator

## Module

We use [terraform-aws-gitlab-module](https://github.com/npalm/terraform-aws-gitlab-runner)
for defining our CI as code.

## Cleaning Lambda

We use AWS Lambda
for hourly cleaning orphaned machines.
Please refer to `infra/clean.tf`
for more information.

## DynamoDB Terraform Lock

We use AWS DynamoDB
for locking Terraform states
and avoiding race conditions.
Please refer to `infra/lock.tf`
for more information.

## Pending tasks

1. [Workers are left orphaned when a runner is destroyed](https://github.com/npalm/terraform-aws-gitlab-runner/issues/214),
    impacting reproducibility.
1. [External cache module fails when referenced before creation](https://github.com/npalm/terraform-aws-gitlab-runner/issues/298),
    impacting reproducibility.
