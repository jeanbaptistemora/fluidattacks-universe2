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
