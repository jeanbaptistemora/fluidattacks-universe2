resource "aws_iam_user" "skims_dev" {
  name = var.user_name
  path = "/user_provision/"

  tags = {
    "management:type"    = "production"
    "management:product" = "serves"
  }
}
