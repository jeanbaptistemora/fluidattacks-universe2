variable "cloudflare_email" {}
variable "cloudflare_api_key" {}
variable "vpnDataRaw" {}

data "cloudflare_ip_ranges" "cloudflare" {}
data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}

locals {
  vpnData = {
    for client in jsondecode(var.vpnDataRaw) : client.id => client
  }
}
