# AWS

resource "aws_iam_user" "web-prod" {
  name = "web-prod"
  path = "/user-provision/"

  tags = {
    "Name"            = "web-prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_access_key" "airs-prod-key-1" {
  user = "web-prod"
}

resource "aws_iam_access_key" "airs-prod-key-2" {
  user = "web-prod"
}

module "publish_credentials_prod" {
  source    = "../../../modules/publish_credentials"
  key_1     = aws_iam_access_key.airs-prod-key-1
  key_2     = aws_iam_access_key.airs-prod-key-2
  prefix    = "AIRS_PROD"
  protected = true
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
