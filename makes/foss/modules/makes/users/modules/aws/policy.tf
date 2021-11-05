resource "aws_iam_policy" "main" {
  name   = var.name
  policy = var.policy

  tags = {
    "Name"            = var.name
    "management:area" = var.area
    "management:type" = var.type
  }
}

resource "aws_iam_user_policy_attachment" "main" {
  user       = var.name
  policy_arn = aws_iam_policy.main.arn
}

