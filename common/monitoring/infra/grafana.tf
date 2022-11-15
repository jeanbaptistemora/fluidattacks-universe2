# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
