module "github_makes" {
  source = "../../../../../makes/applications/makes/foss/modules/github"

  description = "A SecDevOps framework powered by Nix."
  homepage    = null
  name        = "makes"
  token       = var.GITHUB_API_TOKEN
  topics      = ["build", "cd", "ci", "devops", "nix"]

  secrets = {
  }
}
