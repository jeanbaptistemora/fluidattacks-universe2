resource "aws_dynamodb_table" "integrates_vms" {
  name             = "integrates_vms"
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "pk"
  range_key        = "sk"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

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
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}


resource "aws_dynamodb_table" "integrates_vms_consumer" {
  name         = "integrates_vms_consumer"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "leaseKey"

  attribute {
    name = "leaseKey"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "integrates_vms_consumer"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
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
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
