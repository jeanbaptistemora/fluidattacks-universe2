data "aws_iam_policy_document" "autoscaling-clean" {
  # EC2
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "ec2:DescribeInstances",
      "ec2:TerminateInstances",
    ]
    resources = [
      "*",
    ]
  }

  # Logs
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = [
      "*",
    ]
  }
}

resource "aws_iam_policy" "autoscaling-clean" {
  description = "Policy for lambda that cleans autoscaling orphaned machines"
  name        = "autoscaling-clean"
  path        = "/"
  policy      = data.aws_iam_policy_document.autoscaling-clean.json
}

resource "aws_iam_role" "autoscaling-clean" {
  name = "autoscaling-clean"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json
}

resource "aws_iam_role_policy_attachment" "policy-clean-role" {
  role       = aws_iam_role.autoscaling-clean.name
  policy_arn = aws_iam_policy.autoscaling-clean.arn
}

data "archive_file" "archive-clean-role" {
  type        = "zip"
  source_file = "index.js"
  output_path = "clean-role.zip"
}

resource "aws_lambda_function" "lambda-clean-role" {
  filename      = "clean-role.zip"
  function_name = "autoscaling-clean-lambda"
  role          = aws_iam_role.autoscaling-clean.arn
  handler       = "index.handler"
  publish       = true
  timeout       = 10

  source_code_hash = data.archive_file.archive-clean-role.output_base64sha256

  runtime = "nodejs12.x"
}
