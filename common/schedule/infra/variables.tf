variable "productApiToken" {}
variable "region" {
  default = "us-east-1"
}

data "aws_iam_role" "prod_common" {
  name = "prod_common"
}
