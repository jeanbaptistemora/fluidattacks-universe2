variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_email" {}
variable "cloudflare_api_token" {}

data "aws_route53_zone" "fluidattacks" {
  name = "fluidattacks.com."
}

data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}

variable bucket-origin-id {
  default = "web-ephemeral-bucket-origin"
}

variable "region" {
  default = "us-east-1"
}
