resource "aws_kms_key" "vuln_key_exposed_1" {
  description             = "KMS key 1"
  deletion_window_in_days = 10

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Principal": {
          "AWS": "*"
        },
        "Effect": "Allow"
      }
    ]
  }
  EOF
}


resource "aws_kms_key" "sec_key" {
  description = "KMS 2"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Deny"
        Principal = {
          AWS = "*"
        }
      },
    ]
  })
}
