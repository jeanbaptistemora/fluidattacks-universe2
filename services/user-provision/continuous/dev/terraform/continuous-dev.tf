resource "aws_iam_user" "continuous-dev" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "continuous-dev-key" {
  user = var.user-name
}
