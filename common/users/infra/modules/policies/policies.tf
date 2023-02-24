locals {
  pass_self = {
    Sid    = "PassSelf"
    Effect = "Allow"
    Action = ["iam:PassRole"]
    Resource = [
      var.aws_role.arn
    ]
  }
}

resource "aws_iam_policy" "main" {
  for_each = var.policies

  name = each.key
  policy = jsonencode(
    {
      Version = "2012-10-17",
      Statement = concat(
        [local.pass_self],
        each.value,
      )
    }
  )
  tags = var.tags
}

output "aws_policies" {
  value       = aws_iam_policy.main
  description = "The created aws policies."
}
