resource "aws_iam_user" "skims_prod" {
  name = var.user_name
  path = "/user_provision/"

  tags = {
    "Name"               = "skims_prod"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}
