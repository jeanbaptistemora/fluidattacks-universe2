resource "aws_security_group_rule" "allow_all" {
  security_group_id = "sg-123456"
  type              = "ingress"
  from_port         = 0
  to_port           = 65535
  protocol          = "-1"
  cidr_blocks       = "0.0.0.0/0"
  prefix_list_ids   = ["pl-12c4e678"]

}

resource "aws_iam_policy" "policy1" {
  name        = "test_policy"
  path        = "/"
  description = "My test policy"

  policy = <<EOF
{
  "Statement": [
    {
      "Action": [
        "ecr:*"
      ],
      "Effect": "Allow",
      "Resource": [
        "*"
      ]
    },
    {
      "Action": "logs:*",
      "Effect": "Allow",
      "Resource": "arn:aws:logs:*:*:*:*"
    },
    {
      "Effect": "Allow",
      "NotAction": []
    },
    {
      "Effect": "Allow",
      "NotResource": []
    }
  ],
  "Version": "2012-10-17"
}
EOF
}

resource "aws_iam_role" "test_role" {
  name = "test_role"

  assume_role_policy = <<-EOF
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

resource "aws_iam_role_policy" "policy2" {
  name        = "test_policy_2"
  path        = "/"
  description = "Another test policy"
  role        = aws_iam_role.test_role.id

  policy = <<EOF
{
  "Statement": [
    {
      "Action": "*",
      "Effect": "Deny",
      "Resource": "*"
    },
    {
      "Action": [
        "ecr:Get*"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:ecr:us-east-1::repository/*"
      ]
    }
  ],
  "Version": "2012-10-17"
}
EOF
}

resource "aws_iam_role_policy" "policy_iam_powers" {
  name        = "policy_iam_powers"
  path        = "/"
  description = "Test policy with IAM powers"
  role        = aws_iam_role.test_role.id

  policy = <<EOF
{
"Statement": [
  {
    "Action": [
      "ecr:*"
    ],
    "Effect": "Allow",
    "Resource": [
      "*"
    ]
  },
  {
    "Action": "iam:ListUsers",
    "Effect": "Allow",
    "Resource": "*"
  },
  {
    "Action": "ecr:*",
    "Effect": "Allow",
    "Resource": "*"
  },
  {
    "Effect": "Allow",
    "NotAction": []
  },
  {
    "Effect": "Allow",
    "NotResource": []
  }
],
"Version": "2012-10-17"
}
EOF
}

resource "aws_iam_user_policy" "lb_ro" {
  name = "test"
  user = aws_iam_user.lb.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:Describe*"
      ],
      "Effect": "Deny",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_user" "lb" {
  name = "loadbalancer"
  path = "/system/"
}

resource "aws_iam_access_key" "lb" {
  user = aws_iam_user.lb.name
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
