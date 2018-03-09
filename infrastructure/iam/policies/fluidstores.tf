resource "aws_iam_policy" "fluidstores" {
  name        = "fluidstores"
  path        = "/"
  description = "Policy for fluidstores"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::fluidserves/exams/*",
                "arn:aws:s3:::fluidserves",
                "arn:aws:s3:::fluidpersistent",
                "arn:aws:s3:::fluidpersistent/*"
            ]
        }
    ]
}
EOF
}
