resource "aws_s3_bucket" "etl_data" {
  bucket = "observes.etl-data"

  tags = {
    "Name"               = "observes.etl-data"
    "Management:Area"    = "cost"
    "Management:Product" = "observes"
    "Management:Type"    = "product"
    "Access"             = "private"
  }
}

resource "aws_s3_bucket_acl" "etl_data" {
  bucket = aws_s3_bucket.etl_data.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "etl_data" {
  bucket = aws_s3_bucket.etl_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
