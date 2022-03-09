variable "bucket_name" {}
variable "evidences_bucket_name" {}
variable "reports_bucket_name" {}
variable "build_bucket_name" {}
variable "forces_bucket_name" {}

resource "aws_s3_bucket" "fi_resources_bucket" {
  bucket = var.bucket_name

  tags = {
    "Name"               = "fluidintegrates.resources"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "fi_resources_bucket" {
  bucket = aws_s3_bucket.fi_resources_bucket.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "fi_resources_bucket" {
  bucket = aws_s3_bucket.fi_resources_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "fi_resources_bucket" {
  bucket = aws_s3_bucket.fi_resources_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "fi_resources_bucket" {
  bucket = aws_s3_bucket.fi_resources_bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["https://app.fluidattacks.com", "https://localhost:*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket" "fi_evidences_bucket" {
  bucket = var.evidences_bucket_name

  tags = {
    "Name"               = "fluidintegrates.evidences"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "fi_evidences_bucket" {
  bucket = aws_s3_bucket.fi_evidences_bucket.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "fi_evidences_bucket" {
  bucket = aws_s3_bucket.fi_evidences_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "fi_evidences_bucket" {
  bucket = aws_s3_bucket.fi_evidences_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "fi_reports_bucket" {
  bucket = var.reports_bucket_name

  tags = {
    "Name"               = "fluidintegrates.reports"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "fi_reports_bucket" {
  bucket = aws_s3_bucket.fi_reports_bucket.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "fi_reports_bucket" {
  bucket = aws_s3_bucket.fi_reports_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "fi_reports_bucket" {
  bucket = aws_s3_bucket.fi_reports_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "fi_reports_bucket" {
  bucket = aws_s3_bucket.fi_reports_bucket.id

  rule {
    id     = "reports"
    status = "Enabled"
    expiration {
      # 1 month + some timezone skews
      days = 32
    }
  }
}

resource "aws_s3_bucket" "fi_build_bucket" {
  bucket = var.build_bucket_name

  tags = {
    "Name"               = "fluidintegrates.build"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "fi_build_bucket" {
  bucket = aws_s3_bucket.fi_build_bucket.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "fi_build_bucket" {
  bucket = aws_s3_bucket.fi_build_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "fi_build_bucket" {
  bucket = aws_s3_bucket.fi_build_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "fi_forces_bucket" {
  bucket = var.forces_bucket_name

  tags = {
    "Name"               = "fluidintegrates.forces"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "fi_forces_bucket" {
  bucket = aws_s3_bucket.fi_forces_bucket.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "fi_forces_bucket" {
  bucket = aws_s3_bucket.fi_forces_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "fi_forces_bucket" {
  bucket = aws_s3_bucket.fi_forces_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

output "fi_evidences_bucket_id" {
  value = aws_s3_bucket.fi_evidences_bucket.id
}

output "fi_evidences_bucket_arn" {
  value = aws_s3_bucket.fi_evidences_bucket.arn
}

output "fi_resources_bucket_id" {
  value = aws_s3_bucket.fi_resources_bucket.id
}

output "fi_resources_bucket_arn" {
  value = aws_s3_bucket.fi_resources_bucket.arn
}

output "fi_reports_bucket_id" {
  value = aws_s3_bucket.fi_reports_bucket.id
}

output "fi_reports_bucket_arn" {
  value = aws_s3_bucket.fi_reports_bucket.arn
}

output "fi_build_bucket_id" {
  value = aws_s3_bucket.fi_build_bucket.id
}

output "fi_build_bucket_arn" {
  value = aws_s3_bucket.fi_build_bucket.arn
}
