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
    "FI_alerts_by_company",
    "FI_comments",
    "fi_events",
    "FI_findings",
    "FI_project_access",
    "fi_project_comments",
    "fi_project_names",
    "FI_projects",
    "FI_toe",
    "FI_users",
    "FI_vulnerabilities",
    "FI_weekly_report",
  ]
}
