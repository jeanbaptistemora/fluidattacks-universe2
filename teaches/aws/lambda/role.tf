variable "lambda_execution_policy" {}

resource "aws_iam_role" "secure-function-role" {
  name = "secure-function-role"

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

resource "aws_iam_role_policy_attachment" "lambda_execution_attach" {
  policy_arn = var.lambda_execution_policy
  role       = aws_iam_role.secure-function-role.name
}
