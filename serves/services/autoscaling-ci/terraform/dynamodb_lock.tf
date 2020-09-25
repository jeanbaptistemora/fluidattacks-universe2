resource "aws_dynamodb_table" "terraform_state_lock" {
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  name         = "terraform_state_lock"

  attribute {
    name = "LockID"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    "management:type"    = "production"
    "management:product" = "serves"
  }
}
