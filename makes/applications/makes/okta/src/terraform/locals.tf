locals {
  app_groups = flatten([
    for app in jsondecode(var.okta_apps) : [
      for group in jsondecode(var.okta_groups) : [
        {
          "id"    = app.id
          "type"  = app.type
          "group" = group.id
        }
      ]
    ]
  ])
}
