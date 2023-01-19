locals {
  tags = {
    "Name"               = "prometheus"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

data "aws_eks_cluster" "k8s_cluster" {
  name = "common"
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

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
  }
}

resource "helm_release" "cert_manager" {
  name            = "cert-manager"
  description     = "Certificate manager, required to install OpenTelemtry Operator"
  repository      = "https://charts.jetstack.io"
  chart           = "cert-manager"
  version         = "1.11.0"
  namespace       = kubernetes_namespace.monitoring.metadata[0].name
  cleanup_on_fail = true
  atomic          = true

  set {
    name  = "installCRDs"
    value = "true"
  }
}

resource "helm_release" "adot_operator" {
  name            = "adot-operator"
  description     = "OpenTelemetry Operator, scrapes metrics and sends them to AWS Managed Prometheus"
  repository      = "https://open-telemetry.github.io/opentelemetry-helm-charts"
  chart           = "opentelemetry-operator"
  version         = "0.21.2"
  namespace       = kubernetes_namespace.monitoring.metadata[0].name
  cleanup_on_fail = true
  atomic          = true

  depends_on = [
    helm_release.cert_manager
  ]
}
