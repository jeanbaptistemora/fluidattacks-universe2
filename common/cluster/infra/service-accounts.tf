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
    prod-skims = {
      namespace = "production"
      role      = "prod_skims"
    }
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
