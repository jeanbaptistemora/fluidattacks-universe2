variable "asserts-bucket" {}
variable "asserts_projects" {
  type = list(string)
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

resource "aws_iam_policy" "asserts-policies-1" {
  for_each    = {for name in var.asserts_projects: name => name}
  name        = "asserts-logs-policy-${each.value}"
  path        = "/asserts/"
  description = "Asserts policy for ${each.value}"

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
        "arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/asserts-${each.value}"
      ]
    },
    {
      "Sid": "s3WriteLogs",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::${var.asserts-bucket}/${each.value}/*"
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

resource "aws_iam_user" "asserts-users-1" {
  for_each = {for name in var.asserts_projects: name => name}
  name     = "asserts-${each.value}"
  path     = "/asserts/"
}

resource "aws_iam_user_policy_attachment" "attach-asserts-policies" {
  for_each   = {for name in var.asserts_projects: name => name}
  policy_arn = aws_iam_policy.asserts-policies-1[each.key].arn
  user       = aws_iam_user.asserts-users-1[each.key].name
}
