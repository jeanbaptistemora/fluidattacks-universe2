locals {
  product         = "https://gitlab.com/fluidattacks/product"
  product_archive = "${local.product}/-/archive/master.tar.gz"
  product_raw     = "${local.product}/-/raw/master"
}

variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_email" {}
variable "cloudflare_api_key" {}

variable "region" {
  default = "us-east-1"
}
