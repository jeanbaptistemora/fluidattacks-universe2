---
id: cost-management
title: Cost Management
sidebar_label: Cost Management
slug: /development/stack/aws/cost-management
---

## Rationale

We use [Cost Management][COST-MANAGEMENT]
for controlling and optimizing our costs
within [AWS][AWS].
The main reasons why we chose it
over other alternatives
are the following:

- It is a core AWS service.
  Once we start creating infrastructure,
  Cost Management begins to generate costs reports.
- It integrates seamlessly with all AWS services,
  providing fully accurate and granular reporting.
- It provides us with
  [highly customizable](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-chart.html)
  charts that allow us
  to [group costs](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-table.html)
  based on [attributes](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-filtering.html)
  such as service, region, tag, linked account,
  among many others.
  In addition,
  it allows us to combine attributes.
- The charts [support multiple time ranges](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-modify.html#ce-timerange)
  that go from hourly to monthly granularity.
- The charts [support multiple styles](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-modify.html#ce-style)
  for readability.
- All the data used for generating charts
  [can be exported](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-table.html)
  for external use.
- It supports
  [cost forecasting](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-forecast.html),
  allowing us to make predictions
  regarding future costs
  based on consumption
  during a specified time span.
- It supports [report generation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-default-reports.html#ce-cost-usage-reports),
  which allows us to create
  and save customized charts
  such as "Monthly costs by linked account."
- It supports [cost allocation tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html),
  allowing us to group costs
  based on tags assigned to resources.

## Alternatives

- **[GCP Cost Management](https://cloud.google.com/cost-management):**
  It is directly tied to [GCP](https://cloud.google.com/gcp),
  so we would have to migrate to use it.
- **[Azure Cloud Cost Management](https://azure.microsoft.com/en-us/services/cost-management/):**
  It is directly tied to [Azure](https://azure.microsoft.com/en-us/),
  so we would have to migrate to use it.

## Usage

We use [Cost Management][COST-MANAGEMENT] for

- monitoring our [AWS][AWS] consumption constantly and
- grouping costs [based on product tags](https://gitlab.com/fluidattacks/product/-/blob/fca78e4277e2cb9f71a5e8de45f67219c64ccf63/.tflint.hcl#L6).

We do not use Cost Management for

- managing costs using [budgets](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/budgets-managing-costs.html)
  (our third-party provider for AWS does this for us) or
- monitoring costs using [Cost Anomaly Detection](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/manage-ad.html)
  (pending review).

## Guidelines

You can access the [Cost Management][COST-MANAGEMENT] console
after [authenticating to AWS](/development/stack/aws#guidelines).

[AWS]: /development/stack/aws/
[COST-MANAGEMENT]: https://aws.amazon.com/aws-cost-management/
