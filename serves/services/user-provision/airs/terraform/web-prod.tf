resource "aws_iam_user" "web-prod" {
  name = "web-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "web-prod"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "web-prod-key-1" {
  user = "web-prod"
}

resource "aws_iam_access_key" "web-prod-key-2" {
  user = "web-prod"
}
