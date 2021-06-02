---
id: gitlab
title: Gitlab
sidebar_label: Gitlab
slug: /development/stack/gitlab
---

## Rationale

[Gitlab](https://about.gitlab.com/)
is the platform we use for
[developing our software](https://gitlab.com/fluidattacks/product).
It provides essential services like
[Git repositories](https://blog.axosoft.com/learning-git-repository/),
[Merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/index.html),
[Development planning](https://docs.gitlab.com/ee/topics/plan_and_track.html),
[CI/CD](gitlab-ci),
among many others.

The main reasons why we chose
[Gitlab](https://about.gitlab.com/)
over other alternatives are:

1. It is [Open Source](https://opensource.com/resources/what-open-source).
1. It is [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service).
1. It is a [DevOps Suite](https://about.gitlab.com/blog/2017/10/04/devops-strategy/),
meaning that all their technical efforts are focused on creating
a workflow that facilitates getting high quality
code to production as secure and fast as possible.
Such vision is in harmony with our philosophical
vision of
[software development](https://en.wikipedia.org/wiki/Software_development)
and current
[development cycle](https://about.gitlab.com/stages-devops-lifecycle/).
1. It has its own [Continuous Integrator](gitlab-ci)
with built-in support,
which is essetial to our
[development cycle](https://about.gitlab.com/stages-devops-lifecycle/).
1. It has the
[Gitlab for Open Source](https://about.gitlab.com/solutions/open-source/)
program,
which gives unlimited
[ultimate](https://about.gitlab.com/pricing/) free seats to
[Open Source](https://opensource.com/resources/what-open-source)
projects like [ours](https://gitlab.com/fluidattacks/product).
1. It provides
[Development Planning](https://docs.gitlab.com/ee/topics/plan_and_track.html)
with
[issues](https://gitlab.com/fluidattacks/product/-/issues),
[milestones](https://gitlab.com/fluidattacks/product/-/milestones),
[roadmaps](https://docs.gitlab.com/ee/user/group/roadmap/index.html),
among others.
Such features are essential for
task prioritization and resource assignment.
1. It has highly customizable
[permissions settings](https://docs.gitlab.com/ee/user/permissions.html),
allowing to give permissions using a
[user-based granular](https://docs.gitlab.com/ee/user/permissions.html#project-members-permissions)
approach.
Publishing specific sections
of a project using a
[section-based granular](https://docs.gitlab.com/ee/user/permissions.html#project-features-permissions)
approach
is also possible.
1. It supports
[Two-factor Authentication](https://docs.gitlab.com/ee/user/profile/account/two_factor_authentication.html).
1. It supports
[Merge Requests](https://gitlab.com/fluidattacks/product/-/merge_requests),
allowing developers to open requests
to get their changes to production.
1. It supports
[Merge Request Approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/),
allowing to specify a group
of developers for reviewing and approving
[merge requests](https://gitlab.com/fluidattacks/product/-/merge_requests).
In order to be able to reach production,
developers need at least one approval
from a user belonging to the approvers group.
An approver cannot approve her own
[merge requests](https://gitlab.com/fluidattacks/product/-/merge_requests),
everyone needs their work to be reviewed by someone else.
1. It has a very complete
[REST API](https://docs.gitlab.com/ee/api/)
that allows us to automatize
processes like
[reviewing merge requests](https://gitlab.com/fluidattacks/product/-/tree/f153761ee61aad37b00212e134eb8ac689e1952e/reviews),
[rotating AWS secrets](https://gitlab.com/fluidattacks/product/-/tree/f153761ee61aad37b00212e134eb8ac689e1952e/makes/utils/user-rotate-keys)
and
[programatically cloning repositories](https://gitlab.com/fluidattacks/product/-/blob/f153761ee61aad37b00212e134eb8ac689e1952e/makes/utils/git/template.sh#L35).
2. It has its own
[Container registry](https://gitlab.com/fluidattacks/product/container_registry),
allowing us to seamlessly store all our containers in the same place.
1. It supports
[CI/CD schedules](https://gitlab.com/fluidattacks/product/-/pipeline_schedules),
which allows us to easily run scheduled
[jobs](https://docs.gitlab.com/ee/ci/jobs/).
1. It supports
[Environments](https://gitlab.com/fluidattacks/product/-/environments)
for seamlessly accessing both development and production environments.
1. It supports built-in
[Analytics](https://gitlab.com/fluidattacks/product/-/value_stream_analytics)
that provide
[issue insights](https://gitlab.com/fluidattacks/product/insights/#/issues),
[CI/CD analytics](https://docs.gitlab.com/ee/user/analytics/ci_cd_analytics.html),
[merge request analytics](https://docs.gitlab.com/ee/user/analytics/merge_request_analytics.html),
[issue analytics](https://gitlab.com/fluidattacks/product/-/analytics/issues_analytics),
[repository analytics](https://gitlab.com/fluidattacks/product/-/graphs/master/charts),
among others.
1. It supports many
[ChatOps integrations](https://docs.gitlab.com/ee/user/project/integrations/overview.html).
Allowing us to have an open,
dedicated telemetry channel
on our internal chat platform
that recieves all types of relevant information
from
[Gitlab](https://about.gitlab.com/).
Developers just need to keep an eye on it
in order to know what's happening with
[merge requests](https://gitlab.com/fluidattacks/product/-/merge_requests),
[issues](https://gitlab.com/fluidattacks/product/-/issues),
[failed jobs](https://docs.gitlab.com/ee/ci/jobs/),
etc.
1. It supports
[Repository Mirroring](https://docs.gitlab.com/ee/user/project/repository/repository_mirroring.html),
allowing us to have a mirror
of [our repository](https://gitlab.com/fluidattacks/product)
on [GitHub](https://github.com/fluidattacks/product).
1. It supports
[Project Access Tokens](https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html),
which greatly increase security and reliability on our integrations,
as we use project-bounded instead of user-bounded tokens.
1. It supports
[GPG Signed Commits](https://docs.gitlab.com/ee/user/project/repository/gpg_signed_commits/),
allowing us to add an extra layer of security by ensuring that
when someone pushes a new commit,
that person is indeed who she claims she is.
1. It supports
[Gitlab Pages](https://docs.gitlab.com/ee/user/project/pages/),
a very easy way of publishing
[static web pages](https://en.wikipedia.org/wiki/Static_web_page).
1. It supports
[Protected Branches](https://docs.gitlab.com/ee/user/project/protected_branches.html),
an essential feature that assures
that no one can push
to the main production branch,
thus forcing developers
to reach production via
[merge requests](https://gitlab.com/fluidattacks/product/-/merge_requests).
1. It supports infrastructure integrations for
[Error Tracking](https://docs.gitlab.com/ee/operations/error_tracking.html),
[Tracing](https://docs.gitlab.com/ee/operations/tracing.html),
[Metrics](https://docs.gitlab.com/ee/user/project/integrations/prometheus_library/kubernetes.html),
among others.
2. It supports
[Push Rules](https://docs.gitlab.com/ee/push_rules/push_rules.html)
that allow to further customize what can and cannot be pushed to the repository.
Some examples are
[branch naming](https://docs.gitlab.com/ee/push_rules/push_rules.html),
[signed commits](https://docs.gitlab.com/ee/push_rules/push_rules.html),
[secret pushing prevention](https://docs.gitlab.com/ee/push_rules/push_rules.html#prevent-pushing-secrets-to-the-repository),
among others.

## Alternatives

1. [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/):
It did not exist at the time.
It is not [Open Source](https://opensource.com/resources/what-open-source).
2. [BitBucket](https://bitbucket.org/product/):
It is not a [DevOps](https://aws.amazon.com/devops/what-is-devops/)
solution but a source code respository.
It did not integrate with a [CI/CD](gitlab-ci) solution.
1. [GitHub](https://github.com/about):
It is not a [DevOps](https://aws.amazon.com/devops/what-is-devops/)
solution but a source code respository.
It did not integrate with a [CI/CD](gitlab-ci) solution.

## Usage

We use [Gitlab](https://about.gitlab.com/) for:

1. Hosting our
[product repository](https://gitlab.com/fluidattacks/product).
1. Hosting our
[issues](https://gitlab.com/fluidattacks/product/-/issues).
1. Hosting our
[milestones](https://gitlab.com/fluidattacks/product/-/milestones).
1. Opening our
[merge requests](https://gitlab.com/fluidattacks/product/-/merge_requests).
1. Hosting our
[containers](https://gitlab.com/fluidattacks/product/container_registry).
1. Visualizing
[jobs](https://docs.gitlab.com/ee/ci/jobs/)
and
[pipelines](https://docs.gitlab.com/ee/ci/pipelines/).


We do not use [Gitlab](https://about.gitlab.com/) for:

1. [Security scans](https://docs.gitlab.com/ee/user/application_security/):
We tried to implement this in the past
but were not able due to
low parametrization capabilities on the scans.
1. [Operations](https://docs.gitlab.com/ee/operations/):
We currently do not use a stack that
integrates with [Gitlab](https://about.gitlab.com/).
Issues have been opened for this:
[Review Sentry](https://gitlab.com/fluidattacks/product/-/issues/4729),
[Review Jaeger](https://gitlab.com/fluidattacks/product/-/issues/4728),
[Review Elastic Stack](https://gitlab.com/fluidattacks/product/-/issues/4727).

## Guidelines

1. [Start using Git on the command line](https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html#start-using-git-on-the-command-line).
1. [Signing commits with GPG](https://docs.gitlab.com/ee/user/project/repository/gpg_signed_commits/).
1. [Generate SSH keys](https://docs.gitlab.com/ee/ssh/#generate-an-ssh-key-pair).
1. [Create a personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#create-a-personal-access-token).
1. [Create a merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html).
1. [Create an issue](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#create-a-new-issue).
