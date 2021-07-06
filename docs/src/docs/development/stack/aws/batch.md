---
id: batch
title: Batch
sidebar_label: Batch
slug: /development/stack/aws/batch
---

## Rationale

We use [Batch][BATCH] for
running [batch processing](https://en.wikipedia.org/wiki/Batch_processing)
jobs in the [cloud](https://en.wikipedia.org/wiki/Cloud_computing).

The main reasons why we chose it
over other alternatives are:

1. It is
    [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service),
    as no infrastructure needs to be directly managed.
1. [It is free](https://aws.amazon.com/batch/pricing/),
    as we only need to pay
    for the [EC2][EC2] machines
    used to process workloads.
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
1. Job logs can be [monitored](https://docs.aws.amazon.com/batch/latest/userguide/using_cloudwatch_logs.html)
    using [CloudWatch](/development/stack/aws/cloudwatch/).
1. Jobs are highly
    [resilent](https://en.wikipedia.org/wiki/Resilience_(network)),
    meaning that they rarely
    go irresponsive.
    This feature is very important
    when jobs take several days to finish.
1. It supports
    [EC2 spot instances](https://gitlab.com/fluidattacks/product/-/blob/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/makes/compute/src/terraform/aws_batch.tf#L138),
    which considerably decreases [EC2][EC2]
    costs.
1. All its settings can be
    [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/batch_compute_environment)
    using
    [Terraform](/development/stack/terraform/).
1. We can use [Nix](https://nixos.org/)
    for [easily queueing jobs](https://gitlab.com/fluidattacks/product/-/blob/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/observes/scheduled/on-aws/dif-gitlab-etl/default.nix).
1. It supports
    [priority-based queues](https://gitlab.com/fluidattacks/product/-/blob/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/makes/compute/src/terraform/aws_batch.tf#L159),
    allowing to prioritize jobs
    by assigning them
    to one queue or another.
1. It supports job
    [automatic retries](https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html).
1. It
    [integrates](https://docs.aws.amazon.com/batch/latest/userguide/batch-supported-iam-actions-resources.html)
    with
    [IAM](/development/stack/aws/iam/),
    allowing to keep a
    [least privilege](/criteria/requirements/186)
    approach
    regarding
    [authentication and authorization](https://securityboulevard.com/2020/06/authentication-vs-authorization-defined-whats-the-difference-infographic/).
1. [EC2][EC2] workers
    running jobs can be monitored
    using [CloudWatch](/development/stack/aws/cloudwatch/).

## Alternatives

[Gitlab CI][GITLAB-CI]:
We used it before implementing [Batch][BATCH].
We migrated because [Gitlab CI][GITLAB-CI]
is not meant to run
scheduled jobs
that take many hours,
often resulting in jobs
becoming irresponsive
before they could finish,
mainly due to disconnections between the
worker running the job and the
[Gitlab CI Bastion](https://docs.gitlab.com/runner/configuration/autoscale.html).

## Usage

We use [Batch][BATCH] for:

1. Running [Observes ETLs](https://gitlab.com/fluidattacks/product/-/tree/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/observes/scheduled/on-aws).
1. Running [Skims scans](https://gitlab.com/fluidattacks/product/-/tree/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/skims/process-groups-on-aws).
1. Running [Skims OWASP Benchmark](https://gitlab.com/fluidattacks/product/-/tree/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/skims/owasp-benchmark-on-aws).
1. Running [ASM Users to Entity reports](https://gitlab.com/fluidattacks/product/-/blob/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/applications/integrates/subscriptions/user-to-entity-on-aws/default.nix).

## Guidelines

1. You can access the
    [Batch][BATCH] console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. Any changes to
    [Batch][BATCH]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. You can queue new jobs to [Batch][BATCH]
    by using the
    [compute-on-aws module](https://gitlab.com/fluidattacks/product/-/tree/89f27281c773baa55b70b8fd37cff8b802edf2e7/makes/utils/compute-on-aws).
1. If a scheduled job
    takes longer than six hours,
    it generally should run in [Batch][BATCH],
    otherwise it can use
    the [Gitlab CI][GITLAB-CI].
1. To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform/),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).

[BATCH]: https://aws.amazon.com/batch/
[EC2]: /development/stack/aws/ec2/
[GITLAB-CI]: /development/stack/gitlab-ci/
