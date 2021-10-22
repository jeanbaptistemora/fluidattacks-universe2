resource "aws_iam_user" "forces_prod" {
  name = "forces_prod"
  path = "/user_provision/"

  tags = {
    "Name"               = "forces_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "forces_prod_key-1" {
  user = "forces_prod"
}

resource "aws_iam_access_key" "forces_prod_key-2" {
  user = "forces_prod"
}

module "publish_credentials_prod" {
  source       = "../../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.forces_prod_key-1
  key_2        = aws_iam_access_key.forces_prod_key-2
  prefix       = "FORCES_PROD"
  protected    = true
}
