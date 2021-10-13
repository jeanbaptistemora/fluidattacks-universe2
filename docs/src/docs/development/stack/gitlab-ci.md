---
id: gitlab-ci
title: Gitlab CI
sidebar_label: Gitlab CI
slug: /development/stack/gitlab-ci
---

## Rationale

[GItlab CI][GITLAB-CI]
is the system that orchestrates all the
[CI/CD](https://docs.gitlab.com/ee/ci/introduction/)
workflows within our company.
Such workflows are the backbone
of our entire
[development cycle][DEV-CYCLE].
By using it, we become capable of:

1. [Running automated processes on every commit](https://docs.gitlab.com/ee/ci/pipelines/).
1. [Automatizing application testing](https://gitlab.com/fluidattacks/product/-/blob/ee58e7a78990ef77ca032e4388d0e0bc49533799/integrates/.gitlab-ci.yml#L368).
1. [Automatizing application deployment](https://gitlab.com/fluidattacks/product/-/blob/ee58e7a78990ef77ca032e4388d0e0bc49533799/integrates/.gitlab-ci.yml#L130).
1. [Automatizing every QA test we can think of](https://gitlab.com/fluidattacks/product/-/blob/47d00a5ace02160becc82de533710f1155080b6d/.gitlab-ci.yml#L141).

By having highly automated workflows,
we become capable of
[deploying applications many times a day](https://gitlab.com/fluidattacks/product/-/commits/master)
without sacrificing quality or security.

The main reasons why we chose
[GItlab CI][GITLAB-CI]
over other alternatives are:

1. It is [Open source](https://opensource.com/resources/what-open-source).
1. [Built-in support for Gitlab][GITLAB]:
    As [Gitlab][GITLAB]
    is the platform we use
    for our [product repository](https://gitlab.com/fluidattacks/product),
    it represents an advantage for us
    to be able to easily integrate
    our [CI][GITLAB-CI] soultion with it.
    All [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface)
    related capabilities like
    [pipelines](https://docs.gitlab.com/ee/ci/pipelines/),
    [jobs][JOBS],
    [CI/CD variables](https://docs.gitlab.com/ee/ci/variables/README.html),
    [environments](https://docs.gitlab.com/ee/ci/environments/),
    [schedules](https://docs.gitlab.com/ee/ci/pipelines/schedules.html),
    and
    [container registries](https://docs.gitlab.com/ee/user/packages/)
    are a consequence of such integration.
1. [It supports pipelines as code](https://about.gitlab.com/topics/ci-cd/pipeline-as-code/):
    It allows us to
    [write all our pipelines as code](https://gitlab.com/fluidattacks/product/-/blob/ee58e7a78990ef77ca032e4388d0e0bc49533799/.gitlab-ci.yml).
1. [It supports horizontal autoscaling][AUTOSCALE]:
    In order to be able to run
    hundreds of [jobs][JOBS]
    for many developers,
    all in real time,
    our system must support
    [horizontal autoscaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/).
1. [It supports directed acyclic graphs (DAG)](https://docs.gitlab.com/ee/ci/directed_acyclic_graph/):
    Such capability allows us to make
    our integrations as fast as possible,
    as [jobs][JOBS]
    exclusively depend on what they really should.
    It is a must when implementing a [monorepo](https://en.wikipedia.org/wiki/Monorepo)
    strategy [like ours](https://gitlab.com/fluidattacks/product).
1. [Highly versatile configurations](https://docs.gitlab.com/ee/ci/yaml/):
    As every piece of software
    usually has its own needs
    when it comes to
    building, testing and deploying,
    [GItlab CI][GITLAB-CI]
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
    The [AWS autoscaler][AUTOSCALE]
    allows configurations for
    [s3 cache](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/#the-runnerscache-section),
    [machine type](https://aws.amazon.com/ec2/instance-types/),
    [max number of machines](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/#the-global-section),
    [spot instances](https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/#cutting-down-costs-with-amazon-ec2-spot-instances),
    [c5d instances ssd disk usage](https://gitlab.com/fluidattacks/product/-/blob/ee58e7a78990ef77ca032e4388d0e0bc49533799/makes/applications/makes/ci/src/config.toml#L56),
    [security groups](https://gitlab.com/fluidattacks/product/-/blob/ee58e7a78990ef77ca032e4388d0e0bc49533799/makes/applications/makes/ci/src/config.toml#L115),
    [ebs disks](https://gitlab.com/fluidattacks/product/-/blob/ee58e7a78990ef77ca032e4388d0e0bc49533799/makes/applications/makes/ci/src/config.toml#L118),
    [off peak periods](https://gitlab.com/fluidattacks/product/-/blob/ee58e7a78990ef77ca032e4388d0e0bc49533799/makes/applications/makes/ci/src/config.toml#L121),
    [tagging](https://gitlab.com/fluidattacks/product/-/blob/ee58e7a78990ef77ca032e4388d0e0bc49533799/makes/applications/makes/ci/src/config.toml#L232),
    [max builds before destruction](https://gitlab.com/fluidattacks/product/-/blob/ee58e7a78990ef77ca032e4388d0e0bc49533799/makes/applications/makes/ci/src/config.toml#L223),
    among many others.
    The importance of having
    a highly versatile [CI][GITLAB-CI]
    comes from the fact
    that our
    [development cycle][DEV-CYCLE]
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
    [Gitlab][GITLAB],
    it was very expensive,
    it was not as parameterizable.
1. [Buildkite](https://buildkite.com/):
    It is still pending for review.

## Usage

We use [GItlab CI][GITLAB-CI] for:

1. Running all our
    [CI/CD](https://docs.gitlab.com/ee/ci/introduction/) jobs.
1. Managing all our
    [CI pipelines as code](https://gitlab.com/fluidattacks/product/-/blob/47d00a5ace02160becc82de533710f1155080b6d/.gitlab-ci.yml).
1. Configuring our
    [AWS autoscaler][AUTOSCALE]
    as
    [code](https://gitlab.com/fluidattacks/product/-/tree/7088bb9d4084d867255edec68614fee6ad7bbca6/makes/foss/modules/makes/ci).
1. Implementing a
    [Continuous Delivery](https://semaphoreci.com/blog/2017/07/27/what-is-the-difference-between-continuous-integration-continuous-deployment-and-continuous-delivery.html)
    approach for our
    [development cycle][DEV-CYCLE].
    This means that although the whole process is automatized,
    including deployments
    for both development and production,
    a manual [merge request approval](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
    from a developer is still required in order to
    be able to deploy changes to production.

We do not use [GItlab CI][GITLAB-CI] for:

1. Highly time-consuming schedules
    that take longer than six hours,
    like
    [Analytics ETL's](https://en.wikipedia.org/wiki/Extract,_transform,_load),
    [Machine learning](https://en.wikipedia.org/wiki/Machine_learning) training,
    among others.
    We use [AWS Batch](/development/stack/aws/batch/) instead.
    The reason for this is that the
    [GItlab CI][GITLAB-CI]
    is not meant to run
    [jobs][JOBS]
    that take that many hours,
    often resulting in
    [jobs][JOBS]
    being terminated
    before they can finish,
    mainly due to disconnections between the
    worker running the job and its
    [Gitlab CI Bastion](https://docs.gitlab.com/runner/configuration/autoscale.html).

## Guidelines

### General

1. Any changes to the
    [CI pipelines](https://gitlab.com/fluidattacks/product/-/blob/47d00a5ace02160becc82de533710f1155080b6d/.gitlab-ci.yml)
    must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. Any changes to the
    [AWS autoscaler][AUTOSCALE]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
    by modifying its
    [Terraform module](https://gitlab.com/fluidattacks/product/-/tree/7088bb9d4084d867255edec68614fee6ad7bbca6/makes/foss/modules/makes/ci).
1. To learn how to test and apply infrastructure
    via [Terraform](/development/stack/terraform),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).
1. If a scheduled job
    takes longer than six hours,
    it generally should run in [Batch](/development/stack/aws/batch/),
    otherwise it can use
    the [Gitlab CI][GITLAB-CI].

### Architecture

We use:

1. [terraform-aws-gitlab-module](https://github.com/npalm/terraform-aws-gitlab-runner)
    for defining our CI as code.
1. [AWS Lambda](/development/stack/aws/lambda/)
    for hourly cleaning orphaned machines.
1. [AWS DynamoDB](/development/stack/aws/dynamodb/)
    for [locking Terraform states](https://www.terraform.io/docs/language/state/locking.html)
    and avoiding race conditions.

### Debugging

As we use a [multi-bastion approach](https://github.com/npalm/terraform-aws-gitlab-runner#gitlab-ci-docker-machine-runner---multiple-runner-agents),
the following tasks can be considered
when debugging the CI:

1. If you're an admin in [Gitlab][GITLAB],
    you can visit the [CI/CD Settings](https://gitlab.com/groups/fluidattacks/-/settings/ci_cd)
    to validate if bastions
    are properly communicating.
1. You can inspect both bastions and workers from the [AWS EC2 console](/development/stack/aws/ec2/).
    Another useful place to look at
    when you're suspecting of [spot availability](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html),
    is the [spot requests view](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-requests.html#using-spot-instances-running).
1. You can connect to a bastion
    using [AWS Session Manager](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/session-manager.html).
    Once inside, you can:
    1. Run `docker-machine` as root.
        This will allow you to inspect and access
        workers with commands like
        `docker-machine ls`,
        `docker-machine inspect <worker>`,
        and `docker-machine ssh <worker>`.
    1. Watch `/var/log/messages` for
        relevant logs from the bastion.
    1. Watch `/etc/gitlab-runner/config.toml`
        for bastion configurations.

### Pending tasks

1. [Workers are left orphaned when a bastion is destroyed](https://github.com/npalm/terraform-aws-gitlab-runner/issues/214),
    impacting reproducibility.
1. [External cache module fails when referenced before creation](https://github.com/npalm/terraform-aws-gitlab-runner/issues/298),
    impacting reproducibility.

[GITLAB]: /development/stack/gitlab
[GITLAB-CI]: https://docs.gitlab.com/ee/ci/
[DEV-CYCLE]: https://about.gitlab.com/stages-devops-lifecycle/
[JOBS]: https://docs.gitlab.com/ee/ci/jobs/
[AUTOSCALE]: https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/
