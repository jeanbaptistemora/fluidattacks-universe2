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

resource "okta_group_rule" "groups_rules_rule" {
  for_each = {
    for _, rule in local.rules : rule.id => rule
  }

  name             = each.value.name
  status           = each.value.status
  expression_type  = each.value.expression_type
  expression_value = each.value.expression_value

  group_assignments = [
    for group in local.groups_rules : okta_group.groups_rules[group.id].id
    if contains(group.rules, each.key)
  ]
}
