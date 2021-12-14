resource "aws_iam_policy" "main" {
  name   = var.name
  policy = var.policy
  tags   = var.tags
}

resource "aws_iam_user_policy_attachment" "main" {
  user       = var.name
  policy_arn = aws_iam_policy.main.arn
}

