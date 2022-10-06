---
id: introduction
title: Amazon Web Services (AWS)
sidebar_label: Introduction
slug: /development/stack/aws
---

## Rationale

[AWS][aws] is our main [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service)
cloud provider.
The main reasons why we chose it
over other alternatives
are the following:

- It provides a highly granular approach to [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service),
  offering over [one hundred independent services][aws]
  that range from [quantum computing](https://aws.amazon.com/braket)
  to [servers for videogames](https://aws.amazon.com/gamelift).
- It has a fully granular
  [pay-as-you-go](https://aws.amazon.com/pricing)
  pricing model,
  which allows us to pay exactly
  for what we are using.
- It complies with
  many global [top security standards](https://aws.amazon.com/compliance/programs/).
- It has a [highly redundant infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/?hp=tile&tile=map)
  distributed across the world,
  making us feel comfortable
  when it comes to its [availability and reliability](https://status.aws.amazon.com/).
- It is a cloud infrastructure leader,
  [according to Gartner](https://www.c-sharpcorner.com/article/top-10-cloud-service-providers/).
- It is the [oldest cloud provider](https://www.techaheadcorp.com/blog/top-cloud-service-providers/#:~:text=Since%20AWS%20is%20the%20oldest,recently%20launched%20AWS%20Storage%20Gateway.).

## Alternatives

[Google Cloud Platform](https://cloud.google.com/gcp)
is an alternative
that did not exist at the time we migrated to the cloud.
Its service catalog is much smaller,
which means less flexibility.

> **Note:**
>
> [Microsoft Azure](https://azure.microsoft.com/en-us/)
> is another alternative
> that did not exist at the time we migrated to the cloud.
> A review is pending.

## Usage

We use the following [AWS][aws] services:

- **Identity and access management:** [IAM](/development/stack/aws/iam/)
- **Cost management:** [Cost Management](/development/stack/aws/cost-management/)
- **Monitoring and logging:** [CloudWatch](/development/stack/aws/cloudwatch/)
- **Elastic cloud computing:** [EC2](/development/stack/aws/ec2/)
- **Cloud file storage:** [S3](/development/stack/aws/s3/)
- **Serverless computing:** [Lambda](/development/stack/aws/lambda/)
- **Elastic block store:** [EBS](/development/stack/aws/ebs/)
- **Elastic load balancing:** [ELB](/development/stack/aws/elb/)
- **Key management system:** [KMS](/development/stack/aws/kms/)
- **Application cluster:** [EKS](/development/stack/aws/eks/)
- **Virtual private cloud:** [VPC](/development/stack/aws/vpc/)
- **NoSQL database:** [DynamoDB](/development/stack/aws/dynamodb/introduction/)
- **Cloud VPN:** [VPN](/development/stack/aws/vpn/)
- **In-memory cache:** [Redis](/development/stack/aws/redis/)
- **Data warehouse:** [Redshift](/development/stack/aws/redshift/)
- **Batch processing:** [Batch](/development/stack/aws/batch/)
- **Machine learning:** [SageMaker](/development/stack/aws/sagemaker/)
- **Elastic container service:** [ECS](https://aws.amazon.com/ecs/)
- **Simple queue service:** [SQS](https://aws.amazon.com/sqs/)

## Guidelines

### Access web console

You can access the AWS Console
by entering the AWS - Production application
through [Okta](/development/stack/okta).
