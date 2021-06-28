---
id: sagemaker
title: SageMaker
sidebar_label: SageMaker
slug: /development/stack/aws/sagemaker
---

## Rationale

[SageMaker][SAGEMAKER] is the platform we use
for developing solutions involving
[Machine Learning][ML].

The main reasons why we chose it
over other alternatives are:

1. It integrates with
    [EC2][EC2],
    allowing to easily provision
    [cloud](https://en.wikipedia.org/wiki/Cloud_computing)
    computing resources.
    Such feature is essential
    in order to have
    [horizontal autoscaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/).
1. It integrates with [S3][S3],
    allowing us easily to store
    raw data,
    datasets
    and training outputs
    in our [S3 Bucket](https://gitlab.com/fluidattacks/product/-/blob/f630ceecb7015146118ef8e9aa4f2576a13785e6/sorts/infra/s3.tf).
1. It supports
    a [wide range](https://aws.amazon.com/sagemaker/pricing/)
    of [EC2][EC2] [ML-specific][ML] machines
    for training models.
1. It supports
    [EC2 spot machines](https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html),
    allowing to
    [considerably reduce machine costs](https://aws.amazon.com/ec2/spot/pricing/).
1. Thanks to its
    [horizontal autoscaling](https://www.section.io/blog/scaling-horizontally-vs-vertically/)
    capabilities,
    it is very easy
    to implement [parallelism](https://en.wikipedia.org/wiki/Parallel_computing)
    by running several
    [models](https://gitlab.com/fluidattacks/product/-/blob/f630ceecb7015146118ef8e9aa4f2576a13785e6/sorts/training/sagemaker_provisioner.py#L69)
    or
    [feature combinations](https://gitlab.com/fluidattacks/product/-/blob/f630ceecb7015146118ef8e9aa4f2576a13785e6/sorts/training/constants.py#L38)
    in separate machines,
    greatly increasing
    training performance.
1. It supports
    [Hyperparametrization](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-define-ranges.html),
    allowing to concurrently
    [train several instances of a model](https://gitlab.com/fluidattacks/product/-/blob/f630ceecb7015146118ef8e9aa4f2576a13785e6/sorts/training/constants.py#L68)
    using different parameter values.
    Such feature is essential
    for optimizing
    our most accurate model.
1. It
    [integrates](https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam.html)
    with
    [IAM](/development/stack/aws/iam/),
    allowing to keep a
    [least privilege](/criteria/requirements/186)
    approach
    regarding
    [authentication and authorization](https://securityboulevard.com/2020/06/authentication-vs-authorization-defined-whats-the-difference-infographic/).
1. It supports a
    [wide range of frameworks](https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html),
    including [scikit-learn](https://scikit-learn.org/),
    the one that [Sorts](https://gitlab.com/fluidattacks/product/-/tree/f630ceecb7015146118ef8e9aa4f2576a13785e6/sorts)
    uses.
1. [EC2][EC2] workers performance
    can be [monitored](https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html)
    via [CloudWatch](/development/stack/aws/cloudwatch/).
1. Logs for training jobs
    can be [monitored](https://docs.aws.amazon.com/sagemaker/latest/dg/logging-cloudwatch.html)
    via [CloudWatch](/development/stack/aws/cloudwatch/).

## Alternatives

1. [IBM Watson Studio](https://www.ibm.com/cloud/watson-studio):
    It does not integrate with [EC2][EC2] or [S3][S3],
    increasing overall complexity.
    Pending to review.
1. [GCP Vertex AI](https://cloud.google.com/vertex-ai):
    It does not integrate with [EC2][EC2] or [S3][S3],
    increasing overall complexity.
    Pending to review.
1. [Azure machine learning](https://azure.microsoft.com/en-us/services/machine-learning/):
    It does not integrate with [EC2][EC2] or [S3][S3],
    increasing overall complexity.
    Pending to review.

## Usage

1. We use [SageMaker][SAGEMAKER]
    as the [Machine Learning][ML]
    platform for training
    [sorts](https://gitlab.com/fluidattacks/product/-/tree/f630ceecb7015146118ef8e9aa4f2576a13785e6/sorts),
    our [ML-based][ML] software vulnerability scanner.
1. We do not use
    [SageMaker spot instances](https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html).
    Pending to implement.

## Guidelines

1. You can access the
    [SageMaker][SAGEMAKER] console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. Any changes to
    [SageMaker][SAGEMAKER]
    configurations must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
    by modifying its
    [estimator configuration](https://gitlab.com/fluidattacks/product/-/blob/f630ceecb7015146118ef8e9aa4f2576a13785e6/sorts/training/sagemaker_provisioner.py#L31).

[SAGEMAKER]: https://aws.amazon.com/sagemaker/
[ML]: https://en.wikipedia.org/wiki/Machine_learning
[EC2]: https://aws.amazon.com/ec2/
[S3]: /development/stack/aws/s3/
