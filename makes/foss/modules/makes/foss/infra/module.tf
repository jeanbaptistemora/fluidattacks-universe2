module "github_makes" {
  source = "./modules/github"

  description = "A DevSecOps framework powered by Nix."
  homepage    = null
  name        = "makes"
  token       = var.githubToken
  topics      = ["build", "cd", "ci", "devops", "devsecops", "nix"]

  secrets = {
  }
}
