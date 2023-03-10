locals {
  admins          = ["prod_common"]
  monitoring_role = "monitoring"
  users = [
    "dev",
    "prod_integrates",
  ]
}

data "aws_iam_role" "main" {
  for_each = toset(concat(local.admins, local.users))

  name = each.key
}

resource "kubernetes_namespace" "main" {
  for_each = toset(local.users)

  metadata {
    name = replace(each.key, "_", "-")
  }
}

resource "kubernetes_service_account" "main" {
  for_each = toset(local.users)

  automount_service_account_token = true

  metadata {
    name      = replace(each.key, "_", "-")
    namespace = kubernetes_namespace.main[each.key].metadata[0].name

    annotations = {
      "eks.amazonaws.com/role-arn" = data.aws_iam_role.main[each.key].arn
    }
  }
}

resource "kubernetes_role" "main" {
  for_each = toset(local.users)

  metadata {
    name      = replace(each.key, "_", "-")
    namespace = kubernetes_namespace.main[each.key].metadata[0].name
  }

  rule {
    api_groups = ["*"]
    resources  = ["*"]
    verbs      = ["*"]
  }
}

resource "kubernetes_cluster_role" "main" {
  for_each = toset(local.users)

  metadata {
    name = replace(each.key, "_", "-")
  }

  rule {
    api_groups = [
      "",
      "apps",
      "opentelemetry.io",
      "rbac.authorization.k8s.io"
    ]
    resources = [
      "clusterrolebindings",
      "clusterroles",
      "configmaps",
      "daemonsets",
      "namespaces",
      "opentelemetrycollectors",
      "rolebindings",
      "roles",
      "serviceaccounts",
      "services",
    ]
    verbs = ["get"]
  }
  rule {
    api_groups = ["", "apiextensions.k8s.io"]
    resources = [
      "customresourcedefinitions",
      "secrets"
    ]
    verbs = ["list"]
  }
}

resource "kubernetes_role_binding" "main" {
  for_each = toset(local.users)

  metadata {
    name      = replace(each.key, "_", "-")
    namespace = kubernetes_namespace.main[each.key].metadata[0].name
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role.main[each.key].metadata[0].name
  }

  subject {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Group"
    name      = each.key
  }
}

resource "kubernetes_cluster_role_binding" "main" {
  for_each = toset(local.users)

  metadata {
    name = replace(each.key, "_", "-")
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.main[each.key].metadata[0].name
  }

  subject {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Group"
    name      = each.key
  }
}

# Monitoring cluster role
data "aws_iam_role" "monitoring" {
  name = local.monitoring_role
}

resource "kubernetes_service_account" "monitoring" {
  automount_service_account_token = true
  metadata {
    name      = local.monitoring_role
    namespace = local.kube_namespace

    annotations = {
      "eks.amazonaws.com/role-arn" = data.aws_iam_role.monitoring.arn
    }
  }
}

resource "kubernetes_cluster_role" "monitoring" {
  metadata {
    name = local.monitoring_role
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
    name = local.monitoring_role
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.monitoring.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.monitoring.metadata[0].name
    namespace = local.kube_namespace
  }
}
