resource "aws_iam_user" "melts-prod" {
  name = "melts-prod"
  path = "/user-provision/"

  tags = {
    "Name"            = "melts-prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_access_key" "melts-prod-key-1" {
  user = "melts-prod"
}

resource "aws_iam_access_key" "melts-prod-key-2" {
  user = "melts-prod"
}

module "publish_credentials_prod" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.melts-prod-key-1
  key_2        = aws_iam_access_key.melts-prod-key-2
  prefix       = "MELTS_PROD"
  protected    = true
}
