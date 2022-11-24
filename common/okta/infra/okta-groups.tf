resource "okta_group" "groups" {
  for_each = {
    for _, group in local.data.groups : group.id => group
  }

  name        = each.value.name
  description = each.value.description

  lifecycle {
    ignore_changes = [
      users,
    ]
  }
}

resource "okta_group_memberships" "memberships" {
  for_each = {
    for group, data in local.data.groups : group => data
    if length(data.users) > 0
  }

  group_id = okta_group.groups[each.key].id
  users    = [for user in each.value.users : okta_user.users[user].id]
}

resource "okta_group_rule" "rules" {
  for_each = {
    for _, rule in local.data.rules : rule.id => rule
  }

  name             = each.value.name
  status           = each.value.status
  expression_type  = each.value.expression_type
  expression_value = each.value.expression_value

  group_assignments = [
    for group in local.data.groups : okta_group.groups[group.id].id
    if contains(group.rules, each.key)
  ]
}
