resource "aws_s3_bucket" "observes_migration" {
  bucket = "observes.migration"

  tags = {
    "Name"               = "observes.migration"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "observes_migration" {
  bucket = aws_s3_bucket.observes_migration.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "observes_migration" {
  bucket = aws_s3_bucket.observes_migration.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
