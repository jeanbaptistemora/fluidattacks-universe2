---
id: intro
title: Observes
sidebar_label: Introduction
slug: /development/observes
---

Observes is the product responsible
for company-wide data analytics.

Observes follows the
[Data Warehouse](https://en.wikipedia.org/wiki/Data_warehouse)
architecture,
which means that most of what it does
is _Extract_ data
from different sources,
_Transform_ that into a relational model,
and _Upload_ the results to a Data Warehouse.
This process is usually known as an ETL.
Once the data is in the Warehouse,
Observes creates dashboards and info-graphics
that End Users consume.

Observes also provides a few services
outside of the Data Warehouse architecture,
for example:
Generating billing information,
mirroring customer source code repositories for easy access by Fluid Attacks Hackers,
and stopping stuck [GitLab](/development/stack/gitlab) jobs.

## Public Oath

1. Data in the Warehouse is consistent, correct, and reasonably up-to-date.

1. When deciding between correctness and speed,
   correctness will be given priority.

## Architecture

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Observes](./arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.
