data "aws_caller_identity" "current" {}
data "cloudflare_api_token_permission_groups" "all" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_email" {}
variable "cloudflare_api_key" {}

data "aws_route53_zone" "fluidattacks" {
  name = "fluidattacks.com."
}
variable "region" {
  default = "us-east-1"
}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}
