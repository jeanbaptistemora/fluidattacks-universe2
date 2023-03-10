# CloudWatch rule that will listen for every state change in Batch jobs
resource "aws_cloudwatch_event_rule" "compute_jobs" {
  name = "monitoring-compute-jobs"

  event_pattern = jsonencode({
    source      = ["aws.batch"]
    detail-type = ["Batch Job State Change"]
  })

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_kinesis_stream" "compute_jobs" {
  name             = "monitoring-compute-jobs"
  retention_period = 24

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Sends all the events to be processed by Kinesis
resource "aws_cloudwatch_event_target" "compute_jobs" {
  rule     = aws_cloudwatch_event_rule.compute_jobs.name
  arn      = aws_kinesis_stream.compute_jobs.arn
  role_arn = aws_iam_role.kinesis_stream.arn

  kinesis_target {
    partition_key_path = "$.id"
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Lambda function that ensures theres a newline separation
# between every record so Athena parses the information correctly
data "archive_file" "lambda_package" {
  type             = "zip"
  source_file      = "src/newline.py"
  output_file_mode = "0666"
  output_path      = "newline.zip"
}

resource "aws_lambda_function" "firehose_transform" {
  function_name    = "FirehoseMultilineJSON"
  role             = aws_iam_role.lambda_role.arn
  description      = "Converts multiline JSON records to one event per line"
  runtime          = "python3.9"
  filename         = data.archive_file.lambda_package.output_path
  handler          = "newline.lambda_handler"
  source_code_hash = data.archive_file.lambda_package.output_base64sha256
  timeout          = 60

  tags = {
    "Name"               = "common-firehose-lambda"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_kinesis_firehose_delivery_stream" "compute_jobs" {
  name        = "common-monitoring-compute-jobs"
  destination = "extended_s3"

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.compute_jobs.arn
    role_arn           = aws_iam_role.firehose_delivery.arn
  }

  extended_s3_configuration {
    role_arn           = aws_iam_role.firehose_delivery.arn
    bucket_arn         = aws_s3_bucket.monitoring.arn
    buffer_size        = 1
    buffer_interval    = 60
    compression_format = "UNCOMPRESSED"
    prefix             = "compute-jobs/"

    processing_configuration {
      enabled = true

      processors {
        type = "Lambda"

        parameters {
          parameter_name  = "LambdaArn"
          parameter_value = aws_lambda_function.firehose_transform.arn
        }

        parameters {
          parameter_name  = "BufferSizeInMBs"
          parameter_value = 1
        }
      }
    }

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.monitoring.name
      log_stream_name = aws_cloudwatch_log_stream.compute_jobs.name
    }
  }
}
