---
id: criteria
title: Criteria
sidebar_label: Criteria
slug: /development/common/criteria
---

## Architecture

1. Criteria is managed as-code using YAML documents
   in order to make the information easily accessible
   to automated programs (most programming languages support YAML).
1. The YAML documents
   are validated using [JSON schema](http://json-schema.org/)
   with the [Ajv](https://ajv.js.org/) tool.

   This ensures information contains the required fields,
   and that it adheres to the expected specification.

1. End Users and Developers are expected to use the YAML documents directly.

   Note that for instance,
   Docs consumes this information
   and transforms it into the [online version of Criteria](/criteria).

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /criteria](./criteria-arch.dot.svg)
