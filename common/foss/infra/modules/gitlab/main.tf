provider "gitlab" {
  token = var.token
}

terraform {
  required_version = "~> 1.0"

  required_providers {
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "3.12.0"
    }
  }
}
