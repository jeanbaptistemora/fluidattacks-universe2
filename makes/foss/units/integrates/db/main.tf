variable "host" {}
variable "port" {}

provider "aws" {
  endpoints {
    dynamodb = "http://${var.host}:${var.port}"
  }
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
}

resource "aws_dynamodb_table" "fi_async_processing" {
  attribute {
    name = "pk"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  name         = "fi_async_processing"
}

resource "aws_dynamodb_table" "fi_authz" {
  attribute {
    name = "subject"
    type = "S"
  }
  attribute {
    name = "object"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "subject"
  name         = "fi_authz"
  range_key    = "object"
}

resource "aws_dynamodb_table" "fi_events" {
  attribute {
    name = "event_id"
    type = "S"
  }
  attribute {
    name = "project_name"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  global_secondary_index {
    hash_key        = "project_name"
    name            = "project_events"
    projection_type = "KEYS_ONLY"
  }
  hash_key = "event_id"
  name     = "fi_events"
}

resource "aws_dynamodb_table" "FI_findings" {
  attribute {
    name = "finding_id"
    type = "S"
  }
  attribute {
    name = "project_name"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  global_secondary_index {
    hash_key = "project_name"
    name     = "project_findings"
    non_key_attributes = [
      "cvss_temporal",
      "finding",
      "historic_state",
      "historic_verification",
      "historic_treatment",
    ]
    projection_type = "INCLUDE"
  }
  hash_key = "finding_id"
  name     = "FI_findings"
}

resource "aws_dynamodb_table" "fi_finding_comments" {
  attribute {
    name = "finding_id"
    type = "S"
  }
  attribute {
    name = "comment_id"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "finding_id"
  name         = "fi_finding_comments"
  range_key    = "comment_id"
}

resource "aws_dynamodb_table" "FI_forces" {
  attribute {
    name = "subscription"
    type = "S"
  }
  attribute {
    name = "execution_id"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "subscription"
  name         = "FI_forces"
  range_key    = "execution_id"
}

resource "aws_dynamodb_table" "fi_organizations" {
  attribute {
    name = "pk"
    type = "S"
  }
  attribute {
    name = "sk"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  global_secondary_index {
    hash_key        = "sk"
    name            = "gsi-1"
    projection_type = "ALL"
    range_key       = "pk"
  }
  hash_key  = "pk"
  name      = "fi_organizations"
  range_key = "sk"
}

resource "aws_dynamodb_table" "fi_portfolios" {
  attribute {
    name = "organization"
    type = "S"
  }
  attribute {
    name = "tag"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "organization"
  name         = "fi_portfolios"
  range_key    = "tag"
}

resource "aws_dynamodb_table" "FI_project_access" {
  attribute {
    name = "user_email"
    type = "S"
  }
  attribute {
    name = "project_name"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  global_secondary_index {
    hash_key = "project_name"
    name     = "project_access_users"
    non_key_attributes = [
      "expiration_time",
      "has_access",
      "responsibility",
    ]
    projection_type = "INCLUDE"
  }
  hash_key  = "user_email"
  name      = "FI_project_access"
  range_key = "project_name"
  ttl {
    attribute_name = "expiration_time"
    enabled        = true
  }
}

resource "aws_dynamodb_table" "fi_project_comments" {
  attribute {
    name = "project_name"
    type = "S"
  }
  attribute {
    name = "user_id"
    type = "N"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "project_name"
  name         = "fi_project_comments"
  range_key    = "user_id"
}

resource "aws_dynamodb_table" "FI_projects" {
  attribute {
    name = "project_name"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "project_name"
  name         = "FI_projects"
}

resource "aws_dynamodb_table" "fi_subscriptions" {
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
  billing_mode = "PAY_PER_REQUEST"
  global_secondary_index {
    hash_key        = "pk_meta"
    name            = "pk_meta"
    projection_type = "ALL"
    range_key       = "sk_meta"
  }
  global_secondary_index {
    hash_key        = "sk_meta"
    name            = "sk_meta"
    projection_type = "ALL"
    range_key       = "pk_meta"
  }
  hash_key  = "pk"
  name      = "fi_subscriptions"
  range_key = "sk"
}

resource "aws_dynamodb_table" "FI_toe" {
  attribute {
    name = "project"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "project"
  name         = "FI_toe"
}

resource "aws_dynamodb_table" "FI_users" {
  attribute {
    name = "email"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "email"
  name         = "FI_users"
}

resource "aws_dynamodb_table" "FI_vulnerabilities" {
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
  billing_mode = "PAY_PER_REQUEST"
  global_secondary_index {
    hash_key        = "UUID"
    name            = "gsi_uuid"
    projection_type = "ALL"
  }
  global_secondary_index {
    name            = "repo_index"
    hash_key        = "repo_nickname"
    range_key       = "UUID"
    projection_type = "ALL"
  }
  hash_key  = "finding_id"
  name      = "FI_vulnerabilities"
  range_key = "UUID"
}

resource "aws_dynamodb_table" "integrates" {
  attribute {
    name = "pk"
    type = "S"
  }
  attribute {
    name = "sk"
    type = "S"
  }
  attribute {
    name = "gsi-2-pk"
    type = "S"
  }
  attribute {
    name = "gsi-2-sk"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  global_secondary_index {
    hash_key        = "sk"
    name            = "gsi-1"
    projection_type = "ALL"
    range_key       = "pk"
  }
  global_secondary_index {
    hash_key        = "gsi-2-pk"
    name            = "gsi-2"
    projection_type = "ALL"
    range_key       = "gsi-2-sk"
  }
  hash_key  = "pk"
  name      = "integrates"
  range_key = "sk"
}


resource "aws_dynamodb_table" "integrates_vms" {
  attribute {
    name = "pk"
    type = "S"
  }
  attribute {
    name = "sk"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  global_secondary_index {
    name            = "inverted_index"
    hash_key        = "sk"
    range_key       = "pk"
    projection_type = "ALL"
  }
  hash_key  = "pk"
  name      = "integrates_vms"
  range_key = "sk"
}
