resource "aws_secretsmanager_secret" "rotation-example" {
  name                = "rotation-example"
  rotation_lambda_arn = aws_lambda_function.example.arn
  rotation_rules {
    automatically_after_days = 7
  }
}
