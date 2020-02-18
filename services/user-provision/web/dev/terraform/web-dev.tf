resource "aws_iam_user" "web-dev" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "web-dev-key" {
  user = var.user-name
}
