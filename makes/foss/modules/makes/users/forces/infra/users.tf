resource "aws_iam_user" "forces_prod" {
  name = "forces_prod"
  path = "/user_provision/"

  tags = {
    "Name"               = "forces_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_user" "forces_dev" {
  name = "forces_dev"
  path = "/user_provision/"

  tags = {
    "Name"               = "forces_dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}
