module "main_role" {
  source = "../role"

  name               = var.name
  assume_role_policy = var.assume_role_policy
  tags               = var.tags
}

module "main_policies" {
  source = "../policies"

  aws_role = module.main_role.aws_role
  policies = var.policies
  tags     = var.tags
}

resource "aws_iam_role_policy_attachment" "main_attachments" {
  for_each   = module.main_policies.aws_policies
  role       = module.main_role.aws_role.name
  policy_arn = each.value.arn
}
