provider "github" {
  owner = "fluidattacks"
  token = var.token
}

terraform {
  required_version = "~> 1.0"

  required_providers {
    github = {
      source  = "integrations/github"
      version = "5.7.0"
    }
  }
}
