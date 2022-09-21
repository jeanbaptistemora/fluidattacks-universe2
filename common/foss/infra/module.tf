# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

module "github_makes" {
  source = "./modules/github"

  description = "A DevSecOps framework powered by Nix."
  homepage    = null
  name        = "makes"
  token       = var.githubToken
  topics      = ["build", "cd", "ci", "devops", "devsecops", "nix"]

  enable_pages = true

  secrets = {
  }
}
