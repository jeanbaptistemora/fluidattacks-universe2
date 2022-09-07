# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_dynamodb_table" "integrates" {
  name         = "integrates"
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
    name = "gsi-2-pk"
    type = "S"
  }

  attribute {
    name = "gsi-2-sk"
    type = "S"
  }

  global_secondary_index {
    name            = "gsi-1"
    hash_key        = "sk"
    range_key       = "pk"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "gsi-2"
    hash_key        = "gsi-2-pk"
    range_key       = "gsi-2-sk"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "integrates"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }
}

resource "aws_dynamodb_table" "integrates_vms" {
  name             = "integrates_vms"
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "pk"
  range_key        = "sk"
  stream_enabled   = true
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  attribute {
    name = "pk_2"
    type = "S"
  }

  attribute {
    name = "sk_2"
    type = "S"
  }

  attribute {
    name = "pk_3"
    type = "S"
  }

  attribute {
    name = "sk_3"
    type = "S"
  }

  attribute {
    name = "pk_4"
    type = "S"
  }

  attribute {
    name = "sk_4"
    type = "S"
  }

  attribute {
    name = "pk_5"
    type = "S"
  }

  attribute {
    name = "sk_5"
    type = "S"
  }

  attribute {
    name = "pk_6"
    type = "S"
  }

  attribute {
    name = "sk_6"
    type = "S"
  }

  global_secondary_index {
    name            = "inverted_index"
    hash_key        = "sk"
    range_key       = "pk"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "gsi_2"
    hash_key        = "pk_2"
    range_key       = "sk_2"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "gsi_3"
    hash_key        = "pk_3"
    range_key       = "sk_3"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "gsi_4"
    hash_key        = "pk_4"
    range_key       = "sk_4"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "gsi_5"
    hash_key        = "pk_5"
    range_key       = "sk_5"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "gsi_6"
    hash_key        = "pk_6"
    range_key       = "sk_6"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "integrates_vms"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }
}

resource "aws_dynamodb_table" "async_processing" {
  name         = "fi_async_processing"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"

  attribute {
    name = "action_name"
    type = "S"
  }
  attribute {
    name = "entity"
    type = "S"
  }
  attribute {
    name = "pk"
    type = "S"
  }

  global_secondary_index {
    name            = "gsi-1"
    hash_key        = "action_name"
    range_key       = "entity"
    projection_type = "ALL"
  }


  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }
  tags = {
    "Name"               = "fi_async_processing"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "fi_authz"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "fi_subscriptions"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "fi_project_comments"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "fi_events"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "FI_projects"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "FI_users"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "FI_project_access"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "project_findings"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "fi_finding_comments"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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
    projection_type = "ALL"
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "FI_vulnerabilities"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "fi_portfolios"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "fi_organizations"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
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

  attribute {
    name = "date"
    type = "S"
  }

  global_secondary_index {
    name            = "date"
    hash_key        = "subscription"
    range_key       = "date"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "FI_forces"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }
}
