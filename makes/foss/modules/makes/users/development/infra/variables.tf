data "cloudflare_api_token_permission_groups" "all" {}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}
variable "gitlab_token" {}
