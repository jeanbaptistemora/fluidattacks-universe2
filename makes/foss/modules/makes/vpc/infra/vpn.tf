resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.fluid-vpc.id

  tags = {
    "Name"               = "main"
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

resource "aws_ec2_client_vpn_endpoint" "main" {
  vpc_id                 = aws_vpc.fluid-vpc.id
  server_certificate_arn = module.acm.acm_certificate_arn
  client_cidr_block      = "10.0.0.0/22"
  session_timeout_hours  = 12

  authentication_options {
    type              = "federated-authentication"
    saml_provider_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:saml-provider/okta-saml-provider"
  }

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

module "vpn" {
  for_each = local.vpnData

  source          = "./modules/vpn"
  aws_cidr        = each.value.aws_cidr
  client_endpoint = each.value.client_endpoint
  client_name     = each.key
  routes          = each.value.routes
  vpn_gateway_id  = aws_vpn_gateway.main.id

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}
