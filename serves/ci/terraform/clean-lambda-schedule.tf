resource "aws_cloudwatch_event_rule" "every-hour" {
  name                = "every--hour"
  description         = "Fires every one hours"
  schedule_expression = "rate(1 hour)"

  tags = {
    "Name"               = "every--hour"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_cloudwatch_event_target" "autoscaling-clean" {
  rule      = aws_cloudwatch_event_rule.every-hour.name
  target_id = "lambda"
  arn       = aws_lambda_function.autoscaling-clean.arn

  input = <<EOF
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
