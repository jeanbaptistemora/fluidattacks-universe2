variable "cloudflare_api_token" {}

data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}
data "cloudflare_ip_ranges" "cloudflare" {}
