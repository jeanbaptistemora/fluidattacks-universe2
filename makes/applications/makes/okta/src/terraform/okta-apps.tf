# Auto login

resource "okta_app_auto_login" "apps" {
  for_each = {
    for _, app in local.apps : app.id => app
    if app.type == "auto_login"
  }

  label               = each.value.label
  status              = each.value.status
  preconfigured_app   = each.value.preconfigured_app
  credentials_scheme  = each.value.credentials_scheme
  shared_username     = each.value.shared_username
  shared_password     = each.value.shared_password
  sign_on_url         = each.value.sign_on_url
  auto_submit_toolbar = true

  groups = [
    for app_group in local.app_groups : okta_group.groups[app_group.group].id
    if app_group.id == each.value.id
  ]

  lifecycle {
    ignore_changes = [
      users,
    ]
  }
}

resource "okta_app_user" "apps_auto_login" {
  for_each = {
    for app in local.app_users : "${app.id}_${app.user}" => app
    if app.type == "auto_login"
  }

  app_id   = okta_app_auto_login.apps[each.value.id].id
  user_id  = okta_user.users[each.value.user].id
  username = ""
}


# SWA

resource "okta_app_swa" "apps" {
  for_each = {
    for _, app in local.apps : app.id => app
    if app.type == "swa"
  }

  label               = each.value.label
  status              = each.value.status
  preconfigured_app   = each.value.preconfigured_app
  button_field        = each.value.button_field
  username_field      = each.value.username_field
  password_field      = each.value.password_field
  url                 = each.value.url
  auto_submit_toolbar = true

  groups = [
    for app_group in local.app_groups : okta_group.groups[app_group.group].id
    if app_group.id == each.value.id
  ]

  lifecycle {
    ignore_changes = [
      users,
    ]
  }
}

resource "okta_app_user" "apps_swa" {
  for_each = {
    for app in local.app_users : "${app.id}_${app.user}" => app
    if app.type == "swa"
  }

  app_id   = okta_app_swa.apps[each.value.id].id
  user_id  = okta_user.users[each.value.user].id
  username = ""
}


# SAML

resource "okta_app_saml" "apps" {
  for_each = {
    for _, app in local.apps : app.id => app
    if app.type == "saml"
  }

  label                    = each.value.label
  preconfigured_app        = each.value.preconfigured_app
  sso_url                  = each.value.sso_url
  recipient                = each.value.recipient
  destination              = each.value.destination
  audience                 = each.value.audience
  subject_name_id_template = each.value.subject_name_id_template
  subject_name_id_format   = each.value.subject_name_id_format
  signature_algorithm      = each.value.signature_algorithm
  digest_algorithm         = each.value.digest_algorithm
  authn_context_class_ref  = each.value.authn_context_class_ref
  response_signed          = each.value.response_signed
  assertion_signed         = each.value.assertion_signed
  status                   = each.value.status
  user_name_template       = each.value.user_name_template
  user_name_template_type  = each.value.user_name_template_type
  app_settings_json        = jsonencode(each.value.app_settings_json)
  auto_submit_toolbar      = true

  lifecycle {
    ignore_changes = [
      groups,
      users,
    ]
  }
}

resource "okta_app_group_assignment" "apps_saml" {
  for_each = {
    for app in local.app_groups : "${app.id}_${app.group}" => app
    if app.type == "saml"
  }

  app_id   = okta_app_saml.apps[each.value.id].id
  group_id = okta_group.groups[each.value.group].id

  lifecycle {
    ignore_changes = [
      priority,
    ]
  }
}

resource "okta_app_user" "apps_saml" {
  for_each = {
    for app in local.app_users : "${app.id}_${app.user}" => app
    if app.type == "saml"
  }

  app_id  = okta_app_saml.apps[each.value.id].id
  user_id = okta_user.users[each.value.user].id
  username = (
    local.apps[each.value.id].single_user == null
    ) ? (
    okta_user.users[each.value.user].login
    ) : (
    local.apps[each.value.id].single_user
  )
}

resource "okta_app_group_assignment" "aws" {
  for_each = {
    for app in local.aws_group_roles : "${app.id}_${app.group}" => app
  }

  app_id   = okta_app_saml.apps[each.value.id].id
  group_id = okta_group.groups[each.value.group].id

  profile = jsonencode({
    samlRoles = each.value.roles
    role      = "AmazonComprehendServiceRole-testttt"
  })

  lifecycle {
    ignore_changes = [
      priority,
    ]
  }
}

resource "okta_app_user" "aws" {
  for_each = {
    for app in local.aws_user_roles : "${app.id}_${app.user}" => app
  }

  app_id   = okta_app_saml.apps[each.value.id].id
  user_id  = okta_user.users[each.value.user].id
  username = okta_user.users[each.value.user].login

  profile = jsonencode({
    email        = okta_user.users[each.value.user].email
    samlRoles    = each.value.roles
    firstName    = okta_user.users[each.value.user].first_name
    lastName     = okta_user.users[each.value.user].last_name
    role         = "AmazonComprehendServiceRole-testttt"
    idpRolePairs = []
  })
}
