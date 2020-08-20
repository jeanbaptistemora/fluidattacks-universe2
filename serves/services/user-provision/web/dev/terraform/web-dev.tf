resource "aws_iam_user" "web-dev" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "web-dev-key-1" {
  user = var.user-name
}

resource "aws_iam_access_key" "web-dev-key-2" {
  user = var.user-name
}
