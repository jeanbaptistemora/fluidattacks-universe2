resource "aws_kms_key" "a" {
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

resource "aws_kms_key" "a" {
  description             = "KMS key 1"
  deletion_window_in_days = 10

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Principal": {
          "AWS": "arn:aws:iam::123456789012:root"
        },
        "Effect": "Allow"
      }
    ]
  }
  EOF
}

resource "aws_kms_key" "a" {
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
        "Effect": "Deny"
      }
    ]
  }
  EOF
}
