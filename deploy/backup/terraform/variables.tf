data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

data "aws_iam_policy_document" "backup-assume-role-policy-data" {
  statement {
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type = "Service"
      identifiers = ["backup.amazonaws.com"]
    }
  }
}

variable "region" {
  default = "us-east-1"
}
