# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
