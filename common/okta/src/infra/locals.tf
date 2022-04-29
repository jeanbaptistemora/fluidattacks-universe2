locals {
  data = jsondecode(
    <<-EOF
      {
        "apps": ${var.oktaDataApps},
        "groups": ${var.oktaDataGroups},
        "rules": ${var.oktaDataRules},
        "users": ${var.oktaDataUsers},
        "app_groups": ${var.oktaDataAppGroups},
        "app_users": ${var.oktaDataAppUsers},
        "aws_group_roles": ${var.oktaDataAwsGroupRoles},
        "aws_user_roles": ${var.oktaDataAwsUserRoles}
      }
    EOF
  )
}
