---
id: criteria
title: Criteria
sidebar_label: Criteria
slug: /development/common/criteria
---

Criteria is the component of Common
that maps different security standards
to each Fluid Attacks internal requirement,
and enumerates the possible types of security findings
that Fluid Attacks can find and report in a client.

Here we store Criteria as raw data
in a format intended to be consumed by automated processes.
[Docs](/development/docs) also holds a [human-readable version of Criteria](/criteria),
but both are different things and have different guarantees.

## Public Oath

1. The data complies the schema.
1. The identifiers and titles of `requirements` and `vulnerabilities`
   do not change.

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
