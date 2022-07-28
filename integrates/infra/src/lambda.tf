variable "aws_opensearch_host" {}
variable "lambda_path" {}

data "aws_iam_policy_document" "lambda" {
  statement {
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "integrates_dynamodb_replication_lambda_role" {
  name = "integrates_dynamodb_replication_lambda_role"

  assume_role_policy = data.aws_iam_policy_document.lambda.json

  tags = {
    "Name"               = "integrates-lambda"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "null_resource" "dynamodb_replication_dependencies" {
  provisioner "local-exec" {
    command = <<EOT
      pip install \
        --no-compile \
        --requirement ${var.lambda_path}/dynamodb_replication/requirements.txt \
        --target ${var.lambda_path}/dynamodb_replication
    EOT
  }

  triggers = {
    dependencies = filemd5("${var.lambda_path}/dynamodb_replication/requirements.txt")
  }
}

data "archive_file" "dynamodb_replication_zip" {
  depends_on  = [null_resource.dynamodb_replication_dependencies]
  output_path = "${var.lambda_path}/dynamodb_replication.zip"
  source_dir  = "${var.lambda_path}/dynamodb_replication"
  type        = "zip"
}

resource "aws_lambda_function" "dynamodb_replication" {
  depends_on       = [data.archive_file.dynamodb_replication_zip]
  filename         = data.archive_file.dynamodb_replication_zip.output_path
  function_name    = "integrates-dynamodb-replication-lambda"
  handler          = "handler.handle"
  role             = aws_iam_role.integrates_dynamodb_replication_lambda_role.arn
  runtime          = "python3.9"
  source_code_hash = filebase64sha256(data.archive_file.dynamodb_replication_zip.output_path)

  environment {
    variables = {
      AWS_OPENSEARCH_HOST = var.aws_opensearch_host
    }
  }

  tags = {
    "Name"               = "integrates-lambda"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
