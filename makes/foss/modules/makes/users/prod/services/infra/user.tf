resource "aws_iam_user" "continuous-prod" {
  name = "continuous-prod"
  path = "/user-provision/"

  tags = {
    "Name"            = "continuous-prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_access_key" "continuous-prod-key-1" {
  user = "continuous-prod"
}

resource "aws_iam_access_key" "continuous-prod-key-2" {
  user = "continuous-prod"
}

module "publish_credentials_prod" {
  source       = "../../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.continuous-prod-key-1
  key_2        = aws_iam_access_key.continuous-prod-key-2
  prefix       = "SERVICES_PROD"
  protected    = true
}

module "publish_credentials_prod_services" {
  source       = "../../../modules/publish_credentials"
  gitlab_token = var.gitlab_token_services
  key_1        = aws_iam_access_key.continuous-prod-key-1
  key_2        = aws_iam_access_key.continuous-prod-key-2
  prefix       = "PROD"
  project_id   = "4603023"
  protected    = true
}
