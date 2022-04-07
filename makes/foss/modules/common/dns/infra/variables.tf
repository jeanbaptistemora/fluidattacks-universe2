locals {
  product         = "https://gitlab.com/fluidattacks/product"
  product_archive = "${local.product}/-/archive/master.tar.gz"
  product_raw     = "${local.product}/-/raw/master"
}

data "local_file" "headers" {
  filename = "js/headers.js"
}

variable "cloudflareApiKey" {}
variable "cloudflareEmail" {}
