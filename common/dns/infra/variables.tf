data "local_file" "headers" {
  filename = "js/headers.js"
}

data "local_file" "mta_sts" {
  filename = "js/mta-sts.js"
}

variable "cloudflareAccountId" {}
variable "cloudflareApiKey" {}
variable "cloudflareEmail" {}
