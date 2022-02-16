resource "aws_dynamodb_table" "basic-dynamodb-table" {
  server_side_encryption {
    enabled     = false
    kms_key_arn = aws_kms_key.dynamo.arn
  }
}
