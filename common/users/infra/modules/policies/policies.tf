locals {
  prefix = "${var.aws_role.name}_"
  prefixed_policies = merge(
    { for k, v in var.policies : join("", [local.prefix, k]) => v },
    {
      "${local.prefix}pass_self" = [{
        Sid    = "PassSelf"
        Effect = "Allow"
        Action = ["iam:PassRole"]
        Resource = [
          var.aws_role.arn
        ]
      }]
    }
  )
}

resource "aws_iam_policy" "main" {
  for_each = local.prefixed_policies

  name = each.key
  policy = jsonencode(
    {
      Version   = "2012-10-17",
      Statement = each.value
    }
  )
  tags = var.tags
}

output "aws_policies" {
  value       = aws_iam_policy.main
  description = "The created aws policies with an aditional pass self policy (i.e. {aws_role.name}_pass_self) for the role {aws_role.name}"
}
