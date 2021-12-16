resource "aws_iam_user" "continuous-prod" {
  name = "continuous-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "continuous-prod"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

resource "aws_iam_access_key" "continuous-prod-key-1" {
  user = "continuous-prod"
}

resource "aws_iam_access_key" "continuous-prod-key-2" {
  user = "continuous-prod"
}

module "publish_credentials_prod" {
  source    = "../../../modules/publish_credentials"
  key_1     = aws_iam_access_key.continuous-prod-key-1
  key_2     = aws_iam_access_key.continuous-prod-key-2
  prefix    = "SERVICES_PROD"
  protected = true

  providers = {
    gitlab = gitlab.product
  }
}
