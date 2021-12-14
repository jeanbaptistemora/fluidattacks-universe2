resource "aws_iam_user" "prod" {
  name = "observes-prod"
  path = "/user-provision/"

  tags = {
    "Name"            = "observes-prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_access_key" "prod-key-1" {
  user = "observes-prod"
}

resource "aws_iam_access_key" "prod-key-2" {
  user = "observes-prod"
}

module "publish_credentials_prod" {
  source    = "../../../modules/publish_credentials"
  key_1     = aws_iam_access_key.prod-key-1
  key_2     = aws_iam_access_key.prod-key-2
  prefix    = "OBSERVES_PROD"
  protected = true
}
