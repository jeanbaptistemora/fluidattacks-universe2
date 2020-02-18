resource "aws_iam_user" "continuous-prod" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "continuous-prod-key" {
  user = var.user-name
}
