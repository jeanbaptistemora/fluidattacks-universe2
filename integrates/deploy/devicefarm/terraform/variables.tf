data "aws_caller_identity" "current" {}

/**
 * Device farm currently only supports us-west-2
 * https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/
 */
variable "region" {
  default = "us-west-2"
}
variable "aws_access_key" {}
variable "aws_secret_key" {}
