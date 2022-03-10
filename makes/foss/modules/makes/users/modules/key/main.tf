terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.4.0"
    }
  }
}

variable "name" {}
variable "admins" {}
variable "users" {}
variable "tags" {}

resource "aws_kms_key" "main" {
  policy                  = jsonencode(local.policy)
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = var.tags
}

resource "aws_kms_alias" "main" {
  name          = "alias/${var.name}"
  target_key_id = aws_kms_key.main.key_id
}

output "key" {
  value = aws_kms_key.main
}

output "alias" {
  value = aws_kms_alias.main
}
