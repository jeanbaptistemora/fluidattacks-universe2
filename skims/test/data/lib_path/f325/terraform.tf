data "aws_iam_policy_document" "safe_policy_1" {
  statement {
    effect = "Allow"
    actions = [
      "a4b:ApproveSkill",
      "backup:ExportBackupPlanTemplate",
      "codeartifact:CreateRepository"
    ]

    resources = [
      "*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "codebuild:BatchDeleteBuilds",
      "codecommit:CreateBranch"
    ]

    resources = [
      "arn:aws:codebuild::111111111111:project/test",
      "arn:aws:codecommit::111111111111:test"
    ]
  }
}

data "aws_iam_policy_document" "vuln_policy_1" {
  statement {
    effect = "Allow"
    actions = [
      "a4b:ApproveSkill",
      "codecommit:CreateBranch"
    ]

    resources = [
      "*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "codecommit:Update*"
    ]

    resources = [
      "*"
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["*"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "vuln_role_policy_1" {
  name = "vuln_role_policy_1"
  role = aws_iam_role.vuln_role_1

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "codecommit:CreateBranch"
        ],
        "Resource": "*"
      }
    ]
  }
  EOF
}
