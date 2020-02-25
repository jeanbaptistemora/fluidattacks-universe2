resource "aws_iam_user" "web-prod" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "web-prod-key-1" {
  user = var.user-name
}

resource "aws_iam_access_key" "web-prod-key-2" {
  user = var.user-name
}
