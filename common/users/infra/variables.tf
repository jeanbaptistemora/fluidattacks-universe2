data "aws_caller_identity" "main" {}
data "cloudflare_api_token_permission_groups" "all" {}
data "aws_eks_cluster" "common" {
  name = "common"
}
variable "gitlab_token" {}
variable "gitlab_token_services" {}
variable "region" {
  default = "us-east-1"
}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}
