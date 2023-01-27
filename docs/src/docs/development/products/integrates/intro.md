---
id: intro
title: Integrates
sidebar_label: Introduction
slug: /development/products/integrates
---

Integrates is the Product responsible
for the [Attack Resistance Management platform (ARM)](/machine/web/arm)
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

## Architecture

1. Integrates is a standard client-server application
   divided into a front-end, a back-end,
   and out-of-band computing tasks.

1. Integrates has three environments:

   - The productive environment (`prod_integrates`)
     is used by the End Users
     and is deployed by the [CI](/development/stack/gitlab-ci)
     from the `trunk` branch on [GitLab](/development/stack/gitlab).

   - The development environment (`dev`)
     is used by developers
     and is deployed
     by the [CI](/development/stack/gitlab-ci)
     from each developer's branch on [GitLab](/development/stack/gitlab)
     with a name equal to the branch it was deployed from.

   - The local environment
     is deployed by each developer on their personal computers.
     However, this environment is not represented
     or further explained in this architecture,
     but instructions can be found [below](#local-environment).

1. The front-end is deployed into [AWS S3](/development/stack/aws/s3) buckets,
   using the corresponding bucket for the environment
   (`development`, or `production`).

1. Static [DNS](/development/stack/cloudflare) entries
   point to the corresponding
   [S3 buckets on Amazon Web Services (AWS)](/development/stack/aws/s3),
   allowing [Cloudflare](/development/stack/cloudflare)
   to cache their content for a while.

1. The back-end is deployed
   into the [Kubernetes](/development/stack/kubernetes) cluster
   provided by the [Cluster component of Common](/development/common/cluster),
   into the corresponding namespace for the environment
   (`dev` or `prod_integrates`).

1. Dynamic [DNS](/development/stack/cloudflare) entries
   are generated automatically for each back-end deployment
   using the [Kubernetes](/development/stack/kubernetes)
   ingress controller for AWS,
   which essentially binds the corresponding domain
   to an AWS Elastic Load Balancer (ELB)
   that routes traffic from the internet
   into the corresponding cluster nodes,
   allowing [Cloudflare](/development/stack/cloudflare)
   to act as a firewall between the internet
   and the web application,
   and providing rate-limiting.

1. The backend uses:

   - [DynamoDB by Amazon Web Services (AWS)](/development/stack/aws/dynamodb/introduction)
     as a database.

     We also have enabled [DynamoDB Streams](https://aws.amazon.com/blogs/database/dynamodb-streams-use-cases-and-design-patterns/)
     on some of our tables,
     to respond to item changes within the database
     and perform actions like updating OpenSearch indexes
     or putting items into [Redshift by Amazon Web Services (AWS)](/development/stack/aws/redshift).

   - [OpenSearch by Amazon Web Services (AWS)](/development/stack/aws/opensearch)
     (previously known as ElasticSearch)
     as a search provider.
   - [S3 by Amazon Web Services (AWS)](/development/stack/aws/s3):
     - As a durable file system,
     - As an ephemeral file system whose objects are deleted after some time.
     - As a staging area for file uploads/downloads
       (using pre-signed URLs).

1. The Database is backed up
   using Backup Vaults by Amazon Web Services (AWS)
   as promised in [1](/about/security/availability/everything-backed-up)
   and [2](/about/security/availability/recovery-objective).

1. The [Compute component of Common](/development/common/compute)
   provides us with out-of-band processing power
   that we use for things like
   periodic tasks (schedules),
   or tasks that can be computed outside of the request/response lifecycle
   and/or that require more beefy machines
   (like generating PDF reports).

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Integrates](./arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.

### Development Environment

Follow the steps
in the [Development Environment](/development/setup/environment) section
of our documentation.

When prompted for an AWS role, choose `dev`,
and when prompted for a Development Environment, pick `integratesBack`.

### Local Environment

Two approaches for deploying
a local environment of Integrates
are described below.
Either of them will launch a replica
of [app.fluidattacks.com](https://fluidattacks.com)
and `app.fluidattacks.com/api`
on `localhost:8001`.

#### Basic approach

Run each of the following commands in different terminals:

```sh
universe $ m . /integrates/back
universe $ m . /integrates/db
universe $ m . /integrates/front
universe $ m . /integrates/storage/dev
```

Each terminal will serve a key component of Integrates.

#### Using mprocs

You can also use [mprocs](https://github.com/pvolok/mprocs)
for handling all components in a single terminal:

- Run `m . /integrates`.
- Jobs can be restarted using `r`.
- Jobs can be stopped using `x`.
