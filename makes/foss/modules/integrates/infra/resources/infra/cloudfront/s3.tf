variable "bucket_name" {}
variable "evidences_bucket_name" {}
variable "reports_bucket_name" {}
variable "build_bucket_name" {}
variable "forces_bucket_name" {}

resource "aws_s3_bucket" "fi_resources_bucket" {
  bucket = var.bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["https://app.fluidattacks.com", "https://localhost:*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    "Name"               = "fluidintegrates.resources"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket" "fi_evidences_bucket" {
  bucket = var.evidences_bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    "Name"               = "fluidintegrates.evidences"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket" "fi_reports_bucket" {
  bucket = var.reports_bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    id      = "reports"
    enabled = true
    expiration {
      # 1 month + some timezone skews
      days = 32
    }
  }

  tags = {
    "Name"               = "fluidintegrates.reports"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket" "fi_build_bucket" {
  bucket = var.build_bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    "Name"               = "fluidintegrates.build"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket" "fi_forces_bucket" {
  bucket = var.forces_bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    "Name"               = "fluidintegrates.forces"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
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
