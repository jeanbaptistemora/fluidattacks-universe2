locals {
  data = jsondecode(var.okta_data)

  apps   = local.data.apps
  groups = local.data.groups
  rules  = local.data.rules
  users  = local.data.users

  user_groups = local.data.user_groups
  app_groups  = local.data.app_groups
  app_users   = local.data.app_users

  aws_group_roles = local.data.aws_group_roles
  aws_user_roles  = local.data.aws_user_roles
}
