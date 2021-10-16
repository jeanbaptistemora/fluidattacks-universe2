resource "aws_iam_user" "main" {
  name = var.name

  tags = {
    "Name"               = var.name
    "management:type"    = var.type
    "management:product" = var.product
  }
}

resource "aws_iam_access_key" "1" {
  user = var.name
}

resource "aws_iam_access_key" "2" {
  user = var.name
}
