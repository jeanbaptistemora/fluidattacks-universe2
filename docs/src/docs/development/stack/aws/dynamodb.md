---
id: dynamodb
title: DynamoDB
sidebar_label: DynamoDB
slug: /development/stack/aws/dynamodb
---

## Rationale

[DynamoDB][DYNAMODB] is the database
we use for storing
all the business-related data
in our [ASM][ASM].

The main reasons why we chose it
over other alternatives are:

1. It is a
    [NoSQL][RDBMS]
    database,
    being the perfect fit for our
    [ASM][ASM],
    as it has clear
    [access patterns](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql-B.html)
    and needs to be performant and scalable.
1. It is a
    [SaaS-oriented](https://en.wikipedia.org/wiki/Software_as_a_service)
    database,
    as it does not require
    managing any type of
    infrastructure like
    [networking](https://en.wikipedia.org/wiki/Computer_network)
    or
    [servers](https://en.wikipedia.org/wiki/Server_(computing)).
1. It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
    certifications from
    [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
    and
    [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
    Many of these certifications
    are focused on granting that the entity
    follows best practices regarding secure
    [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing) environments
    and information security.
1. It allows us to retrieve data
    with single-digit millisecond performance
    without having to worry about
    [scalability](https://en.wikipedia.org/wiki/Scalability)
    or
    [availability](https://en.wikipedia.org/wiki/Availability).
1. It is accessed using a
    [public API](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.API.html),
    considerably simplifying the process
    of connecting applications to it.
1. It has a
    [partition-based](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html)
    architecture,
    allowing to handle
    hundreds of [TiBs](https://es.wikipedia.org/wiki/Tebibyte)
    of data
    and peaks of up to [20 million][DYNAMODB]
    requests per second.
1. Database designs can be
    [versioned as code](https://gitlab.com/fluidattacks/product/-/blob/148eccecfb68b6d5cd2c0418679330c0d6c02c2b/integrates/arch/database-design.json)
    using
    [NoSQL Workbench for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html).
1. It supports
    [pagination](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.Pagination.html),
    which is essential
    for keeping applications performant
    when queries return too much data.
1. It supports
    [Global secondary indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.OnlineOps.html),
    allowing to easily add
    new access patterns
    as applications evolve.
1. It supports classic
    [On-demand backups](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/backuprestore_HowItWorks.html),
    allowing us to have
    backups of all our data
    [stored in the cloud](https://gitlab.com/fluidattacks/product/-/blob/cc1e9585a9e94670d040f680d75667907c3c5733/integrates/deploy/backup/terraform/dynamodb.tf).
1. It supports
    [Point-in-Time Recovery](https://gitlab.com/fluidattacks/product/-/blob/cc1e9585a9e94670d040f680d75667907c3c5733/integrates/deploy/database/terraform/integrates-table.tf#L75),
    which helps to
    [restore](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery.html)
    tables to previous states in time
    by using incremental backups.
1. It
    [Integrates](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/RedshiftforDynamoDB.html)
    with
    [Redshift](/development/stack/aws/redshift/),
    partially allowing us to move data to our
    [data warehouse](https://en.wikipedia.org/wiki/Data_warehouse).
1. It supports
    [local deployments](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html),
    allowing us to run [DynamoDB][DYNAMODB]
    on local machines.
    This is especially useful for
    [ephemeral environments](/about/security/integrity/developing-integrity#ephemeral-environments).
1. All its settings can be
    [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_global_table)
    using
    [Terraform](/development/stack/terraform/).
1. It is supported by
    [Terraform state locking](https://www.terraform.io/docs/language/settings/backends/s3.html#dynamodb-state-locking),
    allowing us to
    [avoid race conditions](https://www.terraform.io/docs/language/state/locking.html)
    when applying infrastructure changes.
1. [DynamoDB][DYNAMODB] performance
    can be monitored via
    [CloudWatch](/development/stack/aws/cloudwatch/).
1. It is
    [supported by many programming languages](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.html),
    including
    [Python](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html).
1. It supports
    [Encryption at rest](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/EncryptionAtRest.html),
    allowing us to easily
    keep stored data secure.
1. It
    [fully integrates](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/authentication-and-access-control.html)
    with
    [IAM](/development/stack/aws/iam/),
    allowing to keep a
    [least privilege](/criteria/requirements/186)
    approach
    regarding
    [authentication and authorization](https://securityboulevard.com/2020/06/authentication-vs-authorization-defined-whats-the-difference-infographic/).

## Alternatives

1. [Google Cloud Spanner](https://cloud.google.com/spanner/docs):
    It is a
    [RDBMS][RDBMS],
    meaning that it is not
    as sacalable and performant
    for web-scale applications.
    It requires managing infrastructure like
    clusters, nodes and networks.
    Connecting it to other
    [AWS](/development/stack/aws/)
    services increased complexity.
    It had an unpredictable
    pricing model at the time.
1. [AWS RDS](https://aws.amazon.com/rds/):
    It is a
    [RDBMS][RDBMS],
    meaning that it is not
    as sacalable and performant
    for web-scale applications.
    It requires managing infrastructure like
    clusters, nodes and networks.
1. [Azure Cosmos DB](https://azure.microsoft.com/en-us/free/cosmos-db/):
    Pending to review.

## Usage

We use [DynamoDB][DYNAMODB] for:

1. Storing and retrieving all
    the business-related data
    in our [ASM][ASM].
1. Storing
    [Point-in-Time Recovery backups](https://gitlab.com/fluidattacks/product/-/blob/cc1e9585a9e94670d040f680d75667907c3c5733/integrates/deploy/database/terraform/integrates-table.tf#L75)
    of all our data.
1. Storing
    [On-demand backups](https://gitlab.com/fluidattacks/product/-/blob/cc1e9585a9e94670d040f680d75667907c3c5733/integrates/deploy/backup/terraform/dynamodb.tf)
    of all our data.
1. Keeping a
    [versioned design](https://gitlab.com/fluidattacks/product/-/blob/148eccecfb68b6d5cd2c0418679330c0d6c02c2b/integrates/arch/database-design.json)
    of our database.
1. Managing
    [Terraform state locks](https://www.terraform.io/docs/language/settings/backends/s3.html#dynamodb-state-locking)
    for
    [all our infrastructure modules](https://gitlab.com/fluidattacks/product/-/blob/148eccecfb68b6d5cd2c0418679330c0d6c02c2b/makes/applications/makes/ci/src/terraform/dynamodb_lock.tf).

We are currently migrating to the new
[Database design][DESIGN],
you can track progress
[here](https://gitlab.com/fluidattacks/product/-/issues/4329).

## Guidelines

1. You can access the
    [DynamoDB][DYNAMODB] console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. Any changes to
    [DynamoDB][DYNAMODB]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform/),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).
1. In order to maximize peformance
    and keeping a simple architecture,
    we use a
    [single table approach](https://gitlab.com/fluidattacks/product/-/blob/148eccecfb68b6d5cd2c0418679330c0d6c02c2b/integrates/deploy/database/terraform/integrates-table.tf#L52)
    for our database.
    Please make sure
    you keep all data within that table.
1. Please adhere to our current [design][DESIGN]
    when modifying the
    [DynamoDB logic](https://gitlab.com/fluidattacks/product/-/tree/master/integrates/back/src/dynamodb),
    that way we can keep
    a consistent architecture.
1. You can open the [design][DESIGN] with
    [NoSQL Workbench for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html).

[DYNAMODB]: https://aws.amazon.com/dynamodb/
[ASM]: https://fluidattacks.com/categories/asm/
[RDBMS]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SQLtoNoSQL.WhyDynamoDB.html
[DESIGN]: https://gitlab.com/fluidattacks/product/-/blob/master/integrates/arch/database-design.json
