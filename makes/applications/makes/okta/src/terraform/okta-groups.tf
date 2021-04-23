resource "okta_group" "groups" {
  for_each    = { for _, group in local.groups : group.id => group }
  name        = each.value.name
  description = each.value.description
  users       = [for _, user in each.value.users : okta_user.users[user].id]
}
