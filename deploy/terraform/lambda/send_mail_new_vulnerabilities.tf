variable "sqs_id" {}

resource "aws_lambda_function" "integrates-send-mail-new-vulnerabilities" {
  filename      = "../../lambda/packages/send_mail_new_vulnerabilities.zip"
  function_name = "integrates-send-mail-new-vulnerabilities"
  role          = aws_iam_role.integrates-lambdas.arn
  handler       = "lambda_send_mail_new_vulnerabilities.send_mail_new_vulnerabilities"
  publish       = true

  runtime = "python3.7"
}

resource "aws_lambda_event_source_mapping" "integrates-event-source-mapping" {
  batch_size        = 1
  event_source_arn  = var.sqs_id
  enabled           = true
  function_name     = aws_lambda_function.integrates-send-mail-new-vulnerabilities.arn
}
