resource "helm_release" "metrics_server" {
  chart       = "metrics-server"
  description = "Horizontal pod autoscaler"
  name        = "metrics-server"
  namespace   = "kube-system"
  repository  = "https://kubernetes-sigs.github.io/metrics-server"
  version     = "3.8.3"
}

resource "helm_release" "keda_autoscaler" {
  chart       = "keda"
  description = "Kubernetes Event Driven Autoscaler"
  name        = "keda-autoscaler"
  namespace   = "kube-system"
  repository  = "https://kedacore.github.io/charts"
  version     = "2.9.3"
}

# Cluster autoscaler

resource "aws_iam_policy" "autoscaler" {
  name_prefix = "${local.cluster_name}-autoscaler-"

  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "autoscaling:DescribeAutoScalingGroups",
            "autoscaling:DescribeAutoScalingInstances",
            "autoscaling:DescribeLaunchConfigurations",
            "autoscaling:DescribeTags",
            "autoscaling:SetDesiredCapacity",
            "autoscaling:TerminateInstanceInAutoScalingGroup",
            "ec2:DescribeInstanceTypes",
            "ec2:DescribeLaunchTemplateVersions",
            "ec2:DescribeInstanceTypes",
            "eks:DescribeNodegroup",
            "cloudwatch:GetMetricData",
          ]
          Resource = ["*"]
        },
      ]
    }
  )
}

module "autoscaler_oidc_role" {
  source           = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  version          = "5.11.1"
  create_role      = true
  role_name_prefix = "${local.cluster_name}-autoscaler-"
  provider_url     = replace(module.cluster.cluster_oidc_issuer_url, "https://", "")

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

    annotations = {
      "eks.amazonaws.com/role-arn" = module.autoscaler_oidc_role.iam_role_arn
    }
  }
}

resource "helm_release" "autoscaler" {
  name       = "autoscaler"
  repository = "https://kubernetes.github.io/autoscaler"
  chart      = "cluster-autoscaler"
  version    = "9.21.1"
  namespace  = "kube-system"

  set {
    name  = "autoDiscovery.clusterName"
    value = local.cluster_name
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
    value = module.autoscaler_oidc_role.iam_role_arn
  }

  set {
    name  = "extraArgs.scale-down-unneeded-time"
    value = "15m"
  }
}
