terraform {
  required_version = "~> 1.0"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "2.25.0"
    }
  }
}

variable "name" {}
variable "policy" {}

resource "cloudflare_api_token" "main" {
  name = var.name

  dynamic "policy" {
    for_each = var.policy
    content {
      effect            = policy.value["effect"]
      permission_groups = policy.value["permission_groups"]
      resources         = policy.value["resources"]
    }
  }
}

output "cloudflare_api_token" {
  sensitive = true
  value     = cloudflare_api_token.main.value
}
