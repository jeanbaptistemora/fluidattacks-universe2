resource "okta_app_saml" "grafana" {
  label             = "Grafana - Universe"
  preconfigured_app = "amazonmanagedgrafanasaml"

  app_settings_json = jsonencode({
    "nameSpace" = "g-41cb062f0f"
    "region"    = "us-east-1"
  })
  app_links_json = jsonencode({
    "amazonmanagedgrafanasaml_link" = true,
  })
  user_name_template      = "$${source.login}"
  user_name_template_type = "BUILT_IN"

  attribute_statements {
    type   = "EXPRESSION"
    name   = "role"
    values = ["admin"]
  }

  lifecycle {
    ignore_changes = [users]
  }
}

resource "okta_app_user" "grafana_user_1" {
  app_id   = okta_app_saml.grafana.id
  user_id  = "00u3fmne3smuCPHVt357"
  username = "acuberos@fluidattacks.com"
}

resource "okta_app_user" "grafana_user_2" {
  app_id   = okta_app_saml.grafana.id
  user_id  = "00u1l65axaSd0IMke357"
  username = "jrestrepo@fluidattacks.com"
}

resource "okta_app_user" "grafana_user_3" {
  app_id   = okta_app_saml.grafana.id
  user_id  = "00u1la30aoz6g8iyD357"
  username = "dacevedo@fluidattacks.com"
}
