data "local_file" "headers" {
  filename = "js/headers.js"
}

variable "cloudflareAccountId" {}
variable "cloudflareApiKey" {}
variable "cloudflareEmail" {}
