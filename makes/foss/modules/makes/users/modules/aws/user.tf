resource "aws_iam_user" "main" {
  name = var.name

  tags = {
    "Name"               = var.name
    "management:type"    = var.type
    "management:product" = var.product
  }
}

resource "aws_iam_access_key" "_1" {
  user = var.name
}

resource "aws_iam_access_key" "_2" {
  user = var.name
}
