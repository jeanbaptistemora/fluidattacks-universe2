data "aws_iam_policy_document" "autoscaler" {
  statement {
    sid    = "AutoscalerAll"
    effect = "Allow"

    actions = [
      "autoscaling:DescribeAutoScalingGroups",
      "autoscaling:DescribeAutoScalingInstances",
      "autoscaling:DescribeLaunchConfigurations",
      "autoscaling:DescribeTags",
      "autoscaling:SetDesiredCapacity",
      "autoscaling:TerminateInstanceInAutoScalingGroup",
      "autoscaling:UpdateAutoScalingGroup",
      "ec2:DescribeLaunchTemplateVersions",
    ]

    resources = ["*"]
  }

  statement {
    sid    = "AutoscalerOwn"
    effect = "Allow"

    actions = [
      "autoscaling:SetDesiredCapacity",
      "autoscaling:TerminateInstanceInAutoScalingGroup",
      "autoscaling:UpdateAutoScalingGroup",
    ]

    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "autoscaling:ResourceTag/k8s.io/cluster-autoscaler/${module.eks.cluster_id}"
      values   = ["owned"]
    }

    condition {
      test     = "StringEquals"
      variable = "autoscaling:ResourceTag/k8s.io/cluster-autoscaler/enabled"
      values   = ["true"]
    }
  }
}

resource "aws_iam_policy" "autoscaler" {
  name_prefix = "makes-k8s-autoscaler"
  description = "EKS cluster-autoscaler policy for cluster ${module.eks.cluster_id}"
  policy      = data.aws_iam_policy_document.autoscaler.json
}

module "autoscaler_oidc_role" {
  source       = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  version      = "3.8.0"
  create_role  = true
  role_name    = "makes-k8s-autoscaler"
  provider_url = replace(module.eks.cluster_oidc_issuer_url, "https://", "")

  role_policy_arns = [
    aws_iam_policy.autoscaler.arn,
  ]

  oidc_fully_qualified_subjects = [
    "system:serviceaccount:kube-system:autoscaler",
  ]
}

resource "kubernetes_service_account" "autoscaler" {
  automount_service_account_token = true

  metadata {
    name      = "autoscaler"
    namespace = "kube-system"

    labels = {
      "app.kubernetes.io/name"       = "autoscaler"
      "app.kubernetes.io/managed-by" = "terraform"
      "k8s-addon"                    = "cluster-autoscaler.addons.k8s.io"
      "k8s-app"                      = "cluster-autoscaler"
    }

    annotations = {
      "eks.amazonaws.com/role-arn" = module.autoscaler_oidc_role.this_iam_role_arn
    }
  }
}

resource "helm_release" "autoscaler" {
  name       = "autoscaler"
  repository = "https://kubernetes.github.io/autoscaler"
  chart      = "cluster-autoscaler"
  version    = "9.9.0"
  namespace  = "kube-system"

  set {
    name  = "autoDiscovery.clusterName"
    value = var.cluster_name
  }

  set {
    name  = "rbac.serviceAccount.create"
    value = false
  }

  set {
    name  = "rbac.serviceAccount.name"
    value = kubernetes_service_account.autoscaler.metadata[0].name
  }

  set {
    name  = "rbac.serviceAccount.annotations.\"eks.amazonaws.com/role-arn\""
    value = module.autoscaler_oidc_role.this_iam_role_arn
  }

  set {
    name  = "extraArgs.scale-down-unneeded-time"
    value = "20m"
  }
}
