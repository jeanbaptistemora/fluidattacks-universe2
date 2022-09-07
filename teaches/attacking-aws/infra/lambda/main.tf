# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_lambda_function" "secure-function" {
  filename      = "lambda/secure_function.zip"
  function_name = "secure-function"
  role          = aws_iam_role.secure-function-role.arn
  handler       = "secure_function.lambda_handler"
  publish       = true
  timeout       = 60

  runtime = "python3.8"
}
