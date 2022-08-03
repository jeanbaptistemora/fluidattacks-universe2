data "aws_caller_identity" "main" {}
data "aws_eks_cluster" "common" {
  name = "common"
}
locals {
  assume_role_policy = {
    Version = "2012-10-17",
    Statement = concat(
      [
        {
          Sid    = "commonClusterAssumePolicy",
          Effect = "Allow",
          Principal = {
            Federated = join(
              "/",
              [
                "arn:aws:iam::${data.aws_caller_identity.main.account_id}:oidc-provider",
                replace(data.aws_eks_cluster.common.identity[0].oidc[0].issuer, "https://", ""),
              ]
            )
          },
          Action = "sts:AssumeRoleWithWebIdentity",
          Condition = {
            StringEquals = {
              join(
                ":",
                [
                  replace(data.aws_eks_cluster.common.identity[0].oidc[0].issuer, "https://", ""),
                  "sub",
                ]
              ) : "system:serviceaccount:development:dev"
            },
          },
        },
        {
          Sid    = "ecsTaskAccess",
          Effect = "Allow",
          Principal = {
            Service = [
              "ecs-tasks.amazonaws.com",
            ],
          },
          Action = "sts:AssumeRole",
        },
        {
          Sid    = "oktaSAMLAccess",
          Effect = "Allow",
          Principal = {
            Federated = "arn:aws:iam::${data.aws_caller_identity.main.account_id}:saml-provider/okta-saml-provider",
          },
          Action = "sts:AssumeRoleWithSAML",
          Condition = {
            StringEquals = {
              "SAML:aud" = "https://signin.aws.amazon.com/saml",
            },
          },
        },
      ],
      var.extra_assume_role_policies,
    )
  }
}

resource "aws_iam_role" "main" {
  name                 = var.name
  assume_role_policy   = jsonencode(local.assume_role_policy)
  max_session_duration = "32400"
  tags                 = var.tags
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}
