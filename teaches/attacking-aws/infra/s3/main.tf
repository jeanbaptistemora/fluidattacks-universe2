resource "aws_s3_bucket" "ultra-secure-app-backup" {
  bucket = "ultra-secure-app-backup"
  acl    = "private"
  tags = {
    "Access" = "private"
  }

  versioning {
    enabled = false
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.ultra-secure-app-backup.id
  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "BUCKET-POLICY"
    Statement = [
      {
        Sid       = "EnforceTls"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          "${aws_s3_bucket.ultra-secure-app-backup.arn}/*",
          "${aws_s3_bucket.ultra-secure-app-backup.arn}",
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
          NumericLessThan = {
            "s3:TlsVersion" : 1.2
          }
        }
      },
    ]
  })
}
