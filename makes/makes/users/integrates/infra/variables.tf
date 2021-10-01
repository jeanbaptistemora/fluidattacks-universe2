data "aws_caller_identity" "current" {}
data "cloudflare_api_token_permission_groups" "all" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_email" {}
variable "cloudflare_api_key" {}
variable "gitlab_token" {}
variable "gitlab_token_services" {}

variable "region" {
  default = "us-east-1"
}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}
