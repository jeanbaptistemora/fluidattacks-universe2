# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "kubernetes_namespace" "development" {
  metadata {
    name = "development"
  }
}

resource "kubernetes_namespace" "production" {
  metadata {
    name = "production"
  }
}

locals {
  accounts = {
    dev = {
      namespace = "development"
      role      = "dev"
    }
    prod-integrates = {
      namespace = "production"
      role      = "prod_integrates"
    }
  }
}

resource "kubernetes_namespace" "main" {
  for_each = toset(local.cluster_users)

  metadata {
    name = replace(each.key, "_", "-")
  }
}

resource "kubernetes_role" "main" {
  for_each = toset(local.cluster_users)

  metadata {
    name      = replace(each.key, "_", "-")
    namespace = kubernetes_namespace.main[each.key].metadata[0].name
  }

  rule {
    api_groups     = ["*"]
    resources      = ["*"]
    resource_names = ["*"]
    verbs          = ["*"]
  }
}

resource "kubernetes_service_account" "main" {
  for_each = local.accounts

  automount_service_account_token = true

  metadata {
    name      = replace(each.key, "_", "-")
    namespace = each.value.namespace

    annotations = {
      "eks.amazonaws.com/role-arn" = "arn:aws:iam::205810638802:role/${each.value.role}"
    }
  }
}
