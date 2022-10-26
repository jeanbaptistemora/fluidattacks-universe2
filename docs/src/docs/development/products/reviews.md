---
id: reviews
title: Reviews
sidebar_label: Reviews
slug: /development/reviews
---

Reviews is the product responsible
for ensuring that Merge Requests on GitLab
comply with the defined development policies,
for instance:

- It checks that the Merge Request
  has the [required syntax](/development/stack/commitlint)
- It checks that the pipeline has succeeded.

Among others.

End Users are given the option to configure what checks run.

## Architecture

1. Reviews is a CLI written in Python.
   It communicates with the [GitLab GraphQL API](/development/integrates)
   to get information about a Merge Request
   and the associated Pipelines and Git Commits to it,
   and then performs checks over the information.
1. Reviews is distributed to the End Users
   using [Makes](/development/stack/makes).

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Reviews](./reviews-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.

### Development Environment

Follow the steps
in the [Development Environment](/development/setup/environment) section of our documentation.

When prompted for an AWS role, choose `dev`,
and when prompted for a Development Environment, pick `reviews`.

### Local Environment

Just run:

```sh
universe $ m . /reviews
```

This will build and run the Reviews CLI application,
including the changes you've made to the source code.
