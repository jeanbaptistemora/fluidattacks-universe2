resource "okta_group" "groups" {
  for_each = {
    for _, group in local.groups : group.id => group
  }

  name        = each.value.name
  description = each.value.description

  lifecycle {
    ignore_changes = [
      users,
    ]
  }
}

resource "okta_group_membership" "memberships" {
  for_each = {
    for user in local.user_groups : "${user.id}_${user.group}" => user
  }

  group_id = okta_group.groups[each.value.group].id
  user_id  = okta_user.users[each.value.id].id
}

resource "okta_group_rule" "rules" {
  for_each = {
    for _, rule in local.rules : rule.id => rule
  }

  name             = each.value.name
  status           = each.value.status
  expression_type  = each.value.expression_type
  expression_value = each.value.expression_value

  group_assignments = [
    for group in local.groups : okta_group.groups[group.id].id
    if contains(group.rules, each.key)
  ]
}
