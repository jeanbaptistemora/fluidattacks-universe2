# Production

resource "aws_s3_bucket" "bucket_prod" {
  bucket = "doc.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  website {
    index_document = "index.html"
    error_document = "404.html"
  }

  tags = {
    "Name"               = "doc.fluidattacks.com"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

data "aws_iam_policy_document" "bucket_prod_policy" {
  statement {
    sid    = "CloudFlare"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.bucket_prod.arn}/*",
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "bucket_prod_policy" {
  bucket = aws_s3_bucket.bucket_prod.id
  policy = data.aws_iam_policy_document.bucket_prod_policy.json
}


# Development

resource "aws_s3_bucket" "bucket_dev" {
  bucket = "doc-dev.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  website {
    index_document = "index.html"
    error_document = "404.html"
  }

  tags = {
    "Name"               = "doc-dev.fluidattacks.com"
    "management:type"    = "development"
    "management:product" = "makes"
  }
}

data "aws_iam_policy_document" "bucket_dev_policy" {
  statement {
    sid    = "CloudFlare"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.bucket_dev.arn}/*",
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "bucket_dev_policy" {
  bucket = aws_s3_bucket.bucket_dev.id
  policy = data.aws_iam_policy_document.bucket_dev_policy.json
}

resource "aws_s3_bucket_object" "html" {
  for_each     = { for name in fileset("${path.module}/html", "*") : name => name }
  bucket       = aws_s3_bucket.bucket_dev.id
  key          = each.value
  source       = "html/${each.value}"
  etag         = filemd5("html/${each.value}")
  content_type = "text/html"

  tags = {
    "Name"               = each.value
    "management:type"    = "development"
    "management:product" = "makes"
  }
}

resource "aws_s3_bucket_object" "img" {
  for_each     = { for name in fileset(path.module, "img/*") : name => name }
  bucket       = aws_s3_bucket.bucket_dev.id
  key          = each.value
  source       = each.value
  etag         = filemd5(each.value)
  content_type = "image/png"

  tags = {
    "Name"               = each.value
    "management:type"    = "development"
    "management:product" = "makes"
  }
}

resource "aws_s3_bucket_object" "css" {
  for_each     = { for name in fileset(path.module, "css/*") : name => name }
  bucket       = aws_s3_bucket.bucket_dev.id
  key          = each.value
  source       = each.value
  etag         = filemd5(each.value)
  content_type = "text/css"

  tags = {
    "Name"               = each.value
    "management:type"    = "development"
    "management:product" = "makes"
  }
}
