resource "aws_iam_saml_provider" "main" {
  name                   = "vpn"
  saml_metadata_document = <<-EOL
    <?xml version="1.0" encoding="UTF-8"?><md:EntityDescriptor entityID="http://www.okta.com/exkgfc3nu8fRQs6Yn357" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"><md:IDPSSODescriptor WantAuthnRequestsSigned="false" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol"><md:KeyDescriptor use="signing"><ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:X509Data><ds:X509Certificate>MIIDqDCCApCgAwIBAgIGAW2yeIqDMA0GCSqGSIb3DQEBCwUAMIGUMQswCQYDVQQGEwJVUzETMBEG
    A1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsGA1UECgwET2t0YTEU
    MBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGZsdWlkYXR0YWNrczEcMBoGCSqGSIb3DQEJ
    ARYNaW5mb0Bva3RhLmNvbTAeFw0xOTEwMDkyMTQwNDdaFw0yOTEwMDkyMTQxNDdaMIGUMQswCQYD
    VQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsG
    A1UECgwET2t0YTEUMBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGZsdWlkYXR0YWNrczEc
    MBoGCSqGSIb3DQEJARYNaW5mb0Bva3RhLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
    ggEBAJZ2XfEX8jtFui4ll7MlUr8ByRQv2R3jaBcBliIh88JFO8PSscqeOCOAm083XO6CYW7FQnMf
    3ceDutnqIFbYemdILiUZXdD07yw+RwCN/WABs2gwpYLNR5ZEHnFrj0a6HMuzcN69l+UnLI6V9iDL
    Jcfz/+U9CoC0KCoW8+IKwrh2RIAMUIBLLBiQaF2kehFL6f+Pd8koa8mPzu3VQyaKDaXJf5GML7Vu
    Ew8MAxF2u8KgolH2MbbybkS4fqFJLDqzVT2RZXy9qUoII6qg0UqdX3do0yTRkLPhfNIIfABgkdre
    VyZXReUTYuLH+sWFq7G9REq45gA5wzNw4tynPyeerAECAwEAATANBgkqhkiG9w0BAQsFAAOCAQEA
    ULhbwMD6EOskawoayLezhPHeAtmzM8stYDaJdQWYzoirb2X+PM42zDVmCOiEQRYZxiUBnlmexPfZ
    Fd/p3ztmrhMCy/QqY901JaGvdUgtelPpVZ5uO9pXAhbY/rXK2jfZCWPu98oIxdWf4p8roTtIzdtw
    lVWI/jhY7rAHn95Vbjrh+OU7O7mTuyguVDXSXNkE3fSR7pp5YxFEw18Q2lJbduTtUDI/DxrXT+Yn
    J1ufkupsSdNt7VAVjA/sBE2qmnE9c4+uaWnR/nUYrRkLLRXRF7+Gdge5HqJ1H/XGPyt0RT9UaJsV
    5pBqdjpXGt+eZOKx4yze9tfx9rP+OUbzjZwBUw==</ds:X509Certificate></ds:X509Data></ds:KeyInfo></md:KeyDescriptor><md:NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</md:NameIDFormat><md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://fluidattacks.okta.com/app/aws_clientvpn/exkgfc3nu8fRQs6Yn357/sso/saml"/><md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://fluidattacks.okta.com/app/aws_clientvpn/exkgfc3nu8fRQs6Yn357/sso/saml"/></md:IDPSSODescriptor></md:EntityDescriptor>
  EOL

  tags = {
    "Name"               = "vpn"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "acm" {
  source  = "terraform-aws-modules/acm/aws"
  version = "~> 3.0"

  domain_name = "vpn.fluidattacks.com"
  zone_id     = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")

  create_route53_records  = false
  validation_record_fqdns = cloudflare_record.validation.*.hostname

  tags = {
    "Name"               = "vpn.fluidattacks.com"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

resource "cloudflare_record" "validation" {
  count = length(module.acm.distinct_domain_names)

  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = element(module.acm.validation_domains, count.index)["resource_record_name"]
  type    = element(module.acm.validation_domains, count.index)["resource_record_type"]
  value   = replace(element(module.acm.validation_domains, count.index)["resource_record_value"], "/.$/", "")
  ttl     = 60
  proxied = false

  allow_overwrite = true
}

resource "aws_cloudwatch_log_group" "main" {
  name = "vpn"

  tags = {
    "Name"               = "vpn"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

resource "aws_ec2_client_vpn_network_association" "main" {
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.main.id
  subnet_id              = data.aws_subnet.batch_clone.id
}

resource "aws_ec2_client_vpn_authorization_rule" "main" {
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.main.id
  target_network_cidr    = "0.0.0.0/0"
  authorize_all_groups   = true
}

resource "aws_ec2_client_vpn_route" "main" {
  for_each = toset(flatten([
    for _, client in local.vpnData : client.routes
  ]))

  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.main.id
  destination_cidr_block = each.key
  target_vpc_subnet_id   = aws_ec2_client_vpn_network_association.main.subnet_id

  timeouts {
    create = "10m"
    delete = "10m"
  }
}

resource "aws_ec2_client_vpn_endpoint" "main" {
  vpc_id                 = data.aws_vpc.main.id
  server_certificate_arn = module.acm.acm_certificate_arn
  client_cidr_block      = "10.0.0.0/22"
  session_timeout_hours  = 12
  split_tunnel           = true
  self_service_portal    = "enabled"

  authentication_options {
    type              = "federated-authentication"
    saml_provider_arn = aws_iam_saml_provider.main.arn
  }

  dns_servers = [
    aws_route53_resolver_endpoint.main.ip_address.*.ip[0],
    aws_route53_resolver_endpoint.main.ip_address.*.ip[1],
  ]

  connection_log_options {
    enabled              = true
    cloudwatch_log_group = aws_cloudwatch_log_group.main.name
  }

  tags = {
    "Name"               = "main"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}
