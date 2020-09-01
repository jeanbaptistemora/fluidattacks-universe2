resource "aws_iam_user" "melts-prod" {
  name = "melts-prod"
  path = "/user-provision/"
}

resource "aws_iam_access_key" "melts-prod-key-1" {
  user = "melts-prod"
}

resource "aws_iam_access_key" "melts-prod-key-2" {
  user = "melts-prod"
}
