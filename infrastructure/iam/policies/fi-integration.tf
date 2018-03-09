resource "aws_iam_policy" "FI_S3INTEGRATION" {
  name        = "FI_S3INTEGRATION"
  path        = "/"
  description = "Policy for FI_S3INTEGRATION"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        }
    ]
}
EOF
}
