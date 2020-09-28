resource "aws_iam_user" "prod" {
  name = "serves-prod"
  path = "/user-provision/"

  tags = {
    "management:type"    = "production"
    "management:product" = "serves"
  }
}
