resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "test_lambda" {
  function_name = "lambda_function"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "index.test"

  tracing_config {
    mode = "Active"
  }
  # ... other configuration ...
}

resource "aws_lambda_function" "test_lambda_insecure_trace" {
  function_name = "lambda_function_insecure"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "index.test"

  tracing_config {
    mode = "PassThrough"
  }
  # ... other configuration ...
}

resource "aws_lambda_function" "test_lambda_missing_trace" {
  function_name = "lambda_function_missing"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "index.test"

  ephemeral_storage {
    size = 10240 # Min 512 MB and the Max 10240 MB
  }
  # ... other configuration ...
}
