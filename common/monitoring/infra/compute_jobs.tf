resource "aws_cloudwatch_log_stream" "compute_jobs" {
  name           = "compute-jobs"
  log_group_name = aws_cloudwatch_log_group.monitoring.name

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

data "aws_iam_policy_document" "lambda_sts_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "archive_file" "lambda_package" {
  type             = "zip"
  source_file      = "src/newline.py"
  output_file_mode = "0666"
  output_path      = "newline.zip"
}

resource "aws_iam_role" "lambda_role" {
  name               = "firehose_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_sts_role.json
}

resource "aws_lambda_function" "firehose_transform" {
  function_name    = "FirehoseMultilineJSON"
  role             = aws_iam_role.lambda_role.arn
  description      = "Converts multiline JSON records to one event per line"
  runtime          = "python3.9"
  filename         = data.archive_file.lambda_package.output_path
  handler          = "newline.lambda_handler"
  source_code_hash = filebase64sha256(data.archive_file.lambda_package.output_path)
  timeout          = 60

  tags = {
    "Name"               = "common-firehose-lambda"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
    "Access"             = "private"
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
      }
    }

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.monitoring.name
      log_stream_name = aws_cloudwatch_log_stream.compute_jobs.name
    }
  }
}

resource "aws_glue_catalog_table" "compute_jobs" {
  database_name = aws_athena_database.monitoring.name
  name          = "compute_jobs"

  table_type = "EXTERNAL_TABLE"

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.monitoring.bucket}/compute-jobs"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat"

    ser_de_info {
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
      parameters = {
        "serialization.format" = 1
      }
    }

    sort_columns {
      column     = "time"
      sort_order = 0
    }

    columns {
      name = "detail"
      type = replace(
        <<-EOF
          struct<
            container:struct<
              command:array<string>,
              environment:array<struct<name:string>>,
              exitCode:bigint,
              image:string,
              logStreamName:string,
              memory:bigint,
              resourceRequirements:array<struct<type:string, value:string>>,
              vcpus:bigint
            >,
            createdAt:timestamp,
            jobId:string,
            jobName:string,
            jobQueue:string,
            startedAt:timestamp,
            status:string,
            statusReason:string,
            stoppedAt:timestamp
          >
        EOF
        ,
      "/[\n ]+/", "")
    }

    columns {
      name = "id"
      type = "string"
    }

    columns {
      name = "time"
      type = "timestamp"
    }
  }
}
