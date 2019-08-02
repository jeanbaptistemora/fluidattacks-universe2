variable "asserts-clients" {
  type = "map"
}

resource "aws_s3_bucket" "asserts-buckets" {
  count = "${length(var.asserts-clients)}"
  bucket = "asserts-logs-${var.asserts-clients[count.index]}"
  acl    = "private"

  # Enable server-side encryption by default
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
