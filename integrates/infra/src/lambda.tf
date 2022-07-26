
data "aws_iam_policy_document" "lambda" {
  statement {
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "integrates_dynamodb_replication_lambda_role" {
  name = "integrates_dynamodb_replication_lambda_role"

  assume_role_policy = data.aws_iam_policy_document.lambda.json

  tags = {
    "Name"               = "integrates-opensearch"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
