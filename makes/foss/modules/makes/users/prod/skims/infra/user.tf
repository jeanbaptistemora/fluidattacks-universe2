resource "aws_iam_user" "skims_prod" {
  name = "skims_prod"
  path = "/user_provision/"

  tags = {
    "Name"               = "skims_prod"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

resource "aws_iam_access_key" "skims_prod_key-1" {
  user = "skims_prod"
}

resource "aws_iam_access_key" "skims_prod_key-2" {
  user = "skims_prod"
}

provider "gitlab" {
  token = var.gitlab_token
}

module "publish_credentials_prod" {
  source    = "../../../modules/publish_credentials"
  key_1     = aws_iam_access_key.skims_prod_key-1
  key_2     = aws_iam_access_key.skims_prod_key-2
  prefix    = "SKIMS_PROD"
  protected = false
}
