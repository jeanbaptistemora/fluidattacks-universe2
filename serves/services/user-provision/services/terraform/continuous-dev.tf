resource "aws_iam_user" "continuous-dev" {
  name = "continuous-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "continuous-dev"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "continuous-dev-key-1" {
  user = "continuous-dev"
}

resource "aws_iam_access_key" "continuous-dev-key-2" {
  user = "continuous-dev"
}
