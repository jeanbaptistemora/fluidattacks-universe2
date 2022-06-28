data "http" "alb-policy" {
  url = "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/45f9e9d89e359bf0988d74b6240ca821823110bb/docs/install/iam_policy.json"
}

resource "aws_iam_policy" "alb" {
  name_prefix = "common-cluster-alb"
  policy      = data.http.alb-policy.body
}

module "alb_oidc_role" {
  source       = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  version      = "5.2.0"
  create_role  = true
  role_name    = "common-cluster-alb"
  provider_url = replace(module.cluster.cluster_oidc_issuer_url, "https://", "")

  role_policy_arns = [
    aws_iam_policy.alb.arn,
  ]

  oidc_fully_qualified_subjects = [
    "system:serviceaccount:kube-system:alb",
  ]
}

resource "kubernetes_service_account" "alb" {
  automount_service_account_token = true

  metadata {
    name      = "alb"
    namespace = "kube-system"

    labels = {
      "app.kubernetes.io/name"       = "alb"
      "app.kubernetes.io/managed-by" = "terraform"
      "k8s-addon"                    = "k8s-alb.addons.k8s.io"
      "k8s-app"                      = "k8s-alb"
    }

    annotations = {
      "eks.amazonaws.com/role-arn" = module.alb_oidc_role.iam_role_arn
    }
  }
}

resource "helm_release" "alb" {
  name       = "alb"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  version    = "1.4.2"
  namespace  = "kube-system"

  set {
    name  = "clusterName"
    value = local.cluster_name
  }

  set {
    name  = "serviceAccount.create"
    value = false
  }

  set {
    name  = "serviceAccount.name"
    value = kubernetes_service_account.alb.metadata[0].name
  }

  set {
    name  = "serviceAccount.annotations.\"eks.amazonaws.com/role-arn\""
    value = module.alb_oidc_role.iam_role_arn
  }
}
