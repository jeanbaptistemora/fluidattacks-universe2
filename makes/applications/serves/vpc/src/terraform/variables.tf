variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_email" {}
variable "cloudflare_api_key" {}

data "aws_caller_identity" "current" {}
data "cloudflare_ip_ranges" "cloudflare" {}

variable "region" {
  default = "us-east-1"
}
