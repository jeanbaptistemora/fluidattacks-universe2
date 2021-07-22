variable "cloudflareAccountId" {}
variable "cloudflareApiToken" {}

data "aws_caller_identity" "current" {}
data "cloudflare_ip_ranges" "cloudflare" {}
data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}
