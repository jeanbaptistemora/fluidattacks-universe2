---
id: gitlab-ci
title: Gitlab CI
sidebar_label: Gitlab CI
slug: /development/stack/gitlab-ci
---

## Rationale

[GItlab CI][gitlab-ci]
is the system that orchestrates all the
[CI/CD](https://docs.gitlab.com/ee/ci/introduction/)
workflows within our company.
Such workflows are the backbone
of our entire
[development cycle][dev-cycle].
By using it, we become capable of:

1. [Running automated processes on every commit](https://docs.gitlab.com/ee/ci/pipelines/).
1. [Automatizing application testing](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/integrates/pipeline/makes.nix#L182).
1. [Automatizing application deployment](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/integrates/pipeline/makes.nix#L131).
1. [Automatizing every QA test we can think of](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/.gitlab-ci.yml#L126).

By having highly automated workflows,
we become capable of
[deploying applications many times a day](https://gitlab.com/fluidattacks/universe/-/commits/trunk)
without sacrificing quality or security.

The main reasons why we chose
[GItlab CI][gitlab-ci]
over other alternatives are:

1. It is [Open source](https://opensource.com/resources/what-open-source).
1. [Built-in support for Gitlab][gitlab]:
   As [Gitlab][gitlab]
   is the platform we use
   for our [product repository](https://gitlab.com/fluidattacks/universe),
   it represents an advantage for us
   to be able to easily integrate
   our [CI][gitlab-ci] soultion with it.
   All [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface)
   related capabilities like
   [pipelines](https://docs.gitlab.com/ee/ci/pipelines/),
   [jobs][jobs],
   [CI/CD variables](https://docs.gitlab.com/ee/ci/variables/README.html),
   [environments](https://docs.gitlab.com/ee/ci/environments/),
   [schedules](https://docs.gitlab.com/ee/ci/pipelines/schedules.html),
   and
   [container registries](https://docs.gitlab.com/ee/user/packages/)
   are a consequence of such integration.
1. [It supports pipelines as code](https://about.gitlab.com/topics/ci-cd/pipeline-as-code/):
   It allows us to
   [write all our pipelines as code](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/.gitlab-ci.yml).
1. [It supports horizontal autoscaling][autoscale]:
   In order to be able to run
   hundreds of [jobs][jobs]
   for many developers,
   all in real time,
   our system must support
   [horizontal autoscaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/).
1. [It supports directed acyclic graphs (DAG)](https://docs.gitlab.com/ee/ci/directed_acyclic_graph/):
   Such capability allows us to make
   our integrations as fast as possible,
   as [jobs][jobs]
   exclusively depend on what they really should.
   It is a must when implementing a [monorepo](https://en.wikipedia.org/wiki/Monorepo)
   strategy [like ours](https://gitlab.com/fluidattacks/universe).
1. [Highly versatile configurations](https://docs.gitlab.com/ee/ci/yaml/):
   As every piece of software
   usually has its own needs
   when it comes to
   building, testing and deploying,
   [GItlab CI][gitlab-ci]
   offers a vast set of
   [configurations](https://docs.gitlab.com/ee/ci/yaml/)
   that range from
   [parallelism](https://docs.gitlab.com/ee/ci/yaml/#parallel),
   [static pages](https://docs.gitlab.com/ee/ci/yaml/#pages),
   and [services](https://docs.gitlab.com/ee/ci/yaml/#services)
   to
   [includes](https://docs.gitlab.com/ee/ci/yaml/#include),
   [workflows](https://docs.gitlab.com/ee/ci/yaml/#workflow)
   and [artifacts](https://docs.gitlab.com/ee/ci/yaml/#artifacts).
1. [Highly versatile infrastructure](https://docs.gitlab.com/runner/configuration/advanced-configuration.html):
   The [AWS autoscaler][autoscale]
   allows configurations for
   [s3 cache](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/#the-runnerscache-section),
   [machine type](https://aws.amazon.com/ec2/instance-types/),
   [max number of machines](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/#the-global-section),
   [spot instances](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/#cutting-down-costs-with-amazon-ec2-spot-instances),
   [c5d instances ssd disk usage](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/common/ci/infra/runners.tf#L352),
   [ebs disks](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/common/ci/infra/runners.tf#L419),
   [off peak periods](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/common/ci/infra/runners.tf#L462),
   [tagging](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/common/ci/infra/runners.tf#L491),
   [max builds before destruction](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/common/ci/infra/runners.tf#L440),
   among many others.
   The importance of having
   a highly versatile [CI][gitlab-ci]
   comes from the fact
   that our
   [development cycle][dev-cycle]
   completely depends on it,
   making us to expect
   clockwork-like responsiveness
   and as-fast-as-possible
   computing speed.

## Alternatives

The following alternatives were considered
but not chosen for the following reasons:

1. [Jenkins](https://www.jenkins.io/):
   It did not support
   [pipelines as code](https://about.gitlab.com/topics/ci-cd/pipeline-as-code/)
   at the time it was reviewed.
1. [TravisCI](https://travis-ci.com/):
   It required licensing
   for private repositories
   at the time it was reviewed.
1. [CircleCI](https://circleci.com/):
   It did not support
   [Gitlab][gitlab],
   it was very expensive,
   it was not as parameterizable.
1. [Buildkite](https://buildkite.com/):
   It is still pending for review.

## Usage

We use [GItlab CI][gitlab-ci] for:

1. Running all our
   [CI/CD](https://docs.gitlab.com/ee/ci/introduction/) jobs.
1. Managing all our
   [CI pipelines as code](https://gitlab.com/fluidattacks/universe/-/blob/trunk/.gitlab-ci.yml).
1. Configuring our
   [AWS autoscaler][autoscale]
   as
   [code](https://gitlab.com/fluidattacks/universe/-/blob/trunk/common/ci/infra/runners.tf).
1. Implementing a
   [Continuous Delivery](https://semaphoreci.com/blog/2017/07/27/what-is-the-difference-between-continuous-integration-continuous-deployment-and-continuous-delivery.html)
   approach for our
   [development cycle][dev-cycle].
   This means that although the whole process is automatized,
   including deployments
   for both development and production,
   a manual [merge request approval](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
   from a developer is still required in order to
   be able to deploy changes to production.

We do not use [GItlab CI][gitlab-ci] for:

1. Highly time-consuming schedules
   that take longer than six hours,
   like
   [Analytics ETL's](https://en.wikipedia.org/wiki/Extract,_transform,_load),
   [Machine learning](https://en.wikipedia.org/wiki/Machine_learning) training,
   among others.
   We use [AWS Batch](/development/stack/aws/batch/) instead.
   The reason for this is that the
   [GItlab CI][gitlab-ci]
   is not meant to run
   [jobs][jobs]
   that take that many hours,
   often resulting in
   [jobs][jobs]
   being terminated
   before they can finish,
   mainly due to disconnections between the
   worker running the job and its
   [Gitlab CI Bastion](https://docs.gitlab.com/runner/configuration/autoscale.html).

## Guidelines

### General

1. Any changes to the
   [CI pipelines](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/.gitlab-ci.yml)
   must be done via
   [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. Any changes to the
   [AWS autoscaler][autoscale]
   infrastructure must be done via
   [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
   by modifying its
   [Terraform module](https://gitlab.com/fluidattacks/universe/-/tree/b0df4c41021c145d8753ee30dbeeb61c5d1484de/common/ci).
1. To learn how to test and apply infrastructure
   via [Terraform](/development/stack/terraform),
   visit the
   [Terraform Guidelines](/development/stack/terraform#guidelines).
1. If a scheduled job
   takes longer than six hours,
   it generally should run in [Batch](/development/stack/aws/batch/),
   otherwise it can use
   the [Gitlab CI][gitlab-ci].

### Components

We use:

1. [terraform-aws-gitlab-module](https://github.com/npalm/terraform-aws-gitlab-runner)
   for defining our CI as code.
1. [AWS Lambda](/development/stack/aws/lambda/)
   for hourly cleaning orphaned machines.
1. [AWS DynamoDB](/development/stack/aws/dynamodb/introduction/)
   for [locking Terraform states](https://www.terraform.io/docs/language/state/locking.html)
   and avoiding race conditions.

### Tunning the CI

Any team member can tune the CI for a specific product
by modifying the values passed to it
in the [terraform module runners section](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/common/ci/infra/runners.tf#L2).

One of the most important values is the `idle-count`, as it:

1. Specifies how many idle machines
   should be waiting for new jobs.
   the more jobs a product pipeline has,
   the more idle machines it should have.
   you can take the [integrates-small](https://gitlab.com/fluidattacks/universe/-/blob/b0df4c41021c145d8753ee30dbeeb61c5d1484de/common/ci/infra/runners.tf#L93)
   runner as a reference.
1. It also dictates the rate at which the CI turns on new machines,
   that is, if a pipeline with 100 jobs is triggered
   for a CI with `idle-count = 8`,
   it will turn on new machines in batches of `8` until
   it stabilizes.
1. More information about how the autoscaling algorithm works can be found
   [here](https://docs.gitlab.com/runner/configuration/autoscale.html#autoscaling-algorithm-and-parameters).

### Debugging

As we use a [multi-bastion approach](https://github.com/npalm/terraform-aws-gitlab-runner#gitlab-ci-docker-machine-runner---multiple-runner-agents),
the following tasks can be considered
when debugging the CI.

#### Review Gitlab CI/CD Settings

If you're an admin in [Gitlab][gitlab],
you can visit the [CI/CD Settings](https://gitlab.com/groups/fluidattacks/-/settings/ci_cd)
to validate if bastions
are properly communicating.

#### Inspect infrastructure

You can inspect both bastions and workers
from the [AWS EC2 console](/development/stack/aws/ec2/).
Another useful place to look at
when you're suspecting of [spot availability](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html),
is the [spot requests view](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-requests.html#using-spot-instances-running).

#### Connect to bastions or workers

You can connect to any bastion or worker
using [AWS Session Manager](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/session-manager.html).

Just go to the [AWS EC2 console](/development/stack/aws/ec2/),
select the instance you want to connect to,
click on `Connect`,
and start a `Session Manager` session.

#### Debugging the bastion

Typical things you want to look at when debugging a bastion are:

- `docker-machine` commands.
  This will allow you to inspect and access
  workers with commands like
  `docker-machine ls`,
  `docker-machine inspect <worker>`,
  and `docker-machine ssh <worker>`.
- `/var/log/messages` for
  relevant logs from the `gitlab-runner` service.
- `/etc/gitlab-runner/config.toml`
  for bastion configurations.

#### Debugging a specific CI job

You can know which machine ran a job by looking at its logs.

For this [example job](https://gitlab.com/fluidattacks/universe/-/jobs/3843183267#L11),
the line
`Running on runner-cabqrx3c-project-20741933-concurrent-0 via runner-cabqrx3c-ci-worker-skims-small-0-1677537770-87c5ed70...`,
tells us that the worker with name
`runner-cabqrx3c-ci-worker-skims-small-0-1677537770-87c5ed70`
was the one that ran it.

From there you can access the bastion and run memory or disk debugging.

[gitlab]: /development/stack/gitlab
[gitlab-ci]: https://docs.gitlab.com/ee/ci/
[dev-cycle]: https://about.gitlab.com/stages-devops-lifecycle/
[jobs]: https://docs.gitlab.com/ee/ci/jobs/
[autoscale]: https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/
