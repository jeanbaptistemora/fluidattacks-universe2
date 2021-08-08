resource "aws_iam_user" "sorts_prod" {
  name = "sorts_prod"
  path = "/user_provision/"

  tags = {
    "Name"               = "sorts_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_user" "sorts_dev" {
  name = "sorts_dev"
  path = "/user_provision/"

  tags = {
    "Name"               = "sorts_dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}
