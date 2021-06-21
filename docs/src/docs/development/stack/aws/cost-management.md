---
id: cost-management
title: Cost Management
sidebar_label: Cost Management
slug: /development/stack/aws/cost-management
---

## Rationale

We use [Cost Management][COST-MANAGEMENT]
for controlling and optimizing our
costs within [AWS][AWS].

The main reasons why we chose it
over other alternatives are:

1. It is a core [AWS][AWS] service.
    Once one starts creating infrastructure,
    [Cost Management][COST-MANAGEMENT]
    begins to generate costs
    reports.
1. It seamlessly integrates with
    all [AWS][AWS] services.
    giving fully accurate and granular reports.
1. It provides
    [highly customizable](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-chart.html)
    charts that allow us to
    [group costs](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-table.html)
    based on
    [attributes](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-filtering.html)
    like service, region, tags, linked account, among many others.
    Combining attributes is also possible.
1. Charts
    [support multiple time ranges](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-modify.html#ce-timerange)
    that go from hourly to monthly granularity.
1. Charts
    [support multiple styles](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-modify.html#ce-style)
    for readability.
1. All the data used for generating charts
    [can be exported](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-table.html)
    for external use.
1. It supports
    [costs forecasting](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-forecast.html),
    allowing us to make predictions
    regarding future costs
    based on consumption
    during a specified timespan.
1. It supports
    [report generation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-default-reports.html#ce-cost-usage-reports),
    which allow us to
    create and save custom charts like
    *Monthly costs by linked account*.
1. It supports
    [cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html),
    allowing us to group costs based on
    tags assigned to resources.

## Alternatives

1. [GCP Cost Management](https://cloud.google.com/cost-management):
    It is directly tied to [GCP](https://cloud.google.com/gcp),
    meaning that in order to use it we would have to migrate.
1. [Azure Cloud Cost Management](https://azure.microsoft.com/en-us/services/cost-management/):
    It is directly tied to [Azure](https://azure.microsoft.com/en-us/),
    meaning that in order to use it we would have to migrate.

## Usage

We use [Cost Management][COST-MANAGEMENT] for:

1. Constantly monitoring our [AWS][AWS] consumption.
1. Grouping costs
    [based on product tags](https://gitlab.com/fluidattacks/product/-/blob/fca78e4277e2cb9f71a5e8de45f67219c64ccf63/.tflint.hcl#L6).

We do not use [Cost Management][COST-MANAGEMENT] for:

1. Managing costs using
    [budgets](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/budgets-managing-costs.html).
    Our third party provider for [AWS][AWS]
    does this for us.
1. Monitoring costs using [Cost Anomaly](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-ad.html).
    Pending to review.

## Guidelines

You can access the
[Cost Management][COST-MANAGEMENT] console
after [authenticating on AWS](/development/stack/aws#guidelines).

[AWS]: https://aws.amazon.com/
[COST-MANAGEMENT]: https://aws.amazon.com/aws-cost-management/
