module "github_makes" {
  source = "../../../../../makes/applications/makes/foss/modules/github"

  description = "A SecDevOps framework powered by Nix"
  homepage    = "https://docs.fluidattacks.com"
  name        = "makes"
  token       = var.GITHUB_API_TOKEN
  topics      = ["build", "devops", "nix"]
}
