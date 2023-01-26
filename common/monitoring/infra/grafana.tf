resource "aws_grafana_workspace" "monitoring" {
  name                     = "monitoring"
  description              = "Fluid Attacks' Universe Monitoring"
  account_access_type      = "CURRENT_ACCOUNT"
  authentication_providers = ["SAML"]
  permission_type          = "CUSTOMER_MANAGED"
  role_arn                 = aws_iam_role.grafana.arn

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_grafana_workspace_saml_configuration" "monitoring" {
  workspace_id     = aws_grafana_workspace.monitoring.id
  idp_metadata_xml = okta_app_saml.grafana.metadata

  admin_role_values  = ["admin"]
  editor_role_values = ["editor"]

  name_assertion          = "displayName"
  email_assertion         = "mail"
  login_assertion         = "mail"
  role_assertion          = "role"
  login_validity_duration = 24 * 60 # 1 Day
}

resource "aws_grafana_workspace_api_key" "monitoring" {
  key_name        = "terraform"
  key_role        = "ADMIN"
  seconds_to_live = 2592000 # 30 Days
  workspace_id    = aws_grafana_workspace.monitoring.id
}

resource "grafana_folder" "monitoring" {
  uid   = "monitoring"
  title = "Monitoring"

  lifecycle {
    prevent_destroy = true
  }
}

data "grafana_dashboards" "monitoring" {}

data "grafana_dashboard" "monitoring" {
  for_each = toset([
    for dashboard in data.grafana_dashboards.monitoring.dashboards : dashboard.uid
  ])

  uid = each.value
}


resource "aws_s3_object" "grafana_backups" {
  for_each = data.grafana_dashboard.monitoring

  bucket  = aws_s3_bucket.monitoring.bucket
  key     = "grafana-backups/${each.value.id}.json"
  content = data.grafana_dashboard.monitoring[each.value.uid].config_json
}
