# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    "Name"               = "terraform_state_lock"
    "Management:Area"    = "innovation"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}
