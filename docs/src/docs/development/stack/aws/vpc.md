---
id: vpc
title: Virtual Private Cloud (VPC)
sidebar_label: VPC
slug: /development/stack/aws/vpc
---

## Rationale

We use [AWS VPC][VPC] for hosting
our own private network
in the [cloud](https://en.wikipedia.org/wiki/Cloud_computing).
It allows us to manage network configurations like
[subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html),
[IP addressing](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html),
[Internet gateways](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html),
[Routing tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html),
[Security groups][SECURITY-GROUPS],
among others.

The main reasons why we chose it
over other alternatives are:

1. It is a core [AWS](/development/stack/aws/)
    service,
    which means that in order to be able to
    use other [AWS](/development/stack/aws/) services
    that rely on networking,
    one must use [VPC][VPC].
1. It integrates with services that use
    networking-dependant infrastructure like
    [EC2](/development/stack/aws/ec2/),
    [Redis](/development/stack/aws/redis/),
    [Elastic Load Balancing](/development/stack/aws/elb/),
    [AWS Redshift](/development/stack/aws/redshift/),
    etc.
1. It supports [Subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#vpc-subnet-basics),
    which allows to have multiple network segments,
    each of them existing in a separate
    [availability zone](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html),
    granting [network redundancy](https://en.wikipedia.org/wiki/Redundancy_(engineering)).
1. It supports [Security groups][SECURITY-GROUPS]
    that allow to specify inbound and outbound rules for
    [network interfaces](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html).
    Such rules can be based on other
    [security groups][SECURITY-GROUPS],
    [IP segments](https://en.wikipedia.org/wiki/IP_address),
    and [communication protocols](https://en.wikipedia.org/wiki/Communication_protocol).
1. It supports [Internet gateways](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)
    that provide [NAT](https://en.wikipedia.org/wiki/Network_address_translation)
    to machines with
    [Internet](https://en.wikipedia.org/wiki/Internet) access.
1. It supports [Routing tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html),
    allowing to customize routing inside the network.
1. It supports [DHCP](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_DHCP_Options.html),
    allowing to easily assign private
    [IP addresses](https://en.wikipedia.org/wiki/IP_address)
    to machines as they are created.
1. Resources can be
    [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)
    using
    [Terraform](/development/stack/terraform/).

## Alternatives

1. [Google Virtual Private Cloud (VPC)](https://cloud.google.com/vpc/):
    It provides a more [SaaS-like](https://en.wikipedia.org/wiki/Software_as_a_service)
    approach to networking.
    Configuring networks is easier,
    but also less parametrizable.
1. [Azure Virtual Network](https://azure.microsoft.com/en-us/free/virtual-network/):
    It did not exist at the time we migrated to the cloud.
    Pending to review.

## Usage

We use [VPC][VPC] for setting
networking and security configurations for:

1. [EC2](/development/stack/aws/ec2/) machines.
1. [Redis cluster](/development/stack/aws/redis/) workers.
1. [Kubernetes cluster](/development/stack/kubernetes/) workers.
1. [Batch](https://aws.amazon.com/batch/) workers.
1. [Elastic Load Balancing](/development/stack/aws/elb/)
    load balancers.

## Guidelines

1. You can access the
    [AWS VPC][VPC] console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. Any changes to
    [VPC's][VPC]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
    by modifying its
    [Terraform module](https://gitlab.com/fluidattacks/product/-/tree/1aa1cbe233dcd683d372df6ed547c899a7ba0168/makes/applications/makes/vpc/src/terraform).
1. To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform/),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).

[VPC]: https://aws.amazon.com/vpc/
[SECURITY-GROUPS]: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html
