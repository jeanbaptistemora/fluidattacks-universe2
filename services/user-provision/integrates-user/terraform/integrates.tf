resource "aws_iam_user" "integrates" {
 name = "integrates-user"
 path = "user-provision"
}

resource "aws_iam_acces_key" "integrates" {
    user = aws_iam_user.integrates.name
}

resource "aws_iam_user_policy" "integrates-user-policies" {
    name = "user-provisioning-policy-${aws_iam_user.integrates.name}"
    user = aws_iam_user.integrates.name

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "kms:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
            "Condition" : {
                "StringEquals" : {
                    "aws:username" : "${aws_iam_user.integrates.name}"
                    }
                }
        }
    ]
}
EOF
}
