---
id: cloudwatch
title: CloudWatch
sidebar_label: CloudWatch
slug: /development/stack/aws/cloudwatch
---

## Rationale

We use [CloudWatch][CLOUDWATCH] for monitoring all our
[AWS][AWS] infrastructure.
It allows us to
monitor our applications,
react to performance changes within those applications,
optimize resource utilization,
and get a unified view of operational health.

The main reasons why we chose it
over other alternatives are:

1. It is a core [AWS][AWS] service.
    Once one starts creating infrastructure,
    [CloudWatch][CLOUDWATCH]
    begins to monitor it.
1. It seamlessly integrates with most [AWS][AWS] services.
    Some examples are
    [EC2][EC2],
    [S3](/development/stack/aws/s3/),
    and
    [DynamoDB](/development/stack/aws/dynamodb/).
1. It supports
    [custom dashboards](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create_dashboard.html)
    for visualizing metrics using diagrams like
    bars, pies, numbers, among others.
    Other customizations like timespans
    and using
    [resource metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/viewing_metrics_with_cloudwatch.html)
    as axes are also available.
1. It supports
    [alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
    using [AWS SNS](https://aws.amazon.com/sns/),
    allowing to trigger email notifications
    when
    [resource metric conditions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ConsoleAlarms.html)
    are not met or
    [anomailes are detected](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Anomaly_Detection_Alarm.html).
1. Resources can be
    [written as code](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
    using
    [Terraform](/development/stack/terraform/).

## Alternatives

1. [GCP Cloud Monitoring](https://cloud.google.com/monitoring):
    It did not exist at the time we migrated to the cloud.
    Pending to review.
1. [Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/overview):
    It did not exist at the time we migrated to the cloud.
    Pending to review.

## Usage

We use [CloudWatch][CLOUDWATCH] for monitoring:

1. [EC2][EC2]
    instance performance.
1. [EBS](/development/stack/aws/ebs/)
    disk usage and performance.
1. [S3](/development/stack/aws/s3/)
    bucket size and object number.
1. [Elastic load balancing](/development/stack/aws/elb/)
    load balancer performance.
1. [Redshift](https://aws.amazon.com/redshift/)
    database usage and performance.
1. [Redis cache cluster](/development/stack/aws/redis/)
    usage and performance.
1. [DynamoDB](/development/stack/aws/dynamodb/)
    tables usage and performance.
1. [SQS](https://aws.amazon.com/sqs/)
    sent, delayed, received and deleted messages.
1. [ECS](https://aws.amazon.com/ecs/)
    cluster resource reservation and utilization.
1. [Lambda][LAMBDA]
    invocations, errors, duration, among others.

We do not use [CloudWatch][CLOUDWATCH] for:

1. [Synthetic monitoring](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html):
    We use [Checkly](https://www.checklyhq.com/) instead.
1. [Service lens](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ServiceLens.html):
    It only supports
    [Lambda][LAMBDA] functions,
    [API Gateway](https://aws.amazon.com/api-gateway/),
    and [Java-based](https://en.wikipedia.org/wiki/Java_(programming_language))
    applications.
1. [Contrinutor insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights.html):
    We use [Cloudflare](/development/stack/cloudflare/) instead.
1. [Container insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html)
    We use [New Relic](https://newrelic.com/). Pending to review.
1. [Lambda insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights.html):
    We currently use [Lambda][LAMBDA]
    for a few non-critical tasks.
1. [Cloudwatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html):
    It could increase visibility for
    [EC2][EC2] machines.
    Pending to review.
1. [Cloudwatch application insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-application-insights.html):
    It only supports [Java-based](https://en.wikipedia.org/wiki/Java_(programming_language))
    applications.
1. Writing our
    [alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
    as code using
    [Terraform](/development/stack/terraform/).
    Pending to do.

## Guidelines

1. You can access the
    [CloudWatch][CLOUDWATCH] console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. You can watch [CloudWatch][CLOUDWATCH]
    metrics from the monitoring section
    of each [AWS][AWS] service.

[AWS]: /development/stack/aws/
[CLOUDWATCH]: https://aws.amazon.com/cloudwatch/
[LAMBDA]: /development/stack/aws/lambda/
[EC2]: /development/stack/aws/ec2/
