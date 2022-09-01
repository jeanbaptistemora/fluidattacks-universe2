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

  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "skims_sca"
    "Management:Area"    = "cost"
    "Management:Product" = "skims"
    "Management:Type"    = "product"
  }
}
