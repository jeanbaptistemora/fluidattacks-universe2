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

variable "dynamodb-tables" {
  default = [
    "fi_authz",
    "FI_comments",
    "fi_events",
    "FI_findings",
    "fi_portfolios",
    "FI_project_access",
    "fi_project_comments",
    "FI_projects",
    "FI_toe",
    "FI_users",
    "FI_vulnerabilities",
    "integrates"
  ]
}
