resource "aws_dynamodb_table" "async_processing" {
  name         = "fi_async_processing"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"

  attribute {
    name = "pk"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "fi_async_processing"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "authz" {
  name         = "fi_authz"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "subject"
  range_key    = "object"

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

  tags = {
    "Name"               = "fi_authz"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "subscriptions" {
  name         = "fi_subscriptions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  range_key    = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  attribute {
    name = "pk_meta"
    type = "S"
  }

  attribute {
    name = "sk_meta"
    type = "S"
  }

  global_secondary_index {
    name            = "pk_meta"
    hash_key        = "pk_meta"
    range_key       = "sk_meta"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "sk_meta"
    hash_key        = "sk_meta"
    range_key       = "pk_meta"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "fi_subscriptions"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "project_comments" {
  name         = "fi_project_comments"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "project_name"
  range_key    = "user_id"

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

  tags = {
    "Name"               = "fi_project_comments"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "events" {
  name         = "fi_events"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "event_id"

  attribute {
    name = "event_id"
    type = "S"
  }

  attribute {
    name = "project_name"
    type = "S"
  }

  global_secondary_index {
    name            = "project_events"
    hash_key        = "project_name"
    projection_type = "KEYS_ONLY"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "fi_events"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "toe" {
  name         = "FI_toe"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "project"

  attribute {
    name = "project"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "FI_toe"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "projects" {
  name         = "FI_projects"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "project_name"

  attribute {
    name = "project_name"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "FI_projects"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "users" {
  name         = "FI_users"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "email"

  attribute {
    name = "email"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "FI_users"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "project_access" {
  name         = "FI_project_access"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_email"
  range_key    = "project_name"

  attribute {
    name = "user_email"
    type = "S"
  }

  attribute {
    name = "project_name"
    type = "S"
  }

  global_secondary_index {
    name            = "project_access_users"
    hash_key        = "project_name"
    projection_type = "INCLUDE"
    non_key_attributes = [
      "expiration_time",
      "responsibility",
      "has_access",
      "project_name"
    ]
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "FI_project_access"
    "management:type"    = "production"
    "management:product" = "integrates"
  }

  ttl {
    attribute_name = "expiration_time"
    enabled        = true
  }
}

resource "aws_dynamodb_table" "findings" {
  name         = "FI_findings"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "finding_id"

  attribute {
    name = "finding_id"
    type = "S"
  }

  attribute {
    name = "project_name"
    type = "S"
  }

  global_secondary_index {
    name            = "project_findings"
    hash_key        = "project_name"
    projection_type = "INCLUDE"
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

  tags = {
    "Name"               = "project_findings"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "finding_comments" {
  name         = "fi_finding_comments"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "finding_id"
  range_key    = "comment_id"

  attribute {
    name = "finding_id"
    type = "S"
  }

  attribute {
    name = "comment_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "fi_finding_comments"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "vulnerabilities" {
  name         = "FI_vulnerabilities"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "finding_id"
  range_key    = "UUID"

  attribute {
    name = "finding_id"
    type = "S"
  }

  attribute {
    name = "UUID"
    type = "S"
  }

  attribute {
    name = "repo_nickname"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  global_secondary_index {
    name            = "gsi_uuid"
    hash_key        = "UUID"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "repo_index"
    hash_key        = "repo_nickname"
    range_key       = "UUID"
    projection_type = "INCLUDE"
    non_key_attributes = [
      "historic_state",
      "historic_treatment",
      "historic_zero_risk"
    ]
  }

  tags = {
    "Name"               = "FI_vulnerabilities"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "portfolios" {
  name         = "fi_portfolios"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "organization"
  range_key    = "tag"

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

  tags = {
    "Name"               = "fi_portfolios"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "organizations" {
  name         = "fi_organizations"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  range_key    = "sk"

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
    name            = "gsi-1"
    hash_key        = "sk"
    range_key       = "pk"
    projection_type = "ALL"
  }

  tags = {
    "Name"               = "fi_organizations"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dynamodb_table" "forces" {
  name         = "FI_forces"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "subscription"
  range_key    = "execution_id"

  attribute {
    name = "execution_id"
    type = "S"
  }

  attribute {
    name = "subscription"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "FI_forces"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}
