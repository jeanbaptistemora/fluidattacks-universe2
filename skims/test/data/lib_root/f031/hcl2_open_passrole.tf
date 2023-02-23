resource "aws_iam_role_policy" "test_policy" {
  name = "test_policy"
  role = aws_iam_role.test_role.id

  policy = <<-EOF
  {
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "iam:PassRole",
        "Resource": "*",
        "Condition": {
          "StringEquals": {
            "iam:PassedToService": "cloudwatch.amazonaws.com"
          }
        }
      },
      {
        "Effect": "Allow",
        "Action": "iam:PassRole",
        "Resource": "arn:aws:iam::*:role/EC2-roles-for-XYZ-*"
      },
      {
        "Effect": "Allow",
        "Action": "iam:Pass*",
        "Resource": "*"
      }
    ]
  }
  EOF
}

data "aws_iam_policy_document" "example" {
  statement {
    actions = [
      "iam:PassRole"
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "vuln_role_1" {
  name = "vuln_role_1"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:*",
          "s3:DeleteObjectVersion",
          "iam:*"
        ],
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}
