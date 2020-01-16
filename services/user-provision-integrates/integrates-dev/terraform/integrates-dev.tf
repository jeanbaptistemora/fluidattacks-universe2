resource "aws_iam_user" "integrates-dev" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "integrates-dev-key" {
  user = var.user-name
}
