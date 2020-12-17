variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_email" {}
variable "cloudflare_api_token" {}

variable "region" {
  default = "us-east-1"
}

data "aws_route53_zone" "fluidattacks" {
  name = "fluidattacks.com."
}

data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}

variable "bucket_origin_id" {
  default = "production-bucket-origin"
}

variable "fluidattacks_root_certificate_arn" {
  default = "arn:aws:acm:us-east-1:205810638802:certificate/08dee275-d65f-4041-813c-5f9387f78116"
}
