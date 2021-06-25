---
id: redshift
title: Redshift
sidebar_label: Redshift
slug: /development/stack/aws/redshift
---

## Rationale

We use [Redshift][REDSHIFT]
as a [data warehouse](https://en.wikipedia.org/wiki/Data_warehouse)
for all our analytics processes.

The main reasons why we chose it
over other alternatives are:

1. It is
    [designed for online analytic processing (OLAP)](https://docs.aws.amazon.com/en_en/redshift/latest/dg/c_redshift-and-postgres-sql.html),
    which grants complete flexibility
    for executing complex queries
    against large datasets.
    This requirement is a must
    in order to be able to answer
    all kinds of business-related questions
    based on our data.
1. It supports
    [clustering](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html),
    allowing to
    [distribute data accross nodes](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#rs-ra3-node-types),
    granting
    [horizontal autoscaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/)
    capabilities.
1. Its [princing model](https://aws.amazon.com/redshift/pricing/)
    is infrastrucutre-based,
    meaning that you pay for
    the size and number of nodes
    your cluster has.
    Such approach makes it
    very cheap when compared to other
    [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service)
    data warehouses.
1. It creates
    [incremental snapshots](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-snapshots.html)
    of your data every eight hours,
    allowing you to revert
    to a previous state
    in case the need arises.
1. Although [Redshift][REDSHIFT]
    is not [Open source](https://opensource.com/resources/what-open-source),
    it is supported by [PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL),
    allowing us to locally simulate a Redshift-like databases
    for testing.
1. It is
    [supported by ChartIO](https://chartio.com/docs/data-sources/connect/amazon-redshift/),
    our analytics visualization tool.
1. It can be partially managed (tables not supported)
    [as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/redshift_cluster)
    using
    [Terraform](/development/stack/terraform/).
1. It supports
    [encryption at rest](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-db-encryption.html#working-with-aws-kms)
    using
    [KMS](/development/stack/aws/kms/).
1. It
    [fully integrates](https://docs.aws.amazon.com/redshift/latest/mgmt/redshift-iam-access-control-identity-based.html)
    with
    [IAM](/development/stack/aws/iam/),
    allowing to keep a
    [least privilege](/criteria/requirements/186)
    approach
    regarding
    [authentication and authorization](https://securityboulevard.com/2020/06/authentication-vs-authorization-defined-whats-the-difference-infographic/).
1. It supports
    [VPC security groups](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-security-groups.html),
    allowing to specify
    networking inbound and outbound rules
    for
    [IP addresses](https://en.wikipedia.org/wiki/IP_address),
    [ports](https://en.wikipedia.org/wiki/Port_(computer_networking))
    and other security groups.
1. Cluster nodes performance
    can be monitored via
    [CloudWatch](/development/stack/aws/cloudwatch/).

## Alternatives

1. [AWS Athena](https://aws.amazon.com/athena/):
    It is a [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service)
    database, meaning that no infrastructure
    maintainance is required.
    Its [pricing model](https://aws.amazon.com/athena/pricing/)
    is based on the
    `number of TBs of data scaned by each query`,
    which makes it considerably more expensive
    in the long term.
    Pending to review.
1. [Google BigQuery](https://cloud.google.com/bigquery):
    Pending to review.
1. [Snowflake](https://www.snowflake.com/):
    Pending to review.

## Usage

1. We use [Redshift][REDSHIFT]
    for storing data
    from [many of our services](https://gitlab.com/fluidattacks/product/-/tree/56b145a05ca4ff05cec79a65c6b1cab16d16fba3/observes/singer)
    and then visualizing it using [ChartIO](https://chartio.com/).
1. Our [Redshift][REDSHIFT] architecture
    is not documented.
    Pending to implement.
1. Our [Redshift][REDSHIFT] cluster
    is not written as code
    using [Terraform](/development/stack/terraform/).
    Pending to implement.
1. Our [Redshift][REDSHIFT]
    is not encrypted at rest
    using [KMS](/development/stack/aws/kms/).
    Pending to implement.

## Guidelines

You can access the
[Redshift][REDSHIFT] console
after [authenticating on AWS](/development/stack/aws#guidelines).

[REDSHIFT]: https://aws.amazon.com/redshift/
