data "local_file" "headers" {
  filename = "js/headers.js"
}

data "local_file" "mta_sts" {
  filename = "js/mta-sts.js"
}

data "cloudflare_zone" "fluidattacks_com" {
  name = "fluidattacks.com"
}

variable "cloudflareAccountId" {}
variable "cloudflareApiKey" {}
variable "cloudflareEmail" {}
