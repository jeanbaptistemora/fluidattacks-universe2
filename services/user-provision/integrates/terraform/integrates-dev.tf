resource "aws_iam_user" "integrates-dev" {
 name = "integrates-dev"
 path = "/user-provision/"
}

resource "aws_iam_access_key" "integrates-dev-key" {
    user = aws_iam_user.integrates-dev.name
}

resource "aws_iam_user_policy" "integrates-user-policies" {
    name = "user-provision-policy-${aws_iam_user.integrates-dev.name}"
    user = aws_iam_user.integrates-dev.name

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "kms:*"
            ],
            "Effect": "Allow",
            "Resource": "*",
            "Condition" : {
                "StringEquals" : {
                    "aws:username" : "${aws_iam_user.integrates-dev.name}"
                    }
                }
        }
    ]
}
EOF
}
