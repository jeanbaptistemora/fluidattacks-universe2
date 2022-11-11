# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_kinesis_stream" "common_compute_monitoring_jobs" {
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

data "aws_iam_policy_document" "common_compute_kinesis" {
  statement {
    actions = [
      "kinesis:Describe*",
      "kinesis:Get*",
      "kinesis:PutRecord",
      "kinesis:PutRecords",
    ]

    resources = [
      aws_kinesis_stream.common_compute_monitoring_jobs.arn
    ]
  }
}

resource "aws_iam_policy" "common_compute_kinesis" {
  name = "common_compute_kinesis"

  policy = data.aws_iam_policy_document.common_compute_kinesis.json
}

data "aws_iam_policy_document" "common_compute_assume_kinesis" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = [
        "events.amazonaws.com",
        "firehose.amazonaws.com",
      ]
    }
  }
}

resource "aws_iam_role" "common_compute_kinesis" {
  name = "common-compute-kinesis"

  assume_role_policy = data.aws_iam_policy_document.common_compute_assume_kinesis.json
}

resource "aws_iam_role_policy_attachment" "common_compute_kinesis" {
  role       = aws_iam_role.common_compute_kinesis.name
  policy_arn = aws_iam_policy.common_compute_kinesis.arn
}

resource "aws_cloudwatch_event_rule" "common_compute_monitoring_jobs" {
  name = "common_compute_monitoring_jobs"

  event_pattern = jsonencode({
    source      = ["aws.batch"]
    detail-type = ["Batch Job State Change"]
  })

  tags = {
    "Name"               = "common_compute_monitoring_jobs"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_target" "common_compute_monitoring_jobs" {
  rule     = aws_cloudwatch_event_rule.common_compute_monitoring_jobs.name
  arn      = aws_kinesis_stream.common_compute_monitoring_jobs.arn
  role_arn = aws_iam_role.common_compute_kinesis.arn

  kinesis_target {
    partition_key_path = "$.detail.jobId"
  }
}

resource "aws_s3_bucket" "common_compute_monitoring" {
  bucket = "common-compute-monitoring"
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.common_compute_monitoring.id
  acl    = "private"
}

resource "aws_iam_role" "assume_firehose" {
  name = "assume_firehose"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "firehose.amazonaws.com"
        },
        "Effect" : "Allow",
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "common_compute_monitoring" {
  name = "common-compute-monitoring"
}

resource "aws_cloudwatch_log_stream" "common_compute_monitoring_jobs" {
  name           = "jobs"
  log_group_name = aws_cloudwatch_log_group.common_compute_monitoring.name
}

resource "aws_s3_object" "common_compute_monitoring_jobs_json_paths" {
  bucket = aws_s3_bucket.common_compute_monitoring.id
  key    = "jobs/jsonpaths.json"
  content = jsonencode({
    "jsonpaths" : [
      "$.detail.jobId",
    ]
  })
}
