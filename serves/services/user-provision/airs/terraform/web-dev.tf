# AWS

resource "aws_iam_user" "web-dev" {
  name = "web-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "web-dev"
    "management:type"    = "production"
    "management:product" = "serves"
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
    ]
    resources = {
      "com.cloudflare.api.account.zone.*" = "*"
    }
  }
}
