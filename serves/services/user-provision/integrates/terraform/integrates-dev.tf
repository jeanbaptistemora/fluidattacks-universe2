resource "aws_iam_user" "integrates-dev" {
  name = "integrates-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "integrates-dev"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "integrates-dev-key-1" {
  user = "integrates-dev"
}

resource "aws_iam_access_key" "integrates-dev-key-2" {
  user = "integrates-dev"
}
