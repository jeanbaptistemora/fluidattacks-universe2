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

We use the following [AWS](https://aws.amazon.com/) services:

1. Elastic cloud computing:
[AWS EC2](https://aws.amazon.com/ec2/).
1. Serverless computing:
[AWS Lambda](https://aws.amazon.com/lambda/).
1. Cloud file storage:
[AWS S3](https://aws.amazon.com/s3/).
1. NoSQL database:
[AWS DynamoDB](https://aws.amazon.com/dynamodb/).
1. Data wareouse:
[AWS Redshift](https://aws.amazon.com/redshift/).
1. Key management system:
[AWS KMS](https://aws.amazon.com/kms/).
1. Cache:
[AWS Redis](https://aws.amazon.com/redis/).
1. Application cluster:
[AWS EKS](https://aws.amazon.com/eks/).
1. Batch processing:
[AWS Batch](https://aws.amazon.com/batch/).
1. Machine learning:
[AWS SageMaker](https://aws.amazon.com/sagemaker/).
1. Secrets manager:
[AWs Secrets Manager](https://aws.amazon.com/secrets-manager/).
1. Simple queue service:
[AWS SQS](https://aws.amazon.com/sqs/).
1. Monitoring and logging:
[AWS CloudWatch](https://aws.amazon.com/cloudwatch/).
2. Cost management:
[AWS Cost Management](https://aws.amazon.com/aws-cost-management/).

## Guidelines

1. You can access the AWS Console
by entering the `AWS - Production`
application via [Okta](/development/stack/okta).
