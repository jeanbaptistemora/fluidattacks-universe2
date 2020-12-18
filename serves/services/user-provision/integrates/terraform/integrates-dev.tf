#AWS

resource "aws_iam_user" "integrates-dev" {
  name = "integrates-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "integrates-dev"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "integrates-dev-key-1" {
  user = "integrates-dev"
}

resource "aws_iam_access_key" "integrates-dev-key-2" {
  user = "integrates-dev"
}


# CloudFlare

resource "cloudflare_api_token" "integrates_development" {
  name = "integrates_development"

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
