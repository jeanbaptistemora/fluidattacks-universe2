# Production
resource "aws_s3_bucket" "integrates" {
  bucket = "integrates"

  tags = {
    "Name"               = "integrates"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  acl = "private"
}

resource "aws_s3_bucket_logging" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  target_bucket = "common.logging"
  target_prefix = "log/integrates"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  rule {
    id     = "analytics"
    status = "Enabled"

    filter {
      prefix = "analytics/"
    }
    noncurrent_version_expiration {
      noncurrent_days = 14
    }
    expiration {
      days = 14
    }
  }
  rule {
    id     = "reports"
    status = "Enabled"

    filter {
      prefix = "reports/"
    }
    expiration {
      # 1 month + some timezone skews
      days = 32
    }
  }
}

resource "aws_s3_bucket_versioning" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["https://app.fluidattacks.com", "https://localhost:*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

# Development

resource "aws_s3_bucket" "storage_dev" {
  bucket = "integrates.dev"

  tags = {
    "Name"               = "integrates.dev"
    "management:area"    = "innovation"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "storage_dev" {
  bucket = aws_s3_bucket.storage_dev.id

  acl = "private"
}

resource "aws_s3_bucket_logging" "storage_dev" {
  bucket = aws_s3_bucket.storage_dev.id

  target_bucket = "common.logging"
  target_prefix = "log/integrates.dev"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "storage_dev" {
  bucket = aws_s3_bucket.storage_dev.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "storage_dev" {
  bucket = aws_s3_bucket.storage_dev.id

  rule {
    id     = "analytics"
    status = "Enabled"

    filter {
      prefix = "analytics/"
    }
    noncurrent_version_expiration {
      noncurrent_days = 14
    }
    expiration {
      days = 14
    }
  }
  rule {
    id     = "reports"
    status = "Enabled"

    filter {
      prefix = "reports/"
    }
    expiration {
      # 1 month + some timezone skews
      days = 32
    }
  }
}

resource "aws_s3_bucket_versioning" "storage_dev" {
  bucket = aws_s3_bucket.storage_dev.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "storage_dev" {
  bucket = aws_s3_bucket.storage_dev.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["https://*.app.fluidattacks.com", "https://localhost:*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}
