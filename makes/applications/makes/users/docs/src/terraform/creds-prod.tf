# AWS

resource "aws_iam_user" "prod" {
  name = "docs_prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "docs_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "prod_1" {
  user = "docs_prod"
}

resource "aws_iam_access_key" "prod_2" {
  user = "docs_prod"
}


# CloudFlare

resource "cloudflare_api_token" "prod" {
  name = "docs_prod"

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
