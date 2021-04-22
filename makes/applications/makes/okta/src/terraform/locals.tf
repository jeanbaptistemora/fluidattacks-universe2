locals {
  app_groups = flatten([
    for app in jsondecode(var.okta_apps) : [
      for group in jsondecode(var.okta_groups) : [
        {
          "id"    = app.id
          "type"  = app.type
          "group" = group.id
        }
      ] if contains(group.apps, app.id)
    ]
  ])
  app_users = flatten([
    for app in jsondecode(var.okta_apps) : [
      for user in jsondecode(var.okta_users) : [
        {
          "id"   = app.id
          "type" = app.type
          "user" = user.id
        }
      ] if contains(user.apps, app.id)
    ]
  ])
}
