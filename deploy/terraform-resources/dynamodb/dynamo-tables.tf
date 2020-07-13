resource "aws_dynamodb_table" "alerts_by_company" {
  name           = "FI_alerts_by_company"
  billing_mode   = "PAY_PER_REQUEST"
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

resource "aws_dynamodb_table" "authz" {
  name          = "fi_authz"
  billing_mode  = "PAY_PER_REQUEST"
  hash_key      = "subject"
  range_key     = "object"

  attribute {
    name = "subject"
    type = "S"
  }
  attribute {
    name = "object"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "subscriptions" {
  name          = "fi_subscriptions"
  billing_mode  = "PAY_PER_REQUEST"
  hash_key      = "pk"
  range_key     = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
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

  lifecycle {
    ignore_changes = [
      read_capacity,
      write_capacity
    ]
  }
}

resource "aws_dynamodb_table" "project_comments" {
  name           = "fi_project_comments"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "project_name"
  range_key      = "user_id"

  attribute {
    name = "project_name"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "N"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "events" {
  name           = "fi_events"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "event_id"

  attribute {
    name = "event_id"
    type = "S"
  }

  attribute {
    name = "project_name"
    type = "S"
  }

  global_secondary_index {
    name               = "project_events"
    hash_key           = "project_name"
    projection_type    = "KEYS_ONLY"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "toe" {
  name           = "FI_toe"
  billing_mode   = "PAY_PER_REQUEST"
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
  billing_mode   = "PAY_PER_REQUEST"
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
  billing_mode   = "PAY_PER_REQUEST"
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
  billing_mode   = "PAY_PER_REQUEST"
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
  billing_mode   = "PAY_PER_REQUEST"
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

  global_secondary_index {
    name               = "project_access_users"
    hash_key           = "project_name"
    projection_type    = "INCLUDE"
    non_key_attributes = [
      "responsibility",
      "has_access",
      "project_name"
    ]
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "findings" {
  name           = "FI_findings"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "finding_id"

  attribute {
    name = "finding_id"
    type = "S"
  }

  attribute {
    name = "project_name"
    type = "S"
  }

  global_secondary_index {
    name               = "project_findings"
    hash_key           = "project_name"
    projection_type    = "INCLUDE"
    non_key_attributes = [
      "historic_treatment",
      "historic_verification",
      "cvss_temporal",
      "historic_state",
      "releaseDate",
      "finding"
    ]
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "vulnerabilities" {
  name           = "FI_vulnerabilities"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "finding_id"
  range_key      = "UUID"

  attribute {
    name = "finding_id"
    type = "S"
  }

  attribute {
    name = "UUID"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "portfolios" {
  name           = "fi_portfolios"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "organization"
  range_key      = "tag"

  attribute {
    name = "organization"
    type = "S"
  }

  attribute {
    name = "tag"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "organizations" {
  name = "fi_organizations"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "pk"
  range_key = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  global_secondary_index {
    name = "gsi-1"
    hash_key =  "sk"
    range_key = "pk"
    projection_type = "ALL"
  }
}
