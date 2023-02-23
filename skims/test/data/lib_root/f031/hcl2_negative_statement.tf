resource "aws_iam_role" "role" {
  name = "test_role"
  path = "/"

  assume_role_policy = <<-EOF
  {
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": [
            "ec2.amazonaws.com"
          ]
        },
        "Action": [
          "sts:AssumeRole"
        ]
      },
      {
        "Effect": "Allow",
        "NotAction": "s3:ListBucket",
        "NotResource": "something"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy" "test_policy" {
  name = "test_policy"
  role = aws_iam_role.test_role.id

  policy = <<-EOF
  {
    "Statement": [
      {
        "Effect": "Allow",
        "NotAction": "*",
        "NotResource": "something"
      }
    ]
  }
  EOF
}

resource "aws_iam_policy_document" "example" {
  statement {
    not_actions   = "*"
    not_resources = "something"
  }
}

resource "aws_iam_role_policy" "vuln_role_1" {
  name = "vuln_role_1"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        NotAction   = ["*"],
        Effect      = "Allow"
        Principal   = "*"
        NotResource = ["something", ]
      }
    ]
  })
}
