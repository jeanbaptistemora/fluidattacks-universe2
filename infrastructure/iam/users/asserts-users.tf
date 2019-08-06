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
      "Sid": "ECR Rules",
      "Effect": "Allow",
      "Action": [
        "ecr:GetLifecyclePolicyPreview",
        "ecr:GetDownloadUrlForLayer",
        "ecr:ListTagsForResource",
        "ecr:ListImages",
        "ecr:BatchGetImage",
        "ecr:DescribeImages",
        "ecr:DescribeRepositories",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetLifecyclePolicy",
        "ecr:GetRepositoryPolicy"
      ],
      "Resource": [
        "arn:aws:ecr:${var.region}::repository/asserts-${var.asserts-clients[count.index]}"
      ]
    },
    {
      "Sid": "S3 Rules",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::${var.asserts-bucket}/${var.asserts-clients[count.index]}/*"
      ]
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
