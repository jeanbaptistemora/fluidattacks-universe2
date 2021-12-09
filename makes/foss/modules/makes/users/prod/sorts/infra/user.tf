resource "aws_iam_user" "sorts_prod" {
  name = "sorts_prod"
  path = "/user_provision/"

  tags = {
    "Name"            = "sorts_prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_access_key" "sorts_prod_key-1" {
  user = "sorts_prod"
}

resource "aws_iam_access_key" "sorts_prod_key-2" {
  user = "sorts_prod"
}

provider "gitlab" {
  token = var.gitlab_token
}

module "publish_credentials_prod" {
  source    = "../../../modules/publish_credentials"
  key_1     = aws_iam_access_key.sorts_prod_key-1
  key_2     = aws_iam_access_key.sorts_prod_key-2
  prefix    = "SORTS_PROD"
  protected = true
}
