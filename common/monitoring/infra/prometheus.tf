resource "aws_prometheus_workspace" "monitoring" {
  alias = "common-monitoring"
  tags = {
    "Name"               = "prometheus"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }

  logging_configuration {
    log_group_arn = "${aws_cloudwatch_log_group.monitoring.arn}:*"
  }
}
