# AWS

resource "aws_iam_user" "web-prod" {
  name = "web-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "web-prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "web-prod-key-1" {
  user = "web-prod"
}

resource "aws_iam_access_key" "web-prod-key-2" {
  user = "web-prod"
}


# CloudFlare

resource "cloudflare_api_token" "airs_production" {
  name = "airs_production"

  policy {
    effect = "allow"
    permission_groups = [
      data.cloudflare_api_token_permission_groups.all.permissions["Workers Routes Write"],
      data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Write"],
      data.cloudflare_api_token_permission_groups.all.permissions["DNS Write"],
    ]
    resources = {
      "com.cloudflare.api.account.zone.*" = "*"
    }
  }

  policy {
    effect = "allow"
    permission_groups = [
      data.cloudflare_api_token_permission_groups.all.permissions["Workers Scripts Write"],
    ]
    resources = {
      "com.cloudflare.api.account.*" = "*"
    }
  }
}
