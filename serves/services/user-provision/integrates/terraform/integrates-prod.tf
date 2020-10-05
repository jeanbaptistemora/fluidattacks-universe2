resource "aws_iam_user" "integrates-prod" {
  name = "integrates-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "integrates-prod"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "integrates-prod-key-1" {
  user = "integrates-prod"
}

resource "aws_iam_access_key" "integrates-prod-key-2" {
  user = "integrates-prod"
}
