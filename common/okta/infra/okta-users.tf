# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "okta_user" "users" {
  for_each    = { for _, user in local.data.users : user.id => user }
  email       = each.value.email
  first_name  = each.value.first_name
  last_name   = each.value.last_name
  login       = each.value.email
  admin_roles = each.value.admin_roles
  status      = each.value.status
}
