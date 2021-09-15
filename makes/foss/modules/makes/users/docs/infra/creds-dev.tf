# AWS

resource "aws_iam_user" "dev" {
  name = "docs_dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "docs_dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "dev_1" {
  user = "docs_dev"
}

resource "aws_iam_access_key" "dev_2" {
  user = "docs_dev"
}

module "publish_credentials_dev" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.dev_1
  key_2        = aws_iam_access_key.dev_2
  prefix       = "DOCS_DEV"
  protected    = false
}

# CloudFlare

resource "cloudflare_api_token" "dev" {
  name = "docs_dev"

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
