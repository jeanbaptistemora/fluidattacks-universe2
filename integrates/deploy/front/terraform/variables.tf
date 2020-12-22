variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_api_token" {}

data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}
data "cloudflare_ip_ranges" "cloudflare" {}
data "aws_route53_zone" "fluidattacks" {
  name = "fluidattacks.com."
}

variable "region" {
  default = "us-east-1"
}
variable bucket-origin-id-development {
  default = "integrates.front.development.origin"
}
variable bucket-origin-id-production {
  default = "integrates.front.production.origin"
}
