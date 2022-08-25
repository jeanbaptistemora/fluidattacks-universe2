---
id: batch
title: Batch
sidebar_label: Batch
slug: /development/stack/aws/batch
---

## Rationale

We use [Batch][BATCH]
for running [batch processing](https://en.wikipedia.org/wiki/Batch_processing)
jobs in the [cloud](https://en.wikipedia.org/wiki/Cloud_computing).
The main reasons why we chose it
over other alternatives
are the following:

- It is [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service)
  (software as a service),
  so we do not need to manage any infrastructure directly.
- [It is free](https://aws.amazon.com/batch/pricing/),
  so we only have to pay
  for the Elastic Compute Cloud ([EC2][EC2]) machines
  we use to process workloads.
- It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
  certifications from [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
  and [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
  Many of these certifications are focused
  on granting that the entity follows best practices
  regarding secure [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing)
  environments
  and information security.
- We can [monitor](https://docs.aws.amazon.com/batch/latest/userguide/using_cloudwatch_logs.html)
  job logs
  using [CloudWatch](/development/stack/aws/cloudwatch/).
- The jobs are highly [resilient](https://en.wikipedia.org/wiki/Resilience_(network)),
  which means
  they rarely go irresponsive.
  This feature is very important
  when jobs take several days to finish.
- It supports [EC2 spot instances](https://gitlab.com/fluidattacks/universe/-/blob/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/makes/compute/src/terraform/aws_batch.tf#L138),
  which considerably decreases EC2 costs.
- All its settings can be [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/batch_compute_environment)
  using [Terraform](/development/stack/terraform/).
- We can use [Nix](https://nixos.org/)
  to [queue jobs easily](https://gitlab.com/fluidattacks/universe/-/blob/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/observes/scheduled/on-aws/dif-gitlab-etl/default.nix).
- It supports [priority-based queuing](https://gitlab.com/fluidattacks/universe/-/blob/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/makes/compute/src/terraform/aws_batch.tf#L159),
  which allows us to prioritize jobs
  by assigning them to one queue or another.
- It supports [automatic retries](https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html)
  of jobs.
- It [integrates](https://docs.aws.amazon.com/batch/latest/userguide/batch-supported-iam-actions-resources.html)
  with Identity and Access Management ([IAM](/development/stack/aws/iam/)),
  allowing us to keep
  a [least privilege](/criteria/requirements/186) approach
  regarding [authentication and authorization](https://securityboulevard.com/2020/06/authentication-vs-authorization-defined-whats-the-difference-infographic/).
- EC2 workers running jobs can be monitored using CloudWatch.

## Alternatives

We used [GitLab CI][GITLAB-CI] before implementing [Batch][BATCH].
We migrated
because GitLab CI is not intended to run scheduled jobs
that take many hours,
often resulting in jobs becoming irresponsive
before they could finish,
mainly due to disconnections
between the worker running the job
and the [GitLab CI Bastion](https://docs.gitlab.com/runner/configuration/autoscale.html).

## Usage

We use [Batch][BATCH] for running

- [Production background schedules](https://gitlab.com/fluidattacks/universe/-/blob/f4def5d3312635b15224d07d840f4aa368b6f93e/common/compute/schedule/schedules.nix)
  for all our products.
- [ARM background tasks](https://gitlab.com/fluidattacks/universe/blob/37b52839d969fe37b4d583756409349f4154ff53/integrates/back/src/batch/enums.py#L21)
  like cloning roots and refreshing targets of evaluation.

## Guidelines

- You can access the [Batch][BATCH] console
  after [authenticating to AWS](/development/stack/aws#guidelines).
- Any changes to [Batch][BATCH] infrastructure
  must be done
  via [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
- You can queue new jobs to [Batch][BATCH]
  using the [compute-on-aws module](https://gitlab.com/fluidattacks/universe/-/tree/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/utils/compute-on-aws).
- If a scheduled job takes longer than six hours,
  it should generally run in [Batch][BATCH];
  otherwise,
  you can use [GitLab CI][GITLAB-CI].
- To learn how to test
  and apply infrastructure
  via [Terraform](/development/stack/terraform/),
  visit the [Terraform Guidelines](/development/stack/terraform#guidelines).
- When adding a new
  [schedule](https://gitlab.com/fluidattacks/universe/-/blob/f4def5d3312635b15224d07d840f4aa368b6f93e/common/compute/schedule/schedules.nix),
  a [Makes](https://github.com/fluidattacks/makes) job
  with name `computeOnAwsBatch/schedule_<job-name>` will be created for local reproducibiliy.
- [Terraform infrastructure](https://gitlab.com/fluidattacks/universe/-/blob/f4def5d3312635b15224d07d840f4aa368b6f93e/common/compute/infra/schedules.tf#L5)
  for such schedule will also be provisioned.

[BATCH]: https://aws.amazon.com/batch/
[EC2]: /development/stack/aws/ec2/
[GITLAB-CI]: /development/stack/gitlab-ci/
