---
id: introduction
title: Amazon Web Services (AWS)
sidebar_label: Introduction
slug: /development/stack/aws
---

## Rationale

[AWS][AWS] is our main [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service)
cloud provider.
The main reasons why we chose it
over other alternatives
are the following:

- It provides a highly granular approach to [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service),
  offering over [one hundred independent services][AWS]
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

- **[Google Cloud Platform](https://cloud.google.com/gcp):**
  It did not exist at the time we migrated to the cloud.
  Its service catalog is much smaller,
  which means less flexibility.
- **[Microsoft Azure](https://azure.microsoft.com/en-us/):**
  It did not exist at the time we migrated to the cloud.
  A deeper review is still pending.

## Usage

We use the following [AWS][AWS] services:

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
- **NoSQL database:** [DynamoDB](/development/stack/aws/dynamodb/)
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

### Get development keys

Developers can use [Okta](/development/stack/okta)
to get development AWS credentials.
Follow these steps
to generate a key pair:

1. Install `awscli` and `aws-okta-processor`.

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

    Be sure to replace the parameters.
        - `<user-email>`: Email.
        - `<user-password>`.
        - `<default-role>`: Use `dev` or another role.

1. Source your profile.

    ```bash
    source ~/.profile
    ```

1. To get the credentials,
   execute the following:

    ```bash
    okta-login # To use the default role
    ```

    ```bash
    okta-login `<role>` # To use a specific role
    ```

1. Use the `--no-aws-cache` flag only in case you
    - are running a local environment connected to production, or
    - have problems with `okta-login`
      or AWS credentials.

[AWS]: https://aws.amazon.com/
