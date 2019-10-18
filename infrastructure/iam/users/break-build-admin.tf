data "aws_iam_policy_document" "break-build-admin-data" {

  statement {
      sid = "ecrBreakBuildAdminAuthToken"
      effect = "Allow"
      actions = [
        "ecr:GetAuthorizationToken"
      ]
      resources = [
        "*"
      ]
    }

  statement {
    sid = "ecrBreakBuildAdmin"
    effect = "Allow"
    actions = [
      "ecr:PutImage",
      "ecr:BatchCheckLayerAvailability",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload"
    ]
    resources = [
      "arn:aws:ecr::${data.aws_caller_identity.current.account_id}:repository/*"
    ]
  }

  statement {
    sid = "s3BreakBuildAdmin"
    effect = "Allow"
    actions = [
      "s3:HeadBucket",
      "s3:ListAllMyBuckets",
      "s3:ListBucket",
      "s3:CreateBucket",
      "s3:DeleteBucket",
      "s3:DeleteObject",
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::break-build-*"
    ]
  }

  statement {
    sid = "iamBreakBuildAdmin"
    effect = "Allow"
    actions = [
      "iam:*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/asserts/break-build-*"
    ]
  }
}

resource "aws_iam_policy" "break-build-admin-policy" {
  name        = "break-build-admin-policy"
  path        = "/asserts/"
  description = "Policy to administrate the Break Build service"

  policy = "${data.aws_iam_policy_document.break-build-admin-data.json}"
}

resource "aws_iam_user" "break-build-admin-user" {
  name     = "break-build-admin"
  path     = "/asserts/"
}

resource "aws_iam_user_policy_attachment" "attach-break-build-admin-policy" {
  policy_arn = "${aws_iam_policy.break-build-admin-policy.arn}"
  user       = "${aws_iam_user.break-build-admin-user.name}"
}
