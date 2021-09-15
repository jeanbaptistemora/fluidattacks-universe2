resource "aws_iam_user" "continuous-dev" {
  name = "continuous-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "continuous-dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "continuous-dev-key-1" {
  user = "continuous-dev"
}

resource "aws_iam_access_key" "continuous-dev-key-2" {
  user = "continuous-dev"
}

module "publish_credentials_dev" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.continuous-dev-key-1
  key_2        = aws_iam_access_key.continuous-dev-key-2
  prefix       = "SERVICES_DEV"
  protected    = false
}

module "publish_credentials_dev_services" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token_services
  key_1        = aws_iam_access_key.continuous-dev-key-1
  key_2        = aws_iam_access_key.continuous-dev-key-2
  prefix       = "DEV"
  project_id   = "4603023"
  protected    = false
}
