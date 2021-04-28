resource "okta_group" "groups" {
  for_each = {
    for _, group in local.groups : group.id => group
    if group.type == "users"
  }

  name        = each.value.name
  description = each.value.description
  users       = [for user in each.value.users : okta_user.users[user].id]
}

resource "okta_group" "groups_rules" {
  for_each = {
    for _, group in local.groups : group.id => group
    if group.type == "rules"
  }

  name        = each.value.name
  description = each.value.description
  users       = null

  lifecycle {
    ignore_changes = [
      users,
    ]
  }
}
