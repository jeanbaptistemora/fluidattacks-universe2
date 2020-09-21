data "aws_iam_policy_document" "web-ephemeral-lambda-subfolder-to-index" {
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

resource "aws_iam_policy" "web-ephemeral-lambda-subfolder-to-index" {
  name        = "web-ephemeral-lambda-subfolder-to-index"
  description = "Allows communication with cloudfront"
  policy      = data.aws_iam_policy_document.web-ephemeral-lambda-subfolder-to-index.json
}

resource "aws_iam_role_policy_attachment" "web-ephemeral-lambda-subfolder-to-index-attach" {
  role       = aws_iam_role.web-ephemeral-lambda.name
  policy_arn = aws_iam_policy.web-ephemeral-lambda-subfolder-to-index.arn
}

data "archive_file" "web-ephemeral-subfolder-to-index-zip" {
  type        = "zip"
  source_file = "index.js"
  output_path = "subfolder-to-index.zip"
}

resource "aws_lambda_function" "web-ephemeral-subfolder-to-index" {
  filename      = "subfolder-to-index.zip"
  function_name = "web-ephemeral-subfolder-to-index"
  role          = aws_iam_role.web-ephemeral-lambda.arn
  handler       = "index.handler"
  publish       = true
  timeout       = 3

  source_code_hash = data.archive_file.web-ephemeral-subfolder-to-index-zip.output_base64sha256

  runtime = "nodejs12.x"
}
