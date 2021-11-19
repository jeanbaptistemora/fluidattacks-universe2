resource "aws_iam_user" "prod" {
  name = "serves-prod"
  path = "/user-provision/"

  tags = {
    "Name"            = "serves-prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_access_key" "prod-key-1" {
  user = "serves-prod"
}

resource "aws_iam_access_key" "prod-key-2" {
  user = "serves-prod"
}

module "publish_credentials_prod" {
  source       = "../../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.prod-key-1
  key_2        = aws_iam_access_key.prod-key-2
  prefix       = "MAKES_PROD"
  protected    = true
}
