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
        "NotPrincipal": {
          "Service": [
            "s3.amazonaws.com"
          ]
        },
        "Action": [
          "sts:AssumeRole"
        ]
      }
    ]
  }
  EOF

  managed_policy_arns = [
    aws_iam_policy.policy_one.arn,
    aws_iam_policy.policy_two.arn,
    "arn:aws:iam::aws:policy/AdministratorAccess",
    "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
  ]
}

resource "aws_iam_role_policy" "test_policy" {
  name = "test_policy"
  role = aws_iam_role.test_role.id

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "ec2:action"
        ],
        "Resource": "*",
        "Effect": "Allow"
      }
    ]
  }
  EOF
}
