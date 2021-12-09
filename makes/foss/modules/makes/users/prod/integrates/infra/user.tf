# AWS

resource "aws_iam_user" "integrates-prod" {
  name = "integrates-prod"
  path = "/user-provision/"

  tags = {
    "Name"            = "integrates-prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_access_key" "integrates-prod-key-1" {
  user = "integrates-prod"
}

resource "aws_iam_access_key" "integrates-prod-key-2" {
  user = "integrates-prod"
}

provider "gitlab" {
  token = var.gitlab_token
}

module "publish_credentials_prod" {
  source    = "../../../modules/publish_credentials"
  key_1     = aws_iam_access_key.integrates-prod-key-1
  key_2     = aws_iam_access_key.integrates-prod-key-2
  prefix    = "INTEGRATES_PROD"
  protected = true
}

# CloudFlare

resource "cloudflare_api_token" "integrates_production" {
  name = "integrates_production"

  policy {
    effect = "allow"
    permission_groups = [
      data.cloudflare_api_token_permission_groups.all.permissions["Zone Read"],
      data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Write"],
      data.cloudflare_api_token_permission_groups.all.permissions["Firewall Services Write"],
      data.cloudflare_api_token_permission_groups.all.permissions["DNS Write"],
      data.cloudflare_api_token_permission_groups.all.permissions["Cache Purge"],
    ]
    resources = {
      "com.cloudflare.api.account.zone.*" = "*"
    }
  }
}
