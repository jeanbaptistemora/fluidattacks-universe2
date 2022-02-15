variable "cloudflare_email" {}
variable "cloudflare_api_key" {}
variable "vpnDataRaw" {}

data "aws_caller_identity" "current" {}
data "cloudflare_ip_ranges" "cloudflare" {}

locals {
  vpnData = {
    for client in jsondecode(var.vpnDataRaw) : client.id => client
  }
}
