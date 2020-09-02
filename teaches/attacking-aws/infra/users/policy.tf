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


data "aws_iam_policy_document" "lambda-user-policy-document" {
  statement {
    sid = "LambdaUserPolicy"
    effect = "Allow"
    actions = [
      "iam:PassRole",
      "lambda:CreateFunction",
      "lambda:UpdateFunctionCode",
      "lambda:InvokeFunction"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "lambda_user_policy" {
  name        = "lambda_user_policy"
  path        = "/"
  description = "Policy to allow creating, updating and invoking lambdas"

  policy = data.aws_iam_policy_document.lambda-user-policy-document.json
}


output "lambda_execution_policy" {
  value = aws_iam_policy.lambda_execution_policy.arn
}
