---
id: introduction
title: DynamoDB
sidebar_label: Introduction
slug: /development/stack/aws/dynamodb/introduction
---

## Rationale

[DynamoDB][DYNAMODB] is the database we use
for storing all the business-related data
in our [ARM][ARM].
The main reasons why we chose it
over other alternatives
are the following:

- It is a [NoSQL][RDBMS] database service
  whose premise is to be performant and scalable no matter the request traffic.
- It is a [SaaS-oriented](https://en.wikipedia.org/wiki/Software_as_a_service)
  database
  since it does not require managing
  any type of infrastructure
  such as [networks](https://en.wikipedia.org/wiki/Computer_network)
  or [servers](<https://en.wikipedia.org/wiki/Server_(computing)>).
- It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
  certifications from [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
  and [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
  Many of these certifications are focused
  on granting that the entity follows best practices
  regarding secure [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing)
  environments
  and information security.
- It was designed to provide
  single-digit millisecond performance
  without having to worry
  about [scalability](https://en.wikipedia.org/wiki/Scalability)
  or [availability](https://en.wikipedia.org/wiki/Availability).
- It is accessed using a [public API](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.API.html).
- It has a [partition-based](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html)
  architecture,
  which allows it to handle
  hundreds of [TiBs](https://es.wikipedia.org/wiki/Tebibyte) of data.
- Database designs can be [versioned as code][DESIGN]
  using [NoSQL Workbench for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html).
- It supports [pagination](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.Pagination.html),
  which is essential
  for keeping applications performant
  when queries return too much data.
- It supports [global secondary indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.OnlineOps.html),
  allowing us to add new access patterns
  as applications evolve.
- It supports classic [on-demand backups](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/backuprestore_HowItWorks.html),
  allowing us to have backups
  of all our data [stored in the cloud](https://gitlab.com/fluidattacks/universe/-/blob/cc1e9585a9e94670d040f680d75667907c3c5733/integrates/deploy/backup/terraform/dynamodb.tf).
- It supports [Point-in-Time Recovery](https://gitlab.com/fluidattacks/universe/-/blob/cc1e9585a9e94670d040f680d75667907c3c5733/integrates/deploy/database/terraform/integrates-table.tf#L75),
  which helps us [restore](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery.html)
  tables to previous states in time
  by using incremental backups.
- It [integrates](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/RedshiftforDynamoDB.html)
  with [Redshift](/development/stack/aws/redshift/),
  partially allowing us to move data
  to our [data warehouse](https://en.wikipedia.org/wiki/Data_warehouse).
- It supports [local deployments](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html),
  i.e.,
  we can run [DynamoDB][DYNAMODB]
  on local machines.
  This is especially useful
  for [ephemeral environments](/about/security/integrity/developing-integrity#ephemeral-environments).
- All its settings can be [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table)
  using [Terraform](/development/stack/terraform/).
- It is supported by [Terraform state locking](https://www.terraform.io/docs/language/settings/backends/s3.html#dynamodb-state-locking),
  which allows us to [avoid race conditions](https://www.terraform.io/docs/language/state/locking.html)
  when applying infrastructure changes.
- Its performance can be monitored
  via [CloudWatch](/development/stack/aws/cloudwatch/).
- It is [supported by many programming languages](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.html),
  including [Python](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html).
- It supports [encryption at rest](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/EncryptionAtRest.html),
  allowing us to easily
  keep stored data secure.
- It [fully integrates](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/authentication-and-access-control.html)
  with [IAM](/development/stack/aws/iam/),
  allowing us to keep
  a [least privilege](/criteria/requirements/186) approach
  regarding [authentication and authorization](https://securityboulevard.com/2020/06/authentication-vs-authorization-defined-whats-the-difference-infographic/).

## Alternatives

- **[Google Cloud Spanner](https://cloud.google.com/spanner/docs):**
  It is a Relational Database Management System ([RDBMS][RDBMS]),
  which means it is not as scalable and performant
  for web-scale applications.
  It requires managing infrastructures
  such as clusters, nodes and networks.
  Connecting it to other [AWS](/development/stack/aws/) services
  increased complexity.
  In addition,
  it had an unpredictable
  pricing model at the time.
- **[AWS RDS](https://aws.amazon.com/rds/):**
  It is an RDBMS,
  which means it is not as scalable and performant
  for web-scale applications.
  It requires managing infrastructures
  such as clusters, nodes and networks.

> **Note:** > [Azure Cosmos DB](https://azure.microsoft.com/en-us/free/cosmos-db/)
> is another alternative.
> A review is pending.

## Usage

We use [DynamoDB][DYNAMODB] for

- storing and retrieving all the business-related data
  in our [ARM][ARM];
- storing [Point-in-Time Recovery backups](https://gitlab.com/fluidattacks/universe/-/blob/9983b45250644945ebbc7915484848bc80d6ee10/integrates/infra/src/db.tf#L167)
  of all our data;
- storing [on-demand backups](https://gitlab.com/fluidattacks/universe/-/blob/9983b45250644945ebbc7915484848bc80d6ee10/integrates/infra/src/backup.tf)
  of all our data;
- keeping a [versioned design][DESIGN]
  of our database, and
- managing [Terraform state locks](https://www.terraform.io/docs/language/settings/backends/s3.html#dynamodb-state-locking)
  for [all our infrastructure modules](https://gitlab.com/fluidattacks/universe/-/blob/9983b45250644945ebbc7915484848bc80d6ee10/common/ci/infra/lock.tf).

## Guidelines

- You can access the [DynamoDB][DYNAMODB] console
  after [authenticating to AWS](/development/stack/aws#guidelines).
- Any changes to [DynamoDB][DYNAMODB] infrastructure
  must be done
  via [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
- To learn how to test and apply infrastructure
  via [Terraform](/development/stack/terraform/),
  visit the [Terraform Guidelines](/development/stack/terraform#guidelines).
- Following [AWS best practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html),
  we use a single table design for our database.
- You can view the design
  with [NoSQL Workbench for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html).

[DYNAMODB]: https://aws.amazon.com/dynamodb/
[ARM]: https://fluidattacks.com/categories/arm/
[RDBMS]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SQLtoNoSQL.WhyDynamoDB.html
[DESIGN]: https://gitlab.com/fluidattacks/universe/-/blob/trunk/integrates/arch/database-design.json
