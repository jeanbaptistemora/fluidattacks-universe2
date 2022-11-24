variable "cloudflare_email" {}
variable "cloudflare_api_key" {}

data "cloudflare_ip_ranges" "cloudflare" {}
