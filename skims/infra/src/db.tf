resource "aws_dynamodb_table" "sca_advisories" {
  name         = "sca_advisories"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "Advisory"
  range_key    = "PackageName"

  attribute {
    name = "Advisory"
    type = "S"
  }

  attribute {
    name = "PackageName"
    type = "S"
  }

  attribute {
    name = "PackageManager"
    type = "S"
  }

  attribute {
    name = "VulnerableVersion"
    type = "S"
  }

  attribute {
    name = "Severity"
    type = "S"
  }

  attribute {
    name = "Source"
    type = "S"
  }

  global_secondary_index {
    name            = "gsi_pm"
    hash_key        = "Source"
    range_key       = "PackageManager"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "gsi_severity"
    hash_key        = "Severity"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "gsi_version"
    hash_key        = "VulnerableVersion"
    projection_type = "ALL"
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
