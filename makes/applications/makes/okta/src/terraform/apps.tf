resource "okta_app_auto_login" "apps" {
  for_each = {
    for app in jsondecode(var.okta_apps) : app.id => app
    if app.type == "auto_login"
  }

  label               = each.value.label
  status              = each.value.status
  preconfigured_app   = each.value.preconfigured_app
  credentials_scheme  = each.value.credentials_scheme
  shared_username     = each.value.shared_username
  shared_password     = each.value.shared_password
  auto_submit_toolbar = true

  lifecycle {
    ignore_changes = [groups]
  }
}

resource "okta_app_group_assignment" "apps_auto_login" {
  for_each = {
    for app in local.app_groups : app.id => app.group
    if app.type == "auto_login"
  }

  app_id   = okta_app_auto_login.apps[each.key].id
  group_id = okta_group.groups[each.value].id
}

resource "okta_app_user" "apps_auto_login" {
  for_each = {
    for app in local.app_users : app.id => app.user
    if app.type == "auto_login"
  }

  app_id   = okta_app_auto_login.apps[each.key].id
  user_id  = okta_user.users[each.value].id
  username = ""
}
