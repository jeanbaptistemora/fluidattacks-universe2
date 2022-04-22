variable "productApiToken" {}
variable "region" {
  default = "us-east-1"
}

data "aws_iam_role" "prod_common" {
  name = "prod_common"
}

data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "common" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["common"]
  }
}
