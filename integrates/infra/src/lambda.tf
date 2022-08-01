variable "aws_opensearch_host" {}
variable "lambda_path" {}

resource "aws_security_group" "integrates-lambda" {
  name   = "integrates-opensearch"
  vpc_id = data.aws_vpc.main.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.main.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.main.cidr_block]
  }

  tags = {
    "Name"               = "integrates-lambda"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

data "aws_iam_policy_document" "integrates_lambda_policy" {
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
}

data "aws_iam_policy_document" "integrates_dynamodb_replication_lambda_policy" {
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

  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:*"
    ]
    sid = "lambdaCloudwatchAccess"
  }
}

resource "aws_iam_policy" "integrates_dynamodb_replication_lambda_policy" {
  description = "Policy for dynamodb replication"
  name        = "integrates_dynamodb_replication_lambda_policy"
  path        = "/"
  policy      = data.aws_iam_policy_document.integrates_dynamodb_replication_lambda_policy.json
}

resource "aws_iam_role" "integrates_dynamodb_replication_lambda_role" {
  assume_role_policy = data.aws_iam_policy_document.integrates_lambda_policy.json
  name               = "integrates_dynamodb_replication_lambda_role"

  tags = {
    "Name"               = "integrates-lambda"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_iam_role_policy_attachment" "integrates_dynamodb_replication_lambda_role" {
  role       = aws_iam_role.integrates_dynamodb_replication_lambda_role.name
  policy_arn = aws_iam_policy.integrates_dynamodb_replication_lambda_policy.arn
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
    always_run = timestamp()
  }
}

data "archive_file" "dynamodb_replication_zip" {
  depends_on       = [null_resource.dynamodb_replication_dependencies]
  output_file_mode = "0666"
  output_path      = "${var.lambda_path}/dynamodb_replication.zip"
  source_dir       = "${var.lambda_path}/dynamodb_replication"
  type             = "zip"
}

resource "aws_lambda_function" "dynamodb_replication" {
  depends_on       = [data.archive_file.dynamodb_replication_zip]
  filename         = data.archive_file.dynamodb_replication_zip.output_path
  function_name    = "integrates-dynamodb-replication-lambda"
  handler          = "handler.handle"
  role             = aws_iam_role.integrates_dynamodb_replication_lambda_role.arn
  runtime          = "python3.9"
  source_code_hash = data.archive_file.dynamodb_replication_zip.output_base64sha256
  timeout          = 60

  environment {
    variables = {
      AWS_OPENSEARCH_HOST = var.aws_opensearch_host
    }
  }

  vpc_config {
    security_group_ids = [
      aws_security_group.integrates-lambda.id,
    ]

    subnet_ids = [
      for subnet in data.aws_subnet.main : subnet.id
    ]
  }

  tags = {
    "Name"               = "integrates-lambda"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_lambda_event_source_mapping" "dynamodb_replication" {
  batch_size        = 100
  event_source_arn  = aws_dynamodb_table.integrates_vms.stream_arn
  function_name     = aws_lambda_function.dynamodb_replication.arn
  starting_position = "LATEST"

  filter_criteria {
    filter {
      pattern = jsonencode({
        dynamodb = {
          "Keys" : {
            "pk" : { "S" : [{ "prefix" : "VULN#" }] },
            "sk" : { "S" : [{ "prefix" : "FIN#" }] },
          }
        }
      })
    }
  }
}
