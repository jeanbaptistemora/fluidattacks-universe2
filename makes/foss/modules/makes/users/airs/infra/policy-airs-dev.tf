data "aws_iam_policy_document" "web-dev-policy-data" {

  # S3 web prod bucket
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:Get*",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks.com/*",
      "arn:aws:s3:::fluidattacks.com",
    ]
  }

  # S3 web ephemeral bucket
  statement {
    effect = "Allow"
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
    effect = "Allow"
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
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-service-role/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/web-*",
    ]
  }

  # ACM read certificate
  statement {
    effect = "Allow"
    actions = [
      "acm:DescribeCertificate",
      "acm:ListTagsForCertificate",
    ]
    resources = [
      "*",
    ]
  }

  # Lambda
  statement {
    effect = "Allow"
    actions = [
      "lambda:Get*",
      "lambda:List*"
    ]
    resources = [
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:web-*"
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
    effect = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/web-dev-*"
    ]
  }

  # DynamoDB for locking terraform state
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:DeleteItem",
      "dynamodb:GetItem",
      "dynamodb:PutItem",
    ]
    resources = [
      var.terraform_state_lock_arn,
    ]
  }
}
resource "aws_iam_policy" "web-dev-policy" {
  description = "web-dev policy"
  name        = "web-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.web-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "web-dev-attach-policy" {
  user       = "web-dev"
  policy_arn = aws_iam_policy.web-dev-policy.arn
}
