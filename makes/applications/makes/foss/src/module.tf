module "github_makes" {
  source = "../../../../../makes/applications/makes/foss/modules/github"

  description = "A DevSecOps framework powered by Nix."
  homepage    = null
  name        = "makes"
  token       = var.GITHUB_API_TOKEN
  topics      = ["build", "cd", "ci", "devops", "devsecops", "nix"]

  secrets = {
  }
}
