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

resource "aws_s3_object" "monitoring_jobs_json_paths" {
  bucket = aws_s3_bucket.monitoring.id
  key    = "jobs/jsonpaths.json"
  content = jsonencode({
    "jsonpaths" : [
      "$.detail.jobId",
    ]
  })
}
