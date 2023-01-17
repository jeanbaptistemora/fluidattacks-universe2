resource "aws_prometheus_workspace" "monitoring" {
  alias = "common-monitoring"

  logging_configuration {
    log_group_arn = aws_cloudwatch_log_group.monitoring.arn
  }

  tags = {
    "Name"               = "prometheus"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
    "Access"             = "private"
  }
}
