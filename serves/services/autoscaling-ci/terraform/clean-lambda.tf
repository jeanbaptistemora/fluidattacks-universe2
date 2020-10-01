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

  tags = {
    "Name"               = "autoscaling-clean"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_role_policy_attachment" "autoscaling-clean" {
  role       = aws_iam_role.autoscaling-clean.name
  policy_arn = aws_iam_policy.autoscaling-clean.arn
}

data "archive_file" "autoscaling-clean" {
  type        = "zip"
  source_file = "index.js"
  output_path = "autoscaling-clean.zip"
}

resource "aws_lambda_function" "autoscaling-clean" {
  filename      = "autoscaling-clean.zip"
  function_name = "autoscaling-clean"
  role          = aws_iam_role.autoscaling-clean.arn
  handler       = "index.handler"
  publish       = true
  timeout       = 60

  source_code_hash = data.archive_file.autoscaling-clean.output_base64sha256

  runtime = "nodejs12.x"

  tags = {
    "Name"               = "autoscaling-clean"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}
