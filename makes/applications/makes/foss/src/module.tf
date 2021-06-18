module "gitlab_makes" {
  source = "../../../../../makes/applications/makes/foss/modules/gitlab"

  description = "A SecDevOps framework based on Nix"
  group       = "fluidattacks"
  name        = "makes"
  token       = var.PRODUCT_API_TOKEN
}
