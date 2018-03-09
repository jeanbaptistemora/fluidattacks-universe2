resource "aws_iam_policy" "Blog_IAM_Policy" {
  name        = "Blog_IAM_Policy"
  path        = "/"
  description = "Policy for web"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::web.fluid.la/*",
                "arn:aws:s3:::web.fluidattacks.com/*",
                "arn:aws:s3:::web.fluid.la",
                "arn:aws:s3:::web.fluidattacks.com"
            ]
        }
    ]
}
EOF
}
