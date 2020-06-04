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

  global_secondary_index {
    name               = "gsi-1"
    hash_key           = "sk"
    range_key          = "pk"
    projection_type    = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }
}
