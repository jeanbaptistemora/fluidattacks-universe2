# AWS vars
variable "dynamo_access_key" {}
variable "dynamo_secret_key" {}
variable "region" {}

provider "aws" {
  access_key = "${var.dynamo_access_key}"
  secret_key = "${var.dynamo_secret_key}"
  region = "${var.region}"
}

resource "aws_dynamodb_table" "alerts_by_company" {
  name           = "FI_alerts_by_company"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "company_name"
  range_key      = "project_name"

  attribute {
    name = "company_name"
    type = "S"
  }

  attribute {
    name = "project_name"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "comments" {
  name           = "FI_comments"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "finding_id"
  range_key      = "user_id"

  attribute {
    name = "finding_id"
    type = "N"
  }

  attribute {
    name = "user_id"
    type = "N"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "findings_email" {
  name           = "FI_findings_email"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "project_name"
  range_key      = "unique_id"

  attribute {
    name = "project_name"
    type = "S"
  }

  attribute {
    name = "unique_id"
    type = "N"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "remediated" {
  name           = "FI_remediated"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "finding_id"

  attribute {
    name = "finding_id"
    type = "N"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "toe" {
  name           = "FI_toe"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "project"

  attribute {
    name = "project"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "weekly_report" {
  name           = "FI_weekly_report"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "init_date"

  attribute {
    name = "init_date"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
resource "aws_dynamodb_table" "projects" {
  name           = "FI_projects"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "project_name"

  attribute {
    name = "project_name"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
resource "aws_dynamodb_table" "users" {
  name           = "FI_users"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
resource "aws_dynamodb_table" "project_access" {
  name           = "FI_project_access"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "user_email"
  range_key      = "project_name"

  attribute {
    name = "user_email"
    type = "S"
  }

  attribute {
    name = "project_name"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
resource "aws_dynamodb_table" "findings_new" {
  name           = "FI_findings_new"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "finding_id"

  attribute {
    name = "finding_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "findings" {
  name           = "FI_findings"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "finding_id"

  attribute {
    name = "finding_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}