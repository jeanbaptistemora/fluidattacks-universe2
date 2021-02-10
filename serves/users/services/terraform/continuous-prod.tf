resource "aws_iam_user" "continuous-prod" {
  name = "continuous-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "continuous-prod"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "continuous-prod-key-1" {
  user = "continuous-prod"
}

resource "aws_iam_access_key" "continuous-prod-key-2" {
  user = "continuous-prod"
}
