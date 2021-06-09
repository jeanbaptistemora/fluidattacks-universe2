---
id: introduction
title: Commitlint
sidebar_label: Introduction
slug: /development/stack/commitlint
---

## Rationale

[Commitlint](https://github.com/conventional-changelog/commitlint)
is the tool we use for standardizing our
[commit messages](https://git-scm.com/docs/git-commit)
and running
[CI/CD](https://docs.gitlab.com/ee/ci/introduction/)
tests
to force compliance.
It allows us to have
[commit messages](https://git-scm.com/docs/git-commit)
that:

1. Follow a convention.
1. Are readable for humans and machines.

The main reasons why we chose
it over other alternatives are:

1. It allows us to
    have a stadardized
    [commit history](https://gitlab.com/fluidattacks/product/-/commits/master),
    greatly improving documentation
    on what each commit does
    from a high level perspective
    while avoiding ending up
    with a
    [messy commit history](https://chris.beams.io/posts/git-commit/).
1. It supports testing
    commit messages via
    [CLI](https://en.wikipedia.org/wiki/Command-line_interface),
    allowing us to
    automatize it as a
    [CI job](https://gitlab.com/fluidattacks/product/-/blob/f4f630df896ae88f1a88257fcc72e6d8ea9344fc/.gitlab-ci.yml#L100).
1. As commit data is standardized,
    it allows us to run
    [data analytics](https://fluidattacks.com/blog/git-steroids/)
    on our commit history
    and answer questions like
    ***What percentage of the commits
    in the last month were backend features?***,
    ***How many developers worked on
    the front end of our application in the last month?***,
    among many others.
1. It is [Open source](https://opensource.com/resources/what-open-source).
1. It is
    [widely used by the community](https://www.npmjs.com/package/@commitlint/cli).
1. It allows us to
    [declare a syntax](https://commitlint.js.org/#/reference-configuration?id=parser-presets)
    based on
    [our own needs](/development/stack/commitlint/syntax/commit#syntax).
1. It supports many
    [rules](https://commitlint.js.org/#/reference-rules)
    that can be tuned
    based on
    [our own needs](/development/stack/commitlint/syntax/commit#rules).

## Alternatives

1. [git-commit-msg-linter](https://github.com/legend80s/commit-msg-linter#readme):
    It has a
    [much smaller ruleset](https://github.com/legend80s/commit-msg-linter#commitlinterrcjson).
    It is not
    [as widely used by the community](https://www.npmjs.com/package/git-commit-msg-linter).

## Usage

We use [Commitlint](https://github.com/conventional-changelog/commitlint) for:

1. [Linting](https://gitlab.com/fluidattacks/product/-/blob/f9dccced62b019b654c0cc5675392f3ad254baea/makes/applications/makes/lint-commit-msg/entrypoint.sh)
    commit messages in our
    [repository](https://gitlab.com/fluidattacks/product/-/blob/f9dccced62b019b654c0cc5675392f3ad254baea/.commitlintrc.js).

## Guidelines

1. You can run `./m makes.lint-commit-msg`
    for linting your last commit message.
1. You can find commits
    syntax documentation
    [here](/development/stack/commitlint/syntax/commit).
1. You can find
    [merge requests](https://gitlab.com/fluidattacks/product/-/merge_requests)
    syntax documentation
    [here](/development/stack/commitlint/syntax/merge-request).
