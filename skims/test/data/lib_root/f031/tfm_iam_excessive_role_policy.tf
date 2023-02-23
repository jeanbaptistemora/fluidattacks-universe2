resource "aws_iam_role" "role" {
  name = "test_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "test_policy" {
  name        = "test_policy"
  description = "A test policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:Describe*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
        "Sid": "iamWrite",
        "Effect": "Allow",
        "Action": [
            "iam:Attach*",
            "iam:Create*"
        ],
        "Resource": [
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/*test_role*"
        ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "vuln_role_1" {
  name = "vuln_role_1"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "iam:Attach*"
        ],
        Effect   = "Allow"
        Resource = "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/*test_role*"
      },
    ]
  })
}

data "aws_iam_policy_document" "example" {
  statement {
    actions = [
      "iam:Attach*"
    ]

    resources = [
      "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/*test_role*",
    ]
  }
}

resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.test_policy.arn
}
