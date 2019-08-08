variable "asserts-bucket" {}
variable "asserts_projects" {
  type = "map"
}
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

resource "aws_iam_policy" "asserts-policies" {
  count = "${length(var.asserts_projects)}"
  name = "asserts-logs-policy-${var.asserts_projects[count.index]}"
  path = "/asserts/"
  description = "Asserts policy for ${var.asserts_projects[count.index]}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ecrPullContainer",
      "Effect": "Allow",
      "Action": [
        "ecr:BatchGetImage"
      ],
      "Resource": [
        "arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/asserts-${var.asserts_projects[count.index]}"
      ]
    },
    {
      "Sid": "s3WriteLogs",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::${var.asserts-bucket}/${var.asserts_projects[count.index]}/*"
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
  count = "${length(var.asserts_projects)}"
  name = "asserts-${var.asserts_projects[count.index]}"
  path = "/asserts/"
}

resource "aws_iam_user_policy_attachment" "attach-policies" {
  count = "${length(var.asserts_projects)}"
  policy_arn = "${aws_iam_policy.asserts-policies.*.arn[count.index]}"
  user = "${aws_iam_user.asserts-users.*.name[count.index]}"
}
