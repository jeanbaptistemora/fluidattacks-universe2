resource "aws_iam_policy" "break-build-policies" {
  for_each    = {for name in var.break_build_projects: name => name}
  name        = "break-build-${each.value}"
  path        = "/asserts/"
  description = "Asserts breaking build policy for ${each.value}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ecrPullContainer",
      "Effect": "Allow",
      "Action": [
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ],
      "Resource": ${jsonencode([
        for subs in lookup(var.break_build_project_allies, each.value, [each.value]):
        "arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/break-build-${subs}"
      ])}
    },
    {
      "Sid": "s3WriteLogs",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::${var.break-build-bucket}/${each.value}/*"
      ]
    },
    {
      "Sid": "ecrAuthToken",
      "Effect": "Allow",
      "Action": "ecr:GetAuthorizationToken",
      "Resource": "*"
    },
    {
      "Sid": "iamGetUser",
      "Effect": "Allow",
      "Action": "iam:GetUser",
      "Resource": [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/asserts/break-build-${each.value}"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_user" "break-build-users" {
  for_each = {for name in var.break_build_projects: name => name}
  name     = "break-build-${each.value}"
  path     = "/asserts/"
}

resource "aws_iam_user_policy_attachment" "attach-break-build-policies" {
  for_each   = {for name in var.break_build_projects: name => name}
  policy_arn = aws_iam_policy.break-build-policies[each.key].arn
  user       = aws_iam_user.break-build-users[each.key].name
}
