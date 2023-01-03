terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 3.10.0"
    }
  }
}

variable "domain" {}