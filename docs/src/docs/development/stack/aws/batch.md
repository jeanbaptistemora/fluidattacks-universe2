---
id: batch
title: Batch
sidebar_label: Batch
slug: /development/stack/aws/batch
---

## Rationale

We use [Batch][batch]
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
  for the Elastic Compute Cloud ([EC2][ec2]) machines
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
- The jobs are highly [resilient](<https://en.wikipedia.org/wiki/Resilience_(network)>),
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

### GitLab CI

We used [GitLab CI][gitlab-ci] before implementing [Batch][batch].
We migrated
because GitLab CI is not intended to run scheduled jobs
that take many hours,
often resulting in jobs becoming irresponsive
before they could finish,
mainly due to disconnections
between the worker running the job
and the [GitLab CI Bastion](https://docs.gitlab.com/runner/configuration/autoscale.html).
On top of this,
GitLab CI has a limit on the number of schedules per project,
and running thousands of jobs puts a lot of pressure on the GitLab coordinator
and the GitLab CI Bastion.

### Buildkite

> https://buildkite.com

Pros:

- Handles submission of duplicated jobs
- Gives us logging, monitoring, and stability measurements out-of-the-box
- We can separate costs by having different queues (associated to different deployments)
- Notifications out-of-the-box to email and others
- Support pipelines out-of-the-box
- They have an API to query information about past jobs on a pipeline
  and trigger new builds,
  which is much more flexible than Batch's API

Cons:

- Much more expensive.

### Kubernetes Jobs

> https://kubernetes.io/docs/concepts/workloads/controllers/job/

Pros:

- Allows better separation of costs.

Cons:

- It requires manually kick-starting a build,
  because it doesn't listen automatically to the queue like batch does.

## Usage

We use [Batch][batch] for running

- [Production background schedules](https://gitlab.com/fluidattacks/universe/-/blob/e77b8365a6e1d14e5261c62e9c96c34494957392/common/compute/schedule/data.nix)
  for all our products.
- [ARM background tasks](https://gitlab.com/fluidattacks/universe/blob/37b52839d969fe37b4d583756409349f4154ff53/integrates/back/src/batch/enums.py#L21)
  like cloning roots and refreshing targets of evaluation.

## Guidelines

### General

- You can access the [Batch][batch] console
  after [authenticating to AWS](/development/stack/aws#guidelines).
- Any changes to [Batch][batch] infrastructure
  must be done
  via [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
- You can queue new jobs to [Batch][batch]
  using the [compute-on-aws module](https://gitlab.com/fluidattacks/universe/-/tree/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/utils/compute-on-aws).
- If a scheduled job takes longer than six hours,
  it should generally run in [Batch][batch];
  otherwise,
  you can use [GitLab CI][gitlab-ci].
- To learn how to test
  and apply infrastructure
  via [Terraform](/development/stack/terraform/),
  visit the [Terraform Guidelines](/development/stack/terraform#guidelines).
- [Terraform infrastructure](https://gitlab.com/fluidattacks/universe/-/blob/f4def5d3312635b15224d07d840f4aa368b6f93e/common/compute/infra/schedules.tf#L5)
  for such schedule will also be provisioned.

### Schedules

Schedules are a powerful way to run tasks periodically.

You can find all schedules [here](https://gitlab.com/fluidattacks/universe/-/blob/trunk/common/compute/schedule/data.nix).

#### Creating a new schedule

We highly advise you to take a look
at the currently existing schedules
to get an idea of what is required.

Some special considerations are:

1. The `scheduleExpression` option follows
   the [AWS schedule expression syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html).
1. The `meta.lastReview` option has
   a `DD-MM-YYYY` format.

#### Testing the schedules

Schedules are tested by two Makes jobs:

1. `m . /common/compute/schedule/test` Grants that
   - all schedules comply with a given schema;
   - all schedules have at least one active maintainer;
   - every schedule is reviewed by a maintainer on a monthly basis.
1. `m . /deployTerraform/commonCompute`
   Tests infrastructure
   that will be deployed when new
   schedules are created

#### Deploying schedules to production

Once a schedule reaches production,
required infrastructure for running it is created.

Technical details can be found [here](https://gitlab.com/fluidattacks/universe/-/blob/trunk/common/compute/infra/schedules.tf).

#### Local reproducibility in schedules

Once a new schedule is declared,
A Makes job is created
with the format
`computeOnAwsBatch/schedule_<name>`
for local reproducibility.

Generally,
to run any schedule,
all that is necessary
is to export the `UNIVERSE_API_TOKEN` variable.
Bear in mind that `data.nix`
becomes the single source of truth
regarding schedules.
Everything is defined there,
albeit with a few exceptions.

[batch]: https://aws.amazon.com/batch/
[ec2]: /development/stack/aws/ec2/
[gitlab-ci]: /development/stack/gitlab-ci/
