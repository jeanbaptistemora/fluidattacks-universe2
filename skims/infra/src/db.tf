resource "aws_dynamodb_table" "sca_advisories" {
  name         = "sca_advisories"
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
    projection_type = "INCLUDE"
    non_key_attributes = [
      "associated_advisory",
      "package_name",
      "package_manager",
      "vulnerable_version",
      "severity",
      "source"
    ]
  }

  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "Name"               = "sca_advisories"
    "management:product" = "skims"
    "management:type"    = "product"
  }
}
