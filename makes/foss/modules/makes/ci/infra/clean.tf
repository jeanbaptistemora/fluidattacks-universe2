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

data "aws_iam_policy_document" "lambda-assume-role-policy" {
  statement {
    sid    = "LambdaAssumeRolePolicy"
    effect = "Allow"

    principals {
      type = "Service"
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

data "archive_file" "autoscaling-clean" {
  type        = "zip"
  source_file = "index.js"
  output_path = "autoscaling-clean.zip"
}

resource "aws_iam_policy" "autoscaling-clean" {
  description = "Policy for lambda that cleans autoscaling orphaned machines"
  name        = "autoscaling-clean"
  path        = "/"
  policy      = data.aws_iam_policy_document.autoscaling-clean.json
}

resource "aws_iam_role" "autoscaling-clean" {
  name               = "autoscaling-clean"
  assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json

  tags = {
    "Name"            = "autoscaling-clean"
    "management:area" = "innovation"
    "management:type" = "product"
  }
}

resource "aws_iam_role_policy_attachment" "autoscaling-clean" {
  role       = aws_iam_role.autoscaling-clean.name
  policy_arn = aws_iam_policy.autoscaling-clean.arn
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
    "Name"            = "autoscaling-clean"
    "management:area" = "innovation"
    "management:type" = "product"
  }
}

resource "aws_cloudwatch_event_rule" "every-hour" {
  name                = "every--hour"
  description         = "Fires every one hours"
  schedule_expression = "rate(1 hour)"

  tags = {
    "Name"            = "every--hour"
    "management:area" = "innovation"
    "management:type" = "product"
  }
}

resource "aws_cloudwatch_event_target" "autoscaling-clean" {
  rule      = aws_cloudwatch_event_rule.every-hour.name
  target_id = "lambda"
  arn       = aws_lambda_function.autoscaling-clean.arn

  input = <<-EOF
    {
      "region": [
        "us-east-1"
      ]
    }
  EOF
}

resource "aws_lambda_permission" "autoscaling-clean-every-hour" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.autoscaling-clean.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every-hour.arn
}

resource "aws_cloudwatch_log_group" "autoscaling-clean" {
  name = "/aws/lambda/autoscaling-clean"

  tags = {
    "Name"            = "autoscaling-clean"
    "management:area" = "innovation"
    "management:type" = "product"
  }
}
