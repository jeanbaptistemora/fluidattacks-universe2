resource "aws_iam_user" "main" {
  name = var.name

  tags = {
    "Name"               = var.name
    "management:type"    = var.type
    "management:product" = var.product
  }
}

