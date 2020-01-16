resource "aws_iam_user" "integrates-prod" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "integrates-prod-key" {
  user = var.user-name
}
