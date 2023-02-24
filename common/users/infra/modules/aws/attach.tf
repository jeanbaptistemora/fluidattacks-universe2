module "main_policies" {
  source = "../policies"

  aws_role = aws_iam_role.main
  policies = var.policies
  tags     = var.tags
}

resource "aws_iam_role_policy_attachment" "main_attachments" {
  for_each   = module.main_policies.aws_policies
  role       = aws_iam_role.main.name
  policy_arn = each.value.arn
}
