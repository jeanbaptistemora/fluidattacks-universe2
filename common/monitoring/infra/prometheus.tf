locals {
  tags = {
    "Name"               = "prometheus"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

data "aws_subnet" "k8s_subnets" { # common/vpc/infra/subnets.tf
  count = 3
  filter {
    name   = "tag:Name"
    values = ["k8s_${count.index + 1}"]
  }
}

resource "aws_vpc_endpoint" "prometheus_endpoint" {
  service_name = "com.amazonaws.us-east-1.aps-workspaces"
  vpc_id       = data.aws_subnet.k8s_subnets[0].vpc_id
  subnet_ids = [
    for subnet in data.aws_subnet.k8s_subnets : subnet.id
  ]
  vpc_endpoint_type = "Interface"
  tags              = local.tags
}

resource "aws_prometheus_workspace" "monitoring" {
  alias = "common-monitoring"
  tags  = local.tags

  logging_configuration {
    log_group_arn = "${aws_cloudwatch_log_group.monitoring.arn}:*"
  }
}
