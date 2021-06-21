provider "github" {
  token = var.token
}

terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "4.12.0"
    }
  }
}
