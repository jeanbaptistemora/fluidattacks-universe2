resource "aws_cloudwatch_log_group" "monitoring" {
  name = "common-monitoring"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_cloudwatch_log_stream" "compute_jobs" {
  name           = "compute-jobs"
  log_group_name = aws_cloudwatch_log_group.monitoring.name

  lifecycle {
    prevent_destroy = true
  }
}
