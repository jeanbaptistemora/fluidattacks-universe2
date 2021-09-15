#AWS

resource "aws_iam_user" "integrates-dev" {
  name = "integrates-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "integrates-dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "integrates-dev-key-1" {
  user = "integrates-dev"
}

resource "aws_iam_access_key" "integrates-dev-key-2" {
  user = "integrates-dev"
}

module "publish_credentials_dev" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.integrates-dev-key-1
  key_2        = aws_iam_access_key.integrates-dev-key-2
  prefix       = "INTEGRATES_DEV"
  protected    = false
}

module "publish_credentials_dev_services" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token_services
  key_1        = aws_iam_access_key.integrates-dev-key-1
  key_2        = aws_iam_access_key.integrates-dev-key-2
  prefix       = "INTEGRATES_DEV"
  project_id   = "4603023"
  protected    = false
}

# CloudFlare

resource "cloudflare_api_token" "integrates_development" {
  name = "integrates_development"

  policy {
    effect = "allow"
    permission_groups = [
      data.cloudflare_api_token_permission_groups.all.permissions["Zone Read"],
      data.cloudflare_api_token_permission_groups.all.permissions["DNS Read"],
      data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Read"],
      data.cloudflare_api_token_permission_groups.all.permissions["Firewall Services Read"],
      data.cloudflare_api_token_permission_groups.all.permissions["Cache Purge"],
    ]
    resources = {
      "com.cloudflare.api.account.zone.*" = "*"
    }
  }
}
