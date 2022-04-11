data "local_file" "headers" {
  filename = "js/headers.js"
}

variable "cloudflareApiKey" {}
variable "cloudflareEmail" {}
