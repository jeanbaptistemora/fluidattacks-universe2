resource "aws_iam_user" "dev" {
  name = "serves-dev"
  path = "/user-provision/"
}

resource "aws_iam_access_key" "dev-key-1" {
  user = "serves-dev"
}

resource "aws_iam_access_key" "dev-key-2" {
  user = "serves-dev"
}
