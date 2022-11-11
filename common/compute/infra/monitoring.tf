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

data "aws_iam_policy_document" "common_compute_invoke_kinesis" {
  statement {
    actions = [
      "kinesis:PutRecord",
      "kinesis:PutRecords",
    ]

    resources = [
      aws_kinesis_stream.common_compute_monitoring_jobs.arn
    ]
  }
}

resource "aws_iam_policy" "common_compute_invoke_kinesis" {
  name = "common_compute_invoke_kinesis"

  policy = data.aws_iam_policy_document.common_compute_invoke_kinesis.json
}

data "aws_iam_policy_document" "common_compute_assume_invoke_kinesis" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = [
        // TODO: I think `events` is the right one,
        // but pending to debug and remove the unnecessary ones
        "events.amazonaws.com",
        "firehose.amazonaws.com",
        "kinesis.amazonaws.com",
        "schemas.amazonaws.com",
      ]
    }
  }
}

resource "aws_iam_role" "common_compute_invoke_kinesis" {
  name = "common-compute-invoke-kinesis"

  assume_role_policy = data.aws_iam_policy_document.common_compute_assume_invoke_kinesis.json
}

resource "aws_iam_role_policy_attachment" "common_compute_invoke_kinesis" {
  role       = aws_iam_role.common_compute_invoke_kinesis.name
  policy_arn = aws_iam_policy.common_compute_invoke_kinesis.arn
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
  role_arn = aws_iam_role.common_compute_invoke_kinesis.arn

  kinesis_target {
    partition_key_path = "$.detail.jobId"
  }
}
