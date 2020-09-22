data "aws_iam_policy_document" "lambda-assume-role-policy" {
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

resource "aws_iam_role" "web-ephemeral-lambda" {
  name               = "web-ephemeral-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json
}
