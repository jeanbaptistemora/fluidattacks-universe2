resource "aws_iam_user" "web-dev" {
  name = "web-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "web-dev"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "web-dev-key-1" {
  user = "web-dev"
}

resource "aws_iam_access_key" "web-dev-key-2" {
  user = "web-dev"
}
