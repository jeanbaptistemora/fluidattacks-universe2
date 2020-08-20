resource "aws_iam_user" "integrates-prod" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "integrates-prod-key-1" {
  user = var.user-name
}

resource "aws_iam_access_key" "integrates-prod-key-2" {
  user = var.user-name
}
