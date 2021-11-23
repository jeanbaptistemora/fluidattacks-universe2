data "aws_caller_identity" "current" {}
variable "gitlab_token" {}
variable "gitlab_token_services" {}
variable "region" {}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}
