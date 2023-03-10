locals {
  namespace = "kube-system"
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
  name = "common-k8s"
}

resource "aws_prometheus_workspace" "monitoring" {
  alias = "common-monitoring"
  tags  = local.tags

  logging_configuration {
    log_group_arn = "${aws_cloudwatch_log_group.monitoring.arn}:*"
  }
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

data "aws_iam_policy_document" "xray_permissions" {
  statement {
    actions = [
      "xray:PutTelemetryRecords",
      "xray:PutTraceSegments"
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "monitoring_permissions" {
  source_policy_documents = [
    data.aws_iam_policy_document.prometheus_permissions.json,
    data.aws_iam_policy_document.xray_permissions.json,
  ]
}

data "aws_iam_policy_document" "k8s_oidc" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      values   = ["system:serviceaccount:${local.namespace}:${local.role_name}"]
      variable = "${replace(data.aws_eks_cluster.k8s_cluster.identity[0].oidc[0].issuer, "https://", "")}:sub"
    }

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/${replace(data.aws_eks_cluster.k8s_cluster.identity[0].oidc[0].issuer, "https://", "")}"]
    }
  }
}

resource "aws_iam_policy" "monitoring" {
  name        = "EKSMonitoring"
  description = "Permissions required for ADOT Collector to send scraped metrics to AMP and traces to X-Ray"
  policy      = data.aws_iam_policy_document.monitoring_permissions.json
}

resource "aws_iam_role" "monitoring" {
  name               = local.role_name
  assume_role_policy = data.aws_iam_policy_document.k8s_oidc.json
}

resource "aws_iam_role_policy_attachment" "prometheus_access" {
  role       = aws_iam_role.monitoring.name
  policy_arn = aws_iam_policy.monitoring.arn
}
