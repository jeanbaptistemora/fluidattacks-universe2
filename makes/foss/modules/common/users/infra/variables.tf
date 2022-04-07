data "aws_caller_identity" "current" {}
data "cloudflare_api_token_permission_groups" "all" {}
variable "gitlab_token" {}
variable "gitlab_token_services" {}
variable "region" {}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}
