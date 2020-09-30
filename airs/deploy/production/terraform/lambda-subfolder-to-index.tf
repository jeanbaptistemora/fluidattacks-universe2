data "aws_iam_policy_document" "subfolder_to_index" {
  statement {
    sid    = "LogsAccess"
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = [
      "arn:aws:logs:*:*:*"
    ]
  }
}

resource "aws_iam_policy" "subfolder_to_index" {
  name        = "web-production-lambda-subfolder-to-index"
  description = "Allows communication with cloudfront"
  policy      = data.aws_iam_policy_document.subfolder_to_index.json
}

resource "aws_iam_role_policy_attachment" "subfolder_to_index" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.subfolder_to_index.arn
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "index.js"
  output_path = "subfolder-to-index.zip"
}

resource "aws_lambda_function" "subfolder_to_index" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "web-production-subfolder-to-index"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  publish       = true
  timeout       = 3

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  runtime = "nodejs12.x"

  tags = {
    "management:type"    = "production"
    "management:product" = "airs"
  }
}
