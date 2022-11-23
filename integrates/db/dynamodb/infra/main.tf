variable "host" {}
variable "port" {}

terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
    }
  }
}

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
  billing_mode = "PAY_PER_REQUEST"

  global_secondary_index {
    name            = "gsi-1"
    hash_key        = "action_name"
    range_key       = "entity"
    projection_type = "ALL"
  }

  hash_key = "pk"
  name     = "fi_async_processing"
}

resource "aws_dynamodb_table" "integrates_vms" {
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
  billing_mode = "PAY_PER_REQUEST"
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

  hash_key  = "pk"
  name      = "integrates_vms"
  range_key = "sk"
}

resource "aws_dynamodb_table" "integrates_vms_consumer" {
  name         = "integrates_vms_consumer"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "leaseKey"

  attribute {
    name = "leaseKey"
    type = "S"
  }

  tags = {
    "Name"               = "integrates_vms_consumer"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_dynamodb_table" "skims_sca" {
  name         = "skims_sca"
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

  global_secondary_index {
    name            = "gsi_sk"
    hash_key        = "sk"
    range_key       = "pk"
    projection_type = "ALL"
  }
}
