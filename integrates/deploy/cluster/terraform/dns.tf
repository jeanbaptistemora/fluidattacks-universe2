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

  tags = {
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_iam_role_policy_attachment" "dns" {
  role       = aws_iam_role.dns.name
  policy_arn = aws_iam_policy.dns.arn
}

resource "kubernetes_service_account" "dns" {
  automount_service_account_token = true
  metadata {
    name      = "aws-external-dns"
    namespace = "kube-system"
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.dns.arn
    }
    labels = {
      "app.kubernetes.io/name"       = "aws-external-dns"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }
}

resource "kubernetes_cluster_role" "dns" {
  metadata {
    name = "aws-external-dns"
    labels = {
      "app.kubernetes.io/name"       = "aws-external-dns"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  rule {
    api_groups = [
      "",
    ]
    resources = [
      "services",
      "pods",
      "endpoints",
    ]
    verbs = [
      "get",
      "list",
      "watch",
    ]
  }
  rule {
    api_groups = [
      "extensions",
    ]
    resources = [
      "ingresses",
    ]
    verbs = [
      "get",
      "list",
      "watch",
    ]
  }
  rule {
    api_groups = [
      "",
    ]
    resources = [
      "nodes",
    ]
    verbs = [
      "list",
    ]
  }
}

resource "kubernetes_cluster_role_binding" "dns" {
  metadata {
    name = "aws-external-dns"
    labels = {
      "app.kubernetes.io/name"       = "aws-external-dns"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.dns.metadata[0].name
  }

  subject {
    api_group = ""
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.dns.metadata[0].name
    namespace = kubernetes_service_account.dns.metadata[0].namespace
  }
}

resource "kubernetes_deployment" "dns" {
  depends_on = [kubernetes_cluster_role_binding.dns]

  metadata {
    name      = "aws-external-dns"
    namespace = "kube-system"
    labels = {
      "app.kubernetes.io/name"       = "aws-external-dns"
      "app.kubernetes.io/version"    = "v${var.external_dns_version}"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "aws-external-dns"
      }
    }

    strategy {
      type = "Recreate"
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name"    = "aws-external-dns"
          "app.kubernetes.io/version" = var.external_dns_version
        }
      }

      spec {
        automount_service_account_token = true
        service_account_name = kubernetes_service_account.dns.metadata[0].name

        container {
          name              = "aws-external-dns"
          image             = "bitnami/external-dns:0.7.3"
          image_pull_policy = "Always"

          args = [
            "--source=service",
            "--source=ingress",
            "--domain-filter=fluidattacks.com",
            "--provider=aws",
            "--policy=sync",
            "--aws-zone-type=public",
            "--registry=txt",
            "--txt-owner-id=aws-external-dns",
          ]
        }

        security_context {
          fs_group = 65534
        }
      }
    }
  }
}
