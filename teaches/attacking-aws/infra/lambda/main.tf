resource "aws_lambda_function" "secure-function" {
  filename      = "lambda/secure_function.zip"
  function_name = "secure-function"
  role          = aws_iam_role.secure-function-role.arn 
  handler       = "secure_function.lambda_handler"
  publish       = true
  timeout       = 60

  runtime = "python3.8"
}

