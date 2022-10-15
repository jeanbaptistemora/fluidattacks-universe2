---
id: intro
title: Introduction
sidebar_label: Introduction
slug: /development/integrates
---

Integrates is the Product responsible
for the [Attacks Resistance Management platform (ARM)](/machine/web/arm)
and its [API](/machine/api).

## Public Oath

1. The ARM is accessible at
   [app.fluidattacks.com](https://app.fluidattacks.com).
1. Changes to the user interface of the ARM
   that are "significant"
   will be announced
   via the appropriate communication mechanism.
1. The API is accessible at
   [app.fluidattacks.com/api](https://app.fluidattacks.com).
1. The API is backward compatible,
   meaning that no changes made to it by the Developers
   should break the End Users code that depends on it.
1. A six-month notice period will be given
   should backward incompatible changes need to be made in the API,
   for example, but not limited to:
   deprecating attributes and entities,
   making optional arguments mandatory,
   changes in the authentication or authorization system,
   and so on.

## Contributing

Please read the
[contributing](/development/contributing) page first.

### Development Environment

Follow the steps
in the [Development Environment](/development/setup) section
of our documentation.

When prompted for an AWS role, choose `dev`,
and when prompted for a Development Environment, pick `integratesBack`.

### Local Environment

Run each of the following commands in different terminals:

```sh
universe $ m . /integrates/back
universe $ m . /integrates/cache
universe $ m . /integrates/db
universe $ m . /integrates/front
universe $ m . /integrates/storage
```

This will launch a replica of
[app.fluidattacks.com](https://fluidattacks.com)
and [app.fluidattacks.com/api](https://fluidattacks.com/api)
on your [localhost:8001](https://localhost:8001).
