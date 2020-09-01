data "aws_iam_policy_document" "lambda-execution-policy-document" {

  statement {
    sid = "LambdaExecutionPolicy"
    effect = "Allow"
    actions = [
      "iam:*User*"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "lambda_execution_policy" {
  name        = "lambda_execution_policy"
  path        = "/"
  description = "Policy to allow the execute of Secure App"

  policy = data.aws_iam_policy_document.lambda-execution-policy-document.json
}


output "lambda_execution_policy" {
  value = aws_iam_policy.lambda_execution_policy.arn
}
