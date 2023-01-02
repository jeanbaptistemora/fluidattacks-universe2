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
data can be consumed for creating dashboards
and info-graphics that End Users consume.

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

1. The Data Warehouse is a
   [Redshift cluster on Amazon Web Services](/development/stack/aws/redshift)
   deployed on many subnets provided
   by the [VPC component of Common](/development/common/vpc)
   for High Availability.

1. [Grow](https://www.grow.com/)
   is the solution we use for Business Intelligence (BI).

1. ETL tasks are scheduled
   using the [Compute component of Common](/development/common/compute).

   For legacy reasons,
   a custom scheduler exists called `/observes/job/scheduler`,
   whose task is to submit jobs
   to a Job Queue on the [Compute component of Common](/development/common/compute).
   See [Issue #7903](https://gitlab.com/fluidattacks/universe/-/issues/7903).

1. Most of the ETL fetch data from their corresponding service,
   transform it,
   and upload the results to the Warehouse.

   A few exceptions exist though:

   - `/observes/etl/code/compute-bills`:
     Whose task is to produce billing information
     for [Integrates](/development/products/integrates),
     and therefore puts the data into a bucket owned by Integrates.

   - `/observes/etl/code/mirror/all-on-aws`:
     Whose task is to clone the source code repositories of Fluid Attacks customers,
     and publish it in a location more accessible to Fluid Attacks Hackers.

   - `/observes/etl/timedoctor/backup`:
     Whose task is to collect data from the TimeDoctor API periodically
     to speed up the `/observes/etl/timedoctor` ETL,
     but most importantly,
     to overcome a limitation in the TimeDoctor API
     that only allows us to fetch data starting from a few months back in time.

     We collect this data and save it
     so that when it becomes old and unavailable in the API,
     we can take it from the backup,
     and therefore have a complete view of it
     throughout the entire history.

   - `/observes/etl/zoho-crm/fluid/prepare`:
     Whose task is to prepare the data to download on Zoho,
     such that `/observes/etl/zoho-crm/fluid` is able to fetch it.

   - `/observes/job/batch-stability`:
     Whose task is to monitor the
     [Compute component of Common](/development/common/compute).

   - `/observes/job/cancel-ci-jobs`:
     Whose task is to cancel old CI jobs on [GitLab](/development/stack/gitlab)
     that got stuck.

1. Some ETL are differential,
   and they store the current state in the `observes.state` in a
   [S3 bucket](/development/stack/aws/s3).

:::note
For simplicity, the origin service from which each ETL fetch data
is not shown in the diagram,
but it can be inferred from the ETL name,
for instance,
`/observes/etl/checkly` fetches data from
[Checkly](https://www.checklyhq.com/).
:::

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Observes](./arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.
