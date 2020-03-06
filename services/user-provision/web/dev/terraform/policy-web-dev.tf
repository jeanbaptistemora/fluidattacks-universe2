data "aws_iam_policy_document" "web-dev-policy-data" {

  # S3 web bucket
  statement {
    effect  = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:Get*",
    ]
    resources = [
      "arn:aws:s3:::web.fluidattacks.com/*",
      "arn:aws:s3:::web.fluidattacks.com",
    ]
  }

  statement {
    effect  = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:Get*",
      "s3:PutObject",
      "s3:PutObjectAcl",
      "s3:DeleteObject*",
    ]
    resources = [
      "arn:aws:s3:::web.eph.fluidattacks.com/*",
      "arn:aws:s3:::web.eph.fluidattacks.com",
    ]
  }

  # S3 state files
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-*",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/web-secret-management.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-*/user-provision-web-*.tfstate",
    ]
  }

  # IAM read over owned users, roles and policies
  statement {
    effect  = "Allow"
    actions = [
      "iam:GetUser",
      "iam:GetRole",
      "iam:GetPolicy",
      "iam:GetPolicyVersion",
      "iam:ListAttachedUserPolicies",
      "iam:ListAttachedRolePolicies"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/web-*",
    ]
  }

  # KMS read keys
  statement {
    effect = "Allow"
    actions = [
      "kms:List*",
      "kms:Get*",
      "kms:Describe*"
    ]
    resources = [
      "*"
    ]
  }

  # KMS full permissions
  statement {
    effect  = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/web-dev-*"
    ]
  }
}
resource "aws_iam_policy" "web-dev-policy" {
  description = "web-dev policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.web-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "web-dev-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.web-dev-policy.arn
}
