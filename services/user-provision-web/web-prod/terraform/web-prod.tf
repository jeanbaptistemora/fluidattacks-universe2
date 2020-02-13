resource "aws_iam_user" "web-prod" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "web-prod-key" {
  user = var.user-name
}
