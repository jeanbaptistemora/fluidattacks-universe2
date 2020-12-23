variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_api_token" {}

data "cloudflare_ip_ranges" "cloudflare" {}
data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}

variable "region" {
  default = "us-east-1"
}
