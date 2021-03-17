resource "aws_iam_user" "prod" {
  name = "serves-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "serves-prod"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}
