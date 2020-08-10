data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

/**
 * Terraform only supports us-west-2 for device-farm
 * https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/devicefarm_project
 */
variable "region" {
  default = "us-west-2"
}
