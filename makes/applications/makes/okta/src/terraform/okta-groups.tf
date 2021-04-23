resource "okta_group" "groups" {
  for_each    = { for group in jsondecode(var.okta_groups) : group.id => group }
  name        = each.value.name
  description = each.value.description
  users       = [for user in each.value.users : okta_user.users[user].id]
}
