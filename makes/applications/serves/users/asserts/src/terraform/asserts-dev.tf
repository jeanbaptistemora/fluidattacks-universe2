resource "aws_iam_user" "asserts-dev" {
  name = "asserts-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "asserts-dev"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "asserts-dev-key-1" {
  user = "asserts-dev"
}

resource "aws_iam_access_key" "asserts-dev-key-2" {
  user = "asserts-dev"
}
