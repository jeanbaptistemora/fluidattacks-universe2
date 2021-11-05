resource "aws_iam_user" "skims_prod" {
  name = "skims_prod"
  path = "/user_provision/"

  tags = {
    "Name"            = "skims_prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_user" "skims_dev" {
  name = "skims_dev"
  path = "/user_provision/"

  tags = {
    "Name"            = "skims_dev"
    "management:area" = "innovation"
    "management:type" = "product"
  }
}
