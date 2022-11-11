# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_kinesis_stream" "monitoring_jobs" {
  name             = "common_compute_monitoring_jobs"
  retention_period = 48

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }
}

resource "aws_iam_role" "kinesis_stream_monitoring_jobs" {
  name = "common-compute-kinesis"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "events.amazonaws.com"
        },
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "kinesis_stream_monitoring_jobs" {
  role       = aws_iam_role.kinesis_stream_monitoring_jobs.name
  policy_arn = aws_iam_policy.kinesis_stream_monitoring_jobs.arn
}

resource "aws_iam_policy" "kinesis_stream_monitoring_jobs" {
  name = "common-compute-kinesis-stream-monitoring-jobs"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "kinesis:PutRecord",
          "kinesis:PutRecords",
        ],
        "Resource" : [
          aws_kinesis_stream.monitoring_jobs.arn
        ],
      },
    ]
  })
}

resource "aws_cloudwatch_event_rule" "monitoring_jobs" {
  name = "common-compute-monitoring-jobs"

  event_pattern = jsonencode({
    source      = ["aws.batch"]
    detail-type = ["Batch Job State Change"]
  })
}

resource "aws_cloudwatch_event_target" "monitoring_jobs" {
  rule     = aws_cloudwatch_event_rule.monitoring_jobs.name
  arn      = aws_kinesis_stream.monitoring_jobs.arn
  role_arn = aws_iam_role.kinesis_stream_monitoring_jobs.arn

  kinesis_target {
    partition_key_path = "$.detail.jobId"
  }
}

resource "aws_s3_bucket" "monitoring" {
  bucket = "common-compute-monitoring"
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.monitoring.id
  acl    = "private"
}

resource "aws_cloudwatch_log_group" "monitoring" {
  name = "common-compute-monitoring"
}

resource "aws_cloudwatch_log_stream" "monitoring_jobs" {
  name           = "jobs"
  log_group_name = aws_cloudwatch_log_group.monitoring.name
}

resource "aws_iam_role" "firehose_delivery" {
  name = "common-compute-firehose-delivery"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "firehose.amazonaws.com"
        },
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "firehose_delivery" {
  role       = aws_iam_role.firehose_delivery.name
  policy_arn = aws_iam_policy.firehose_delivery.arn
}

resource "aws_iam_policy" "firehose_delivery" {
  name = "common-compute-firehose-delivery"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:PutLogEvents"
        ],
        "Resource" : [
          aws_cloudwatch_log_stream.monitoring_jobs.arn,
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "kinesis:DescribeStream",
          "kinesis:GetShardIterator",
          "kinesis:GetRecords",
          "kinesis:ListShards"
        ],
        "Resource" : [
          aws_kinesis_stream.monitoring_jobs.arn
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:AbortMultipartUpload",
          "s3:GetBucketLocation",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:ListBucketMultipartUploads",
          "s3:PutObject"
        ],
        "Resource" : [
          "${aws_s3_bucket.monitoring.arn}",
          "${aws_s3_bucket.monitoring.arn}/*",
        ],
      },
    ]
  })
}

resource "aws_s3_object" "monitoring_jobs_json_paths" {
  bucket = aws_s3_bucket.monitoring.id
  key    = "jobs/jsonpaths.json"
  content = jsonencode({
    "jsonpaths" : [
      "$.detail.jobId",
    ]
  })
}

resource "aws_redshiftdata_statement" "monitoring_jobs_table" {
  cluster_identifier = data.aws_redshift_cluster.observes.cluster_identifier
  database           = data.aws_redshift_cluster.observes.database_name
  db_user            = data.aws_redshift_cluster.observes.master_username
  sql                = <<-EOF
    CREATE SCHEMA IF NOT EXISTS common_compute;
    CREATE TABLE IF NOT EXISTS common_compute.jobs (jobId text PRIMARY KEY);
  EOF
}

resource "aws_kinesis_firehose_delivery_stream" "monitoring_jobs" {
  name        = "common-compute-monitoring-jobs"
  destination = "redshift"

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.monitoring_jobs.arn
    role_arn           = aws_iam_role.firehose_delivery.arn
  }

  s3_configuration {
    role_arn           = aws_iam_role.firehose_delivery.arn
    bucket_arn         = aws_s3_bucket.monitoring.arn
    buffer_size        = 1
    buffer_interval    = 60
    compression_format = "UNCOMPRESSED"
    prefix             = "jobs"

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.monitoring.name
      log_stream_name = aws_cloudwatch_log_stream.monitoring_jobs.name
    }
  }

  redshift_configuration {
    role_arn        = aws_iam_role.firehose_delivery.arn
    cluster_jdbcurl = "jdbc:redshift://${data.aws_redshift_cluster.observes.endpoint}:${data.aws_redshift_cluster.observes.port}/${data.aws_redshift_cluster.observes.database_name}"
    username        = var.redshiftUser
    password        = var.redshiftPassword
    data_table_name = "common_compute.jobs"
    copy_options    = "json 's3://${aws_s3_object.monitoring_jobs_json_paths.bucket}/${aws_s3_object.monitoring_jobs_json_paths.id}' region 'us-east-1'"

    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.monitoring.name
      log_stream_name = aws_cloudwatch_log_stream.monitoring_jobs.name
    }
  }
}
