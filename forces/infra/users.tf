resource "aws_iam_policy" "break-build-policies" {
  for_each    = {for name in var.projects: name => name}
  name        = "break-build-${each.value}"
  path        = "/asserts/"
  description = "Asserts breaking build policy for ${each.value}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "iamGetUser",
      "Effect": "Allow",
      "Action": "iam:GetUser",
      "Resource": [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/asserts/break-build-${each.value}"
      ]
    },
    {
      "Sid": "getForcesApiToken",
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": [
        "arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:forces-token-${each.value}-??????"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_user" "break-build-users" {
  for_each = {for name in var.projects: name => name}
  name     = "break-build-${each.value}"
  path     = "/asserts/"

  tags = {
    "management:type"    = "production"
    "management:product" = "drills"
  }
}

resource "aws_iam_user_policy_attachment" "attach-break-build-policies" {
  for_each   = {for name in var.projects: name => name}
  policy_arn = aws_iam_policy.break-build-policies[each.key].arn
  user       = aws_iam_user.break-build-users[each.key].name
}

resource "aws_iam_access_key" "break-build-credentials" {
  for_each = {for name in var.projects: name => name}
  user     = "break-build-${each.value}"
}
