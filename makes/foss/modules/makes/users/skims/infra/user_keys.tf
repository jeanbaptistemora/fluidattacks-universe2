resource "aws_iam_access_key" "skims_prod_key-1" {
  user = "skims_prod"
}

resource "aws_iam_access_key" "skims_prod_key-2" {
  user = "skims_prod"
}

resource "aws_iam_access_key" "skims_dev_key-1" {
  user = "skims_dev"
}

resource "aws_iam_access_key" "skims_dev_key-2" {
  user = "skims_dev"
}

module "publish_credentials_dev" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.skims_dev_key-1
  key_2        = aws_iam_access_key.skims_dev_key-2
  prefix       = "SKIMS_DEV"
  protected    = false
}

module "publish_credentials_prod" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.skims_prod_key-1
  key_2        = aws_iam_access_key.skims_prod_key-2
  prefix       = "SKIMS_PROD"
  protected    = false
}
