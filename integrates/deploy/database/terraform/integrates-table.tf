resource "aws_dynamodb_table" "integrates" {
  name           = "integrates"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "pk"
  range_key      = "sk"

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
    name               = "gsi-1"
    hash_key           = "sk"
    range_key          = "pk"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "gsi-2"
    hash_key           = "gsi-2-pk"
    range_key          = "gsi-2-sk"
    projection_type    = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "fi_roots" {
  name           = "fi_roots"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "pk"
  range_key      = "sk"

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
