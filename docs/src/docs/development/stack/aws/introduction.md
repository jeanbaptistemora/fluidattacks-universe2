---
id: introduction
title: Amazon Web Services (AWS)
sidebar_label: Introduction
slug: /development/stack/aws
---

## Rationale

[AWS][AWS] is our main
[IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service)
cloud provider.

The main reasons why we chose it
over other alternatives are:

1. It provides a highly granular approach to
    [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service),
    offering over
    [one hundred independent services][AWS]
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

We use the following [AWS][AWS] services:

1. Identity and Access Management:
    [IAM](/development/stack/aws/iam/).
1. Cost management:
    [Cost Management](/development/stack/aws/cost-management/).
1. Monitoring and logging:
    [CloudWatch](/development/stack/aws/cloudwatch/).
1. Elastic cloud computing:
    [EC2](/development/stack/aws/ec2/).
1. Cloud file storage:
    [S3](/development/stack/aws/s3/).
1. Serverless computing:
    [Lambda](/development/stack/aws/lambda/).
1. Elastic block store:
    [EBS](/development/stack/aws/ebs/).
1. Elastic Load Balancing:
    [ELB](/development/stack/aws/elb/).
1. Key management system:
    [KMS](/development/stack/aws/kms/).
1. Application cluster:
    [EKS](/development/stack/aws/eks/).
1. Virtual private cloud:
    [VPC](/development/stack/aws/vpc/).
1. NoSQL database:
    [DynamoDB](/development/stack/aws/dynamodb/).
1. In-memory cache:
    [Redis](/development/stack/aws/redis/).
1. Data warehouse:
    [Redshift](/development/stack/aws/redshift/).
1. Batch processing:
    [Batch](/development/stack/aws/batch/).
1. Machine learning:
    [SageMaker](/development/stack/aws/sagemaker/).
1. Elastic Container Service:
    [ECS](https://aws.amazon.com/ecs/).
1. Simple queue service:
    [SQS](https://aws.amazon.com/sqs/).

## Guidelines

### Access web console

You can access the AWS Console
by entering the `AWS - Production`
application via [Okta](/development/stack/okta).

### Get development keys

Developers can use
[Okta](/development/stack/okta)
to get development AWS credentials.

Follow these steps
to generate a key pair:

1. Install `awscli` and `aws-okta-processor`:

    ```bash
    nix-env -i awscli
    pip install aws-okta-processor
    ```

1. Add the following function
    in your shell profile (`~/.bashrc`):

    ```bash
    function okta-login {
      local role="${1:-<default-role>}" # Set as default role the role that you uses most
      local role_uppercase="$(echo "${role^^}" | tr - _)" # Used to export the "PRODUC_ENV_*" vars
      local env="${role_uppercase##*_}" # Services compatibility
      local args=(
        authenticate
        --user "<user-email>"
        --pass "<user-password>"
        --organization "fluidattacks.okta.com"
        --role "arn:aws:iam::205810638802:role/${role}"
        --application "https://fluidattacks.okta.com/home/amazon_aws/0oa9ahz3rfx1SpStS357/272"
        --silent
        --duration 32400
        --environment
      ) # Flags required to aws-okta-processor

      if [ "${env}" == 'PROD' ]
      then
        args+=("--no-aws-cache") # If env is PROD cache is not used
      fi \
        && eval $(aws-okta-processor "${args[@]}") \
        && export "${role_uppercase}_AWS_ACCESS_KEY_ID"="${AWS_ACCESS_KEY_ID}" \
        && export "${role_uppercase}_AWS_SECRET_ACCESS_KEY"="${AWS_SECRET_ACCESS_KEY}" \
        && export "${env}_AWS_ACCESS_KEY_ID"="${AWS_ACCESS_KEY_ID}" \
        && export "${env}_AWS_SECRET_ACCESS_KEY"="${AWS_SECRET_ACCESS_KEY}"
    }
    ```

    Make sure you replace the parameters:
        - `<user-email>`: Email.
        - `<user-password>`.
        - `<default-role>`: Use `dev` or another role.

1. Source your profile:

    ```bash
    source ~/.profile
    ```

1. To get the credentials execute:

    ```bash
    okta-login # To use the default role
    ```

    ```bash
    okta-login `<role>` # To use a specific role
    ```

1. Use the `--no-aws-cache` flag only in case you:
    - Run as prod.
    - Have problems with `okta-login` or aws credentials.

[AWS]: https://aws.amazon.com/
