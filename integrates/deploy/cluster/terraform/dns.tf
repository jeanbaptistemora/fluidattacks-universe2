data "aws_iam_policy_document" "dns" {

  statement {
    effect = "Allow"
    actions = [
      "route53:ChangeResourceRecordSets",
    ]
    resources = [
      "arn:aws:route53:::hostedzone/*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "route53:ListHostedZones",
      "route53:ListResourceRecordSets",
    ]
    resources = [
      "*"
    ]
  }

}

data "aws_iam_policy_document" "oidc_assume_role_dns" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect = "Allow"
    principals {
      identifiers = [
        module.eks.oidc_provider_arn,
      ]
      type = "Federated"
    }
    condition {
      test     = "StringEquals"
      variable = "${replace(module.eks.cluster_oidc_issuer_url, "https://", "")}:sub"
      values = [
        "system:serviceaccount:kube-system:aws-external-dns"
      ]
    }
  }
}

resource "aws_iam_policy" "dns" {
  description = "DNS policy for ${var.cluster_name}"
  name        = "${var.cluster_name}-dns"
  policy      = data.aws_iam_policy_document.dns.json
}

resource "aws_iam_role" "dns" {
  name               = "${var.cluster_name}-dns"
  assume_role_policy = data.aws_iam_policy_document.oidc_assume_role_dns.json
}

resource "aws_iam_role_policy_attachment" "dns" {
  role       = aws_iam_role.dns.name
  policy_arn = aws_iam_policy.dns.arn
}
