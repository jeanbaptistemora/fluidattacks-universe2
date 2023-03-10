data "aws_caller_identity" "main" {}

variable "oktaApiToken" {}

locals {
  prometheus_role_name = "monitoring"
}
