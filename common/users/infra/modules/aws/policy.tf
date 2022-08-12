locals {
  policy = {
    Version = "2012-10-17",
    Statement = concat(
      [
        {
          Sid    = "PassSelf"
          Effect = "Allow"
          Action = ["iam:PassRole"]
          Resource = [
            aws_iam_role.main.arn
          ]
        },
      ],
      var.policy,
    )
  }
}

resource "aws_iam_policy" "main" {
  name   = var.name
  policy = jsonencode(local.policy)
  tags   = var.tags
}

resource "aws_iam_user_policy_attachment" "main" {
  user       = var.name
  policy_arn = aws_iam_policy.main.arn
}
