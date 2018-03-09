resource "aws_iam_policy" "SSO_Finance" {
  name        = "SSO_Finance"
  path        = "/"
  description = "Policy for SSO_Finance"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1450111320000",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": [
                "arn:aws:ec2:us-east-1:205810638802:instance/i-0ba149836e9bb8e7c"
            ]
        }
    ]
}
EOF
}
