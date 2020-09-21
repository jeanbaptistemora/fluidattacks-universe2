variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_email" {}
variable "cloudflare_api_key" {}
variable "elbDns" {}
variable "elbZone" {}

variable "s3-east-1-zone-id" {
  default = "Z3AQBSTGFYJSTF"
}
variable "domain" {
  default = "fluidattacks.com"
}
variable "region" {
  default = "us-east-1"
}
