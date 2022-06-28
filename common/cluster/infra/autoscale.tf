# Horizontal Pod Autoscaler

resource "helm_release" "metrics_server" {
  name       = "metrics-server"
  repository = "https://kubernetes-sigs.github.io/metrics-server"
  chart      = "metrics-server"
  version    = "3.8.2"
  namespace  = "kube-system"

  set {
    name  = "replicas"
    value = 3
  }
}

# Karpenter

module "karpenter_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.1.0"

  role_name                          = "karpenter-controller-${local.cluster_name}"
  attach_karpenter_controller_policy = true

  karpenter_controller_cluster_id = module.cluster.cluster_id
  karpenter_controller_ssm_parameter_arns = [
    "arn:aws:ssm:*:*:parameter/aws/service/*"
  ]
  karpenter_controller_node_iam_role_arns = [
    module.cluster.eks_managed_node_groups["karpenter"].iam_role_arn,
  ]

  oidc_providers = {
    main = {
      provider_arn               = module.cluster.oidc_provider_arn
      namespace_service_accounts = ["karpenter:karpenter"]
    }
  }
}

resource "aws_iam_instance_profile" "karpenter" {
  name = "KarpenterNodeInstanceProfile-${local.cluster_name}"
  role = module.cluster.eks_managed_node_groups["karpenter"].iam_role_name
}

resource "helm_release" "karpenter" {
  namespace        = "karpenter"
  create_namespace = true

  name       = "karpenter"
  repository = "https://charts.karpenter.sh"
  chart      = "karpenter"
  version    = "0.11.1"

  set {
    name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = module.karpenter_irsa.iam_role_arn
  }

  set {
    name  = "clusterName"
    value = module.cluster.cluster_id
  }

  set {
    name  = "clusterEndpoint"
    value = module.cluster.cluster_endpoint
  }

  set {
    name  = "aws.defaultInstanceProfile"
    value = aws_iam_instance_profile.karpenter.name
  }

  set {
    name  = "replicas"
    value = "3"
  }
}

resource "kubectl_manifest" "karpenter_development" {
  yaml_body = yamlencode(
    {
      apiVersion = "karpenter.sh/v1alpha5"
      kind       = "Provisioner"
      metadata = {
        name      = "development"
        namespace = "karpenter"
      }
      spec = {
        labels = {
          worker_group = "development"
        }
        requirements = [
          {
            key      = "karpenter.sh/capacity-type"
            operator = "In"
            values   = ["spot"]
          },
          {
            key      = "node.kubernetes.io/instance-type"
            operator = "In"
            values = [
              "m5.xlarge",
              "m5a.xlarge",
              "m5d.xlarge",
              "m5ad.xlarge",
            ]
          },
        ]
        provider = {
          subnetSelector = {
            "karpenter.sh/discovery" = local.cluster_name
          }
          securityGroupSelector = {
            "karpenter.sh/discovery" = local.cluster_name
          }
          tags = {
            "karpenter.sh/discovery" = local.cluster_name
          }
        }
        ttlSecondsAfterEmpty   = 1200
        ttlSecondsUntilExpired = 86400
      }
    }
  )

  depends_on = [
    helm_release.karpenter
  ]
}

resource "kubectl_manifest" "karpenter_production" {
  yaml_body = yamlencode(
    {
      apiVersion = "karpenter.sh/v1alpha5"
      kind       = "Provisioner"
      metadata = {
        name      = "production"
        namespace = "karpenter"
      }
      spec = {
        labels = {
          worker_group = "production"
        }
        requirements = [
          {
            key      = "karpenter.sh/capacity-type"
            operator = "In"
            values   = ["spot"]
          },
          {
            key      = "node.kubernetes.io/instance-type"
            operator = "In"
            values = [
              "m5.large",
              "m5a.large",
              "m5d.large",
              "m5ad.large",
            ]
          },
        ]
        provider = {
          subnetSelector = {
            "karpenter.sh/discovery" = local.cluster_name
          }
          securityGroupSelector = {
            "karpenter.sh/discovery" = local.cluster_name
          }
          tags = {
            "karpenter.sh/discovery" = local.cluster_name
          }
        }
        ttlSecondsAfterEmpty   = 1200
        ttlSecondsUntilExpired = 86400
      }
    }
  )

  depends_on = [
    helm_release.karpenter
  ]
}
