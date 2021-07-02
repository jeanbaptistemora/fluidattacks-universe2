module "github_makes" {
  source = "../../../../../makes/applications/makes/foss/modules/github"

  description = "A SecDevOps framework powered by Nix"
  homepage    = null
  name        = "makes"
  token       = var.GITHUB_API_TOKEN
  topics      = ["build", "cd", "ci", "devops", "nix"]

  secrets = {
    GITLAB_TOKEN  = var.PRODUCT_API_TOKEN
    GITLAB_USER   = var.PRODUCT_API_USER
    _GITHUB_TOKEN = var.GITHUB_API_TOKEN
    _GITHUB_USER  = var.GITHUB_API_USER
  }
}
