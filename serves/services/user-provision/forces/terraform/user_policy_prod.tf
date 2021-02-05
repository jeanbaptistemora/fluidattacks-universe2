data "aws_iam_policy_document" "forces_prod_policy_data" {
  # S3 access to the terraform state
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod/break-build.tfstate",
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

  # IAM Break Build and AWS SSO role
  statement {
    effect = "Allow"
    actions = [
      "iam:*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/asserts/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/asserts/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/break-build-*",
    ]
  }

  # KMS FUll permissions over owned KMS keys
  statement {
    effect = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/continuous-*"
    ]
  }

  # Secretsmanager for forces
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:CreateSecret",
      "secretsmanager:DeleteSecret",
      "secretsmanager:DescribeSecret",
      "secretsmanager:GetResourcePolicy",
      "secretsmanager:PutSecretValue",
      "secretsmanager:RestoreSecret",
      "secretsmanager:UpdateSecret",
      "secretsmanager:TagResource",
    ]
    resources = [
      "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:forces-*"
    ]
  }

}

resource "aws_iam_policy" "forces_prod_policy" {
  description = "forces_prod policy"
  name        = "forces_prod_policy"
  path        = "/user_provision/"
  policy      = data.aws_iam_policy_document.forces_prod_policy_data.json
}

resource "aws_iam_user_policy_attachment" "forces_prod_attach_policy" {
  user       = "forces_prod"
  policy_arn = aws_iam_policy.forces_prod_policy.arn
}
