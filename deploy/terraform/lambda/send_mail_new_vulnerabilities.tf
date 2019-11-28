resource "aws_lambda_function" "integrates-send-mail-new-vulnerabilities" {
  filename      = "../../lambda/packages/send_mail_new_vulnerabilities.zip"
  function_name = "integrates-send-mail-new-vulnerabilities"
  role          = aws_iam_role.integrates-lambdas.arn
  handler       = "lambda_send_mail_new_vulnerabilities.send_mail_new_vulnerabilities"
  publish       = true

  runtime = "python3.7"
}
