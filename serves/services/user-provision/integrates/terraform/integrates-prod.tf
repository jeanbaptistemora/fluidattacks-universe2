# AWS

resource "aws_iam_user" "integrates-prod" {
  name = "integrates-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "integrates-prod"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "integrates-prod-key-1" {
  user = "integrates-prod"
}

resource "aws_iam_access_key" "integrates-prod-key-2" {
  user = "integrates-prod"
}


# CloudFlare

resource "cloudflare_api_token" "integrates_production" {
  name = "integrates_production"

  policy {
    effect = "allow"
    permission_groups = [
      data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Write"],
      data.cloudflare_api_token_permission_groups.all.permissions["DNS Write"],
    ]
    resources = {
      "com.cloudflare.api.account.zone.*" = "*"
    }
  }
}
