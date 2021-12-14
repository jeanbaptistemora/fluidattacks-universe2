resource "aws_iam_user" "main" {
  name = var.name
  tags = var.tags
}

