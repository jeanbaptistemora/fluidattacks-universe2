data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    sid    = "LambdaAssumeRolePolicy"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = [
        "lambda.amazonaws.com",
        "edgelambda.amazonaws.com",
      ]
    }

    actions = [
      "sts:AssumeRole",
    ]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "web-production-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json

  tags = {
    "Name"               = "web-production-lambda"
    "management:type"    = "production"
    "management:product" = "airs"
  }
}
