resource "aws_iam_user" "main" {
  name = var.name

  tags = {
    "Name"            = var.name
    "management:area" = var.area
    "management:type" = var.type
  }
}

