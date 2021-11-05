# AWS

resource "aws_iam_user" "integrates-prod" {
  name = "integrates-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "integrates-prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "integrates-prod-key-1" {
  user = "integrates-prod"
}

resource "aws_iam_access_key" "integrates-prod-key-2" {
  user = "integrates-prod"
}

module "publish_credentials_prod" {
  source       = "../../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.integrates-prod-key-1
  key_2        = aws_iam_access_key.integrates-prod-key-2
  prefix       = "INTEGRATES_PROD"
  protected    = true
}

module "publish_credentials_prod_services" {
  source       = "../../../modules/publish_credentials"
  gitlab_token = var.gitlab_token_services
  key_1        = aws_iam_access_key.integrates-prod-key-1
  key_2        = aws_iam_access_key.integrates-prod-key-2
  prefix       = "INTEGRATES_PROD"
  project_id   = "4603023"
  protected    = true
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
