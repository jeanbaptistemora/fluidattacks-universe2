locals {
  role_name = "monitoring"
  tags = {
    "Name"               = "prometheus"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

data "aws_caller_identity" "current" {}

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

data "aws_iam_policy_document" "prometheus_permissions" {
  statement {
    actions = [
      "aps:GetLabels",
      "aps:GetMetricMetadata",
      "aps:GetSeries",
      "aps:RemoteWrite"
    ]
    resources = [
      aws_prometheus_workspace.monitoring.arn
    ]
  }
}

data "aws_iam_policy_document" "k8s_oidc" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      values   = ["system:serviceaccount:${kubernetes_namespace.monitoring.metadata[0].name}:${local.role_name}"]
      variable = "${data.aws_eks_cluster.k8s_cluster.identity[0].oidc[0].issuer}:sub"
    }

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/${data.aws_eks_cluster.k8s_cluster.identity[0].oidc[0].issuer}"]
    }
  }
}

resource "aws_iam_policy" "prometheus" {
  name        = "EKSPrometheusAccess"
  description = "Permissions required for ADOT Collector to send scraped metrics to AMP"
  policy      = data.aws_iam_policy_document.prometheus_permissions.json
}

resource "aws_iam_role" "monitoring" {
  name               = local.role_name
  assume_role_policy = data.aws_iam_policy_document.k8s_oidc.json
}

resource "aws_iam_role_policy_attachment" "prometheus_access" {
  role       = aws_iam_role.monitoring.name
  policy_arn = aws_iam_policy.prometheus.arn
}

resource "kubernetes_service_account" "monitoring" {
  automount_service_account_token = true
  metadata {
    name      = local.role_name
    namespace = kubernetes_namespace.monitoring.metadata[0].name

    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.monitoring.arn
    }
  }
}

resource "kubernetes_cluster_role" "monitoring" {
  metadata {
    name = local.role_name
  }

  rule {
    api_groups = [""]
    resources = [
      "endpoints",
      "nodes",
      "nodes/metrics",
      "nodes/proxy",
      "pods",
      "services"
    ]
    verbs = [
      "get",
      "list",
      "watch"
    ]
  }

  rule {
    non_resource_urls = ["/metrics"]
    verbs             = ["get"]
  }
}

resource "kubernetes_cluster_role_binding" "monitoring" {
  metadata {
    name = local.role_name
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.monitoring.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.monitoring.metadata[0].name
    namespace = kubernetes_namespace.monitoring.metadata[0].name
  }
}
