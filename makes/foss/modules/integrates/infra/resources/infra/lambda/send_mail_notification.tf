variable "sqs_id" {}
variable "aws_lambda_send_mail_notification_zip" {}

resource "aws_lambda_function" "integrates-send-mail-notification" {
  filename      = var.aws_lambda_send_mail_notification_zip
  function_name = "integrates-send-mail-notification"
  role          = aws_iam_role.integrates-lambdas.arn
  handler       = "lambda_send_mail_notification.send_mail_notification"
  publish       = true
  timeout       = 60

  runtime = "python3.7"

  tags = {
    "Name"               = "integrates-send-mail-notification"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_lambda_event_source_mapping" "integrates-event-source-mapping" {
  batch_size       = 10
  event_source_arn = var.sqs_id
  enabled          = true
  function_name    = aws_lambda_function.integrates-send-mail-notification.arn
}
