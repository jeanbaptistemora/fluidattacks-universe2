variable "region" {}
variable "asserts-bucket" {}
variable "asserts-clients" {
  type = "map"
}


resource "aws_iam_policy" "asserts-policies" {
  count = "${length(var.asserts-clients)}"
  name = "${var.asserts-clients[count.index]}"
  path = "/asserts/"
  description = "Asserts policy for ${var.asserts-clients[count.index]}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ecrRules",
      "Effect": "Allow",
      "Action": [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:DescribeImages",
        "ecr:ListTagsForResource",
        "ecr:BatchCheckLayerAvailability"
      ],
      "Resource": [
        "arn:aws:ecr:${var.region}::repository/asserts-${var.asserts-clients[count.index]}"
      ]
    },
    {
      "Sid": "s3Rules",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::${var.asserts-bucket}/${var.asserts-clients[count.index]}/*"
      ]
    },
    {
      "Sid": "ecrAuthToken",
      "Effect": "Allow",
      "Action": "ecr:GetAuthorizationToken",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_user" "asserts-users" {
  count = "${length(var.asserts-clients)}"
  name = "${var.asserts-clients[count.index]}"
  path = "/asserts/"
}

resource "aws_iam_user_policy_attachment" "attach-policies" {
  count = "${length(var.asserts-clients)}"
  policy_arn = "${aws_iam_policy.asserts-policies.*.name[count.index]}"
  user = "${aws_iam_user.asserts-users.*.name[count.index]}"
}
