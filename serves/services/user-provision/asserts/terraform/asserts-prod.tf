resource "aws_iam_user" "asserts-prod" {
  name = "asserts-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "asserts-prod"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "asserts-prod-key-1" {
  user = "asserts-prod"
}

resource "aws_iam_access_key" "asserts-prod-key-2" {
  user = "asserts-prod"
}
