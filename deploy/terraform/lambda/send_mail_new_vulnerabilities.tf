resource "aws_lambda_function" "send_mail_new_vulnerabilities" {
  filename      = "../../lambda/packages/send_mail_new_vulnerabilities.zip"
  function_name = "send_mail_new_vulnerabilities"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_send_mail_new_vulnerabilities.send_mail_new_vulnerabilities"
  publish       = true

  runtime = "python3.7"
}
