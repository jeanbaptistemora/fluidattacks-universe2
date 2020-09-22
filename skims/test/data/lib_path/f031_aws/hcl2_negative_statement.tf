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
        "NotResource": "*"
      },
      {
        "Effect": "Allow",
        "NotAction": "*",
        "NotResource": "something"
      },
      {
        "Effect": "Allow",
        "NotAction": "s3:ListBucket",
        "NotResource": "*"
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
