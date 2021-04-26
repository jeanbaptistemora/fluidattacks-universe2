locals {
  apps   = { for app in jsondecode(var.okta_apps) : app.id => app }
  groups = { for group in jsondecode(var.okta_groups) : group.id => group }
  users  = { for user in jsondecode(var.okta_users) : user.id => user }

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
