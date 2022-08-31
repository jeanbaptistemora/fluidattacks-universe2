resource "aws_cloudwatch_log_group" "fluid" {
  name = "FLUID"

  tags = {
    "Name"               = "FLUID"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }
}

data "aws_iam_policy_document" "opensearch-log-policy" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:PutLogEventsBatch",
    ]

    resources = ["arn:aws:logs:us-east-1:${data.aws_caller_identity.current.account_id}:log-group:FLUID*", ]

    principals {
      identifiers = ["es.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_cloudwatch_log_resource_policy" "opensearch-log-policy" {
  policy_document = data.aws_iam_policy_document.opensearch-log-policy.json
  policy_name     = "opensearch-log-policy"
}
