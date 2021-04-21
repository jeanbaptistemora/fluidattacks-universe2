resource "okta_group" "groups" {
  for_each    = jsondecode(var.okta_groups)
  name        = each.value.name
  description = each.value.description
  users       = [for user in each.value.users : okta_user.users[user].id]
}
