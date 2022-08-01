variable "aws_opensearch_host" {}
variable "lambda_path" {}

data "aws_iam_policy_document" "integrates_dynamodb_replication_lambda_policy" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]
    effect = "Allow"
    sid    = "lambdaAccess"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }

  statement {
    actions = [
      "dynamodb:ListStreams",
    ]
    effect    = "Allow"
    resources = ["*"]
    sid       = "lambdaDynamodbGlobalAccess"
  }

  statement {
    actions = [
      "dynamodb:DescribeStream",
      "dynamodb:GetRecords",
      "dynamodb:GetShardIterator",
    ]
    effect = "Allow"
    resources = [
      "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/*/stream/*"
    ]
    sid = "lambdaDynamodbStreamAccess"
  }
}

resource "aws_iam_role" "integrates_dynamodb_replication_lambda_role" {
  name = "integrates_dynamodb_replication_lambda_role"

  assume_role_policy = data.aws_iam_policy_document.integrates_dynamodb_replication_lambda_policy.json

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
}

data "archive_file" "dynamodb_replication_zip" {
  output_path = "${var.lambda_path}/dynamodb_replication.zip"
  source_dir  = "${var.lambda_path}/dynamodb_replication"
  type        = "zip"
}

resource "aws_lambda_function" "dynamodb_replication" {
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

resource "aws_lambda_event_source_mapping" "dynamodb_replication" {
  event_source_arn  = aws_dynamodb_table.integrates_vms.stream_arn
  function_name     = aws_lambda_function.dynamodb_replication.arn
  starting_position = "LATEST"

  filter_criteria {
    filter {
      pattern = jsonencode({
        dynamodb = {
          "Keys" : {
            "pk" : [{ "prefix" : "VULN#" }],
            "sk" : [{ "prefix" : "FIN#" }]
          }
        }
      })
    }
  }
}
