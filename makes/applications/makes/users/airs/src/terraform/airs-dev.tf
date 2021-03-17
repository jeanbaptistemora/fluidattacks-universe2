# AWS

resource "aws_iam_user" "web-dev" {
  name = "web-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "web-dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "web-dev-key-1" {
  user = "web-dev"
}

resource "aws_iam_access_key" "web-dev-key-2" {
  user = "web-dev"
}


# CloudFlare

resource "cloudflare_api_token" "airs_development" {
  name = "airs_development"

  policy {
    effect = "allow"
    permission_groups = [
      data.cloudflare_api_token_permission_groups.all.permissions["DNS Read"],
      data.cloudflare_api_token_permission_groups.all.permissions["Workers Routes Read"],
      data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Read"],
    ]
    resources = {
      "com.cloudflare.api.account.zone.*" = "*"
    }
  }

  policy {
    effect = "allow"
    permission_groups = [
      data.cloudflare_api_token_permission_groups.all.permissions["Workers Scripts Read"],
    ]
    resources = {
      "com.cloudflare.api.account.*" = "*"
    }
  }
}
