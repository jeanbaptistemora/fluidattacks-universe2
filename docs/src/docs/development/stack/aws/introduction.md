---
id: introduction
title: Amazon Web Services
sidebar_label: Introduction
slug: /development/stack/aws
---

## Rationale

[AWS](https://aws.amazon.com/) is our main
[IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service)
cloud provider.

The main reasons why we chose it
over other alternatives are:

1. It provides a highly granular approach to
[IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service),
offering over
[one hundred independant services](https://aws.amazon.com/)
that range from
[quantum computing](https://aws.amazon.com/braket)
to
[servers for videogames](https://aws.amazon.com/gamelift).
1. It has a fully granular
[pay-as-you-go](https://aws.amazon.com/pricing)
pricing model,
which allows us to pay exactly for what
we are using.
1. It complies with
many global
[top security standards](https://aws.amazon.com/compliance/programs/).
1. It has a
[highly redundant infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/?hp=tile&tile=map)
that is distributed across the world,
making us feel comfortable
when it comes to its
[availability and reliability](https://status.aws.amazon.com/).
1. It is a cloud infrastructure leader
[according to Gartner](https://www.c-sharpcorner.com/article/top-10-cloud-service-providers/).
1. It is the
[oldest cloud provider](https://www.techaheadcorp.com/blog/top-cloud-service-providers/#:~:text=Since%20AWS%20is%20the%20oldest,recently%20launched%20AWS%20Storage%20Gateway.).

## Alternatives

1. [Google Cloud Platform](https://cloud.google.com/gcp):
It did not exist at the time we migrated to the cloud.
Its service catalogue is much smaller,
thus reducing its flexibility.
1. [Microsoft Azure](https://azure.microsoft.com/en-us/):
It did not exist at the time we migrated to the cloud.
A deeper review is still pending.

## Usage

We use [AWS](https://aws.amazon.com/) for:

1. [Cloud computing](https://aws.amazon.com/ec2/).
1. [Serverless computing](https://aws.amazon.com/lambda/).
1. [Cloud file storage](https://aws.amazon.com/s3/).
1. [NoSQL database](https://aws.amazon.com/dynamodb/).
1. [Data wareouse](https://aws.amazon.com/redshift/).
1. [Key management system](https://aws.amazon.com/kms/).
1. [Cache](https://aws.amazon.com/redis/).
1. [Application cluster](https://aws.amazon.com/eks/).
1. [Batch processing](https://aws.amazon.com/batch/).
1. [Machine learning](https://aws.amazon.com/sagemaker/).
1. [Secrets manager](https://aws.amazon.com/secrets-manager/).
1. [Simple queue service](https://aws.amazon.com/sqs/).
1. [Monitoring](https://aws.amazon.com/cloudwatch/).
1. [Cost management](https://aws.amazon.com/aws-cost-management/).

## Guidelines

1. You can access the AWS Console
by entering the `AWS - Production`
application via [Okta](/development/stack/okta).
