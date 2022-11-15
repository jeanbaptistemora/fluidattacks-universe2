# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_cloudwatch_log_stream" "compute_jobs" {
  name           = "compute-jobs"
  log_group_name = aws_cloudwatch_log_group.monitoring.name
}

resource "aws_kinesis_stream" "compute_jobs" {
  name             = "monitoring-compute-jobs"
  retention_period = 24

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }
}

resource "aws_cloudwatch_event_rule" "compute_jobs" {
  name = "monitoring-compute-jobs"

  event_pattern = jsonencode({
    source      = ["aws.batch"]
    detail-type = ["Batch Job State Change"]
  })
}

resource "aws_cloudwatch_event_target" "compute_jobs" {
  rule     = aws_cloudwatch_event_rule.compute_jobs.name
  arn      = aws_kinesis_stream.compute_jobs.arn
  role_arn = aws_iam_role.kinesis_stream.arn

  kinesis_target {
    partition_key_path = "$.detail.jobId"
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
