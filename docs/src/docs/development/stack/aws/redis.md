---
id: redis
title: Redis
sidebar_label: Redis
slug: /development/stack/aws/redis
---

## Rationale

We use [Redis][REDIS]
as the [cache database](https://en.wikipedia.org/wiki/Database_caching)
for our [ASM][ASM].

The main reasons why we chose it
over other alternatives are:

1. It supports
    [clustering](https://redis.io/topics/cluster-tutorial),
    allowing to
    [distribute data accross nodes](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.NodeGroups.html),
    granting
    [horizontal autoscaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/)
    capabilities.
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
1. It can exist within the same [VPC](/development/stack/aws/vpc/)
    as AWS-hosted applications like our
    [ASM][ASM].
1. As it exists
    within the same [VPC](/development/stack/aws/vpc/)
    as our [ASM][ASM],
    cached data only has to travel
    within the local network,
    increasing overrall application performance.
1. It supports
    [complex data types](https://redis.io/topics/data-types),
    which considerably simplifies
    [mapping data from applications](https://gitlab.com/fluidattacks/universe/-/blob/148eccecfb68b6d5cd2c0418679330c0d6c02c2b/integrates/arch/2021-01-27-cache-design.md)
    to it.
1. It supports
    [local deployments](https://redis.io/topics/cluster-tutorial),
    allowing us to run [Redis][REDIS]
    on local machines.
    This is especially useful for
    [ephemeral environments](/about/security/integrity/developing-integrity#ephemeral-environments).
1. It can be fully managed
    [as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticache_replication_group)
    using
    [Terraform](/development/stack/terraform/).
1. It supports a wide range of
    [cache node sizes](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html),
    which come preconfigured
    and are
    [very easy to set](https://gitlab.com/fluidattacks/universe/-/blob/148eccecfb68b6d5cd2c0418679330c0d6c02c2b/integrates/deploy/cache-db/terraform/database.tf#L34).
1. It supports
    [VPC security groups](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/GettingStarted.AuthorizeAccess.html),
    allowing to specify
    networking inbound and outbound rules
    for
    [IP addresses](https://en.wikipedia.org/wiki/IP_address),
    [ports](https://en.wikipedia.org/wiki/Port_(computer_networking))
    and other security groups.
1. It quickly adds support
    to the newest
    [Redis versions](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/supported-engine-versions.html).
1. [Redis][REDIS] cluster performance
    can be monitored via
    [CloudWatch](/development/stack/aws/cloudwatch/).

## Alternatives

1. [AWS DynamoDB Accelerator (DAX)](https://aws.amazon.com/dynamodb/dax/):
    It is a cache
    that sits between [DynamoDB][DYNAMODB]
    and the application,
    allowing to cache data
    without having to maintain an
    [extra layer of complexity](https://gitlab.com/fluidattacks/universe/-/tree/148eccecfb68b6d5cd2c0418679330c0d6c02c2b/integrates/back/src/redis_cluster)
    in your application.
    It does not support local deployments,
    its [query cache](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.concepts.html#DAX.concepts.query-cache)
    is not granular,
    generating inconsistencies
    when data changes via
    [granular operations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.concepts.html#DAX.concepts.item-cache),
    it has a [poorly maintained](https://pypi.org/project/amazon-dax-client/2.0.0/)
    client.
1. [AWS DynamoDB (No cache)][DYNAMODB]:
    We are considering
    removing the entire
    [extra layer of complexity](https://gitlab.com/fluidattacks/universe/-/tree/148eccecfb68b6d5cd2c0418679330c0d6c02c2b/integrates/back/src/redis_cluster)
    that cache brings with it
    and only using [DynamoDB][DYNAMODB],
    as it already provides
    very good performance.
    This could considerably simplify
    our [ASM][ASM] architecture
    by slightly reducing its performance.

## Usage

We use [Redis][REDIS] for:

1. Retrieving cached data
    from our [ASM][ASM].
1. Managing our [ASM][ASM] sessions.

## Guidelines

1. You can access the
    [Redis][REDIS] console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. Any changes to
    [Redis][REDIS]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
    by modifying its
    [Terraform module](https://gitlab.com/fluidattacks/universe/-/tree/trunk/integrates/deploy/cache-db/terraform).
1. To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform/),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).
1. Please adhere to our current
    [design](https://gitlab.com/fluidattacks/universe/-/blob/trunk/integrates/arch/2021-01-27-cache-design.md)
    when modifying the
    [Redis logic](https://gitlab.com/fluidattacks/universe/-/tree/trunk/integrates/back/src/redis_cluster),
    that way we can keep
    a consistent architecture.
1. When working on our [ASM][ASM],
    sometimes you will need
    to invalidate [Redis][REDIS] cache,
    you can do this
    by using the `invalidateCache` mutation.
    Please visit our [API Documentation section](https://app.fluidattacks.com/api)
    for more information.

[ASM]: https://fluidattacks.com/categories/asm/
[REDIS]: https://aws.amazon.com/redis/
[DYNAMODB]: /development/stack/aws/dynamodb/
