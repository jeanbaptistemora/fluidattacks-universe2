data "aws_iam_policy_document" "integrates-ecr-admin-data" {

  statement {
      sid = "ecrIntegratesECRAdminAuthToken"
      effect = "Allow"
      actions = [
        "ecr:GetAuthorizationToken"
      ]
      resources = [
        "*"
      ]
    }

  statement {
    sid = "ecrIntegratesECRAdmin"
    effect = "Allow"
    actions = [
      "ecr:PutImage",
      "ecr:BatchCheckLayerAvailability",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload"
    ]
    resources = [
      "arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/integrates-*"
    ]
  }

  statement {
    sid = "iamIntegratesECRAdmin"
    effect = "Allow"
    actions = [
      "iam:*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/integrates/integrates-ecr-*"
    ]
  }
}

resource "aws_iam_policy" "integrates-ecr-admin-policy" {
  name        = "integrates-ecr-admin-policy"
  path        = "/integrates/"
  description = "Policy to administrate Integrates ECR"

  policy = data.aws_iam_policy_document.integrates-ecr-admin-data.json
}

resource "aws_iam_user" "integrates-ecr-admin-user" {
  name     = "integrates-ecr-admin"
  path     = "/integrates/"
}

resource "aws_iam_user_policy_attachment" "attach-integrates-ecr-admin-policy" {
  policy_arn = aws_iam_policy.integrates-ecr-admin-policy.arn
  user       = aws_iam_user.integrates-ecr-admin-user.name
}
