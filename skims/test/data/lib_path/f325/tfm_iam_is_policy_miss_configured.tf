resource "aws_iam_role_policy" "test_policy" {
  name = "test_policy"
  role = aws_iam_role.test_role.id

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "ec2:*",
          "iam:*",
          "eks:*"
        ],
        "Resource": "*",
        "Effect": "Allow"
      },
      {
        "Action": [
          "ec2:Something"
        ],
        "Resource": "*",
        "Effect": "Deny"
      },
      {
        "Action": "*",
        "Resource": "arn:::ec2/specific",
        "Effect": "Allow"
      },
      {
        "Action": "ec2:Something",
        "Resource": "arn:::ec2/specific",
        "Effect": "Allow"
      }
    ]
  }
  EOF
}

data "aws_iam_policy_document" "example" {
  statement {
    actions = [
      "ec2:*",
      "autoscaling:*",
      "eks:*"
    ]

    resources = [
      "*",
    ]
  }

  statement {
    sid    = "Enable IAM User Permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
    actions = [
      "iam:*"
    ]
    resources = [
      "*"
    ]
  }
}
