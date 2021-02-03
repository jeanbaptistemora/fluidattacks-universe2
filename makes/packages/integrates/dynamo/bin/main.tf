provider "aws" {
  endpoints {
    dynamodb = "http://127.0.0.1:8022"
  }
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
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

resource "aws_dynamodb_table" "FI_comments" {
  attribute {
    name = "finding_id"
    type = "S"
  }
  attribute {
    name = "user_id"
    type = "S"
  }
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "finding_id"
  name         = "FI_comments"
  range_key    = "user_id"
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
  hash_key  = "event_id"
  name      = "fi_events"
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
    hash_key        = "project_name"
    name            = "project_findings"
    non_key_attributes = [
      "cvss_temporal",
      "finding",
      "historic_state",
      "historic_verification",
      "historic_treatment",
    ]
    projection_type = "INCLUDE"
  }
  hash_key  = "finding_id"
  name      = "FI_findings"
  range_key = "project_name"
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
