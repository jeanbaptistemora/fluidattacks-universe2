resource "okta_domain" "main" {
  name = "iam.fluidattacks.tech"
}

resource "okta_domain_verification" "main" {
  domain_id = okta_domain.main.id
}
