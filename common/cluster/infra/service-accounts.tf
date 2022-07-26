data "aws_iam_role" "main" {
  for_each = toset([
    "dev",
    "prod_integrates",
  ])

  name = each.key
}

resource "kubernetes_service_account" "main" {
  for_each = data.aws_iam_role.main

  automount_service_account_token = true

  metadata {
    name      = replace(each.key, "_", "-")
    namespace = "kube-system"

    annotations = {
      "eks.amazonaws.com/role-arn" = each.value.arn
    }
  }
}
