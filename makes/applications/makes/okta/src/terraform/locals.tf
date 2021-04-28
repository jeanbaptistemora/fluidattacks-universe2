locals {
  data   = jsondecode(var.okta_data)
  apps   = { for app in local.data.apps : app.id => app }
  groups = { for group in local.data.groups : group.id => group }
  rules  = { for rule in local.data.rules : rule.id => rule }
  users  = { for user in local.data.users : user.id => user }

  groups_rules = {
    for group in local.data.groups : group.id => group
    if group.type == "rules"
  }

  app_groups = flatten([
    for _, app in local.apps : [
      for _, group in local.groups : [
        {
          "id"    = app.id
          "type"  = app.type
          "group" = group.id
        }
      ] if contains(group.apps, app.id)
    ]
  ])

  aws_group_roles = flatten([
    for _, app in local.apps : [
      for _, group in local.groups : [
        {
          "id"    = app.id
          "group" = group.id
          "roles" = [for x in group.apps : split("/", x)[1] if length(regexall("/", x)) > 0]
        }
      ] if contains([for x in group.apps : split("/", x)[0] if length(regexall("/", x)) > 0], app.id)
    ]
  ])

  app_users = flatten([
    for _, app in local.apps : [
      for _, user in local.users : [
        {
          "id"   = app.id
          "type" = app.type
          "user" = user.id
        }
      ] if contains(user.apps, app.id)
    ]
  ])

  aws_user_roles = flatten([
    for _, app in local.apps : [
      for _, user in local.users : [
        {
          "id"    = app.id
          "user"  = user.id
          "roles" = [for x in user.apps : split("/", x)[1] if length(regexall("/", x)) > 0]
        }
      ] if contains([for x in user.apps : split("/", x)[0] if length(regexall("/", x)) > 0], app.id)
    ]
  ])
}
