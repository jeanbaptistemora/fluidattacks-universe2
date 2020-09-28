resource "aws_iam_user" "continuous-prod" {
  name = var.user-name
  path = "/user-provision/"

  tags = {
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "continuous-prod-key-1" {
  user = var.user-name
}

resource "aws_iam_access_key" "continuous-prod-key-2" {
  user = var.user-name
}
