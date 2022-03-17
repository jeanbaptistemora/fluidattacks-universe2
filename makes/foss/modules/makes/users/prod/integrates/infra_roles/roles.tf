resource "aws_iam_role" "roles-secret-management" {
  for_each             = { for name in var.projects : name => name }
  name                 = "continuous-${each.value}"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "management:area"    = "cost"
    "management:product" = "services"
    "management:type"    = "service"
  }
}

resource "aws_iam_policy" "policies-secret-management" {
  for_each    = { for name in var.projects : name => name }
  description = "continuous-${each.value} policy"
  name        = "continuous-${each.value}"
  path        = "/user-provision/"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kms:DescribeKey",
        "kms:GetKeyPolicy",
        "kms:GetKeyRotationStatus",
        "kms:GetPublicKey",
        "kms:ListKeys",
        "kms:ListAliases",
        "kms:ListKeyPolicies",
        "iam:ListUsers",
        "iam:ListRoles"
      ],
      "Resource": "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/continuous-${each.value}"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::continuous-repositories"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::continuous-repositories/${each.value}/*",
        "arn:aws:s3:::continuous-repositories/${each.value}"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "continuous-prod-attach-policy" {
  for_each   = { for name in var.projects : name => name }
  role       = "continuous-${each.value}"
  policy_arn = aws_iam_policy.policies-secret-management[each.value].arn
}
