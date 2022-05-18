# Analytics

resource "aws_s3_bucket" "analytics" {
  bucket = "fluidintegrates.analytics"

  tags = {
    "Name"               = "fluidintegrates.analytics"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "analytics" {
  bucket = aws_s3_bucket.analytics.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "analytics" {
  bucket = aws_s3_bucket.analytics.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_logging" "analytics" {
  bucket = aws_s3_bucket.analytics.id

  target_bucket = "common.logging"
  target_prefix = "log/analytics"
}

resource "aws_s3_bucket_versioning" "analytics" {
  bucket = aws_s3_bucket.analytics.id

  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Disabled"
  }
}

# Resources

resource "aws_s3_bucket" "resources" {
  bucket = "fluidintegrates.resources"

  tags = {
    "Name"               = "fluidintegrates.resources"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "resources" {
  bucket = aws_s3_bucket.resources.id

  acl = "private"
}

resource "aws_s3_bucket_logging" "resources" {
  bucket = aws_s3_bucket.resources.id

  target_bucket = "common.logging"
  target_prefix = "log/resources"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "resources" {
  bucket = aws_s3_bucket.resources.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "resources" {
  bucket = aws_s3_bucket.resources.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "resources" {
  bucket = aws_s3_bucket.resources.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["https://app.fluidattacks.com", "https://localhost:*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

# Evidences

resource "aws_s3_bucket" "evidences" {
  bucket = "fluidintegrates.evidences"

  tags = {
    "Name"               = "fluidintegrates.evidences"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "evidences" {
  bucket = aws_s3_bucket.evidences.id

  acl = "private"
}

resource "aws_s3_bucket_logging" "evidences" {
  bucket = aws_s3_bucket.evidences.id

  target_bucket = "common.logging"
  target_prefix = "log/evidences"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "evidences" {
  bucket = aws_s3_bucket.evidences.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "evidences" {
  bucket = aws_s3_bucket.evidences.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Reports

resource "aws_s3_bucket" "reports" {
  bucket = "fluidintegrates.reports"

  tags = {
    "Name"               = "fluidintegrates.reports"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "reports" {
  bucket = aws_s3_bucket.reports.id

  acl = "private"
}

resource "aws_s3_bucket_logging" "reports" {
  bucket = aws_s3_bucket.reports.id

  target_bucket = "common.logging"
  target_prefix = "log/reports"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "reports" {
  bucket = aws_s3_bucket.reports.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id

  rule {
    id     = "reports"
    status = "Enabled"
    expiration {
      # 1 month + some timezone skews
      days = 32
    }
  }
}

# Build

resource "aws_s3_bucket" "build" {
  bucket = "fluidintegrates.build"

  tags = {
    "Name"               = "fluidintegrates.build"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "build" {
  bucket = aws_s3_bucket.build.id

  acl = "private"
}

resource "aws_s3_bucket_logging" "build" {
  bucket = aws_s3_bucket.build.id

  target_bucket = "common.logging"
  target_prefix = "log/build"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "build" {
  bucket = aws_s3_bucket.build.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "build" {
  bucket = aws_s3_bucket.build.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Forces

resource "aws_s3_bucket" "forces" {
  bucket = "fluidintegrates.forces"

  tags = {
    "Name"               = "fluidintegrates.forces"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "forces" {
  bucket = aws_s3_bucket.forces.id

  acl = "private"
}

resource "aws_s3_bucket_logging" "forces" {
  bucket = aws_s3_bucket.forces.id

  target_bucket = "common.logging"
  target_prefix = "log/forces"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "forces" {
  bucket = aws_s3_bucket.forces.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "forces" {
  bucket = aws_s3_bucket.forces.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Continuous respositories

resource "aws_s3_bucket" "continuous_repositories" {
  bucket = "continuous-repositories"

  tags = {
    "Name"               = "continuous-repositories"
    "management:area"    = "cost"
    "management:product" = "services"
    "management:type"    = "service"
  }
}

resource "aws_s3_bucket_acl" "continuous_repositories" {
  bucket = aws_s3_bucket.continuous_repositories.id

  acl = "private"
}

resource "aws_s3_bucket_logging" "continuous_repositories" {
  bucket = aws_s3_bucket.continuous_repositories.id

  target_bucket = "continuous-repositories-logs"
  target_prefix = ""
}

resource "aws_s3_bucket_server_side_encryption_configuration" "continuous_repositories" {
  bucket = aws_s3_bucket.continuous_repositories.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "continuous_repositories" {
  bucket = aws_s3_bucket.continuous_repositories.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Continuous Data

resource "aws_s3_bucket" "continuous_data" {
  bucket = "continuous-data"

  tags = {
    "Name"               = "continuous-data"
    "management:area"    = "cost"
    "management:product" = "services"
    "management:type"    = "service"
  }
}

resource "aws_s3_bucket_acl" "continuous_data" {
  bucket = aws_s3_bucket.continuous_data.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "continuous_data" {
  bucket = aws_s3_bucket.continuous_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "continuous_data" {
  bucket = aws_s3_bucket.continuous_data.id

  versioning_configuration {
    status = "Enabled"
  }
}
