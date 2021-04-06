resource "helm_release" "alb" {
  name       = "alb"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  version    = "1.1.6"
  namespace  = "kube-system"

  set {
    name  = "clusterName"
    value = var.cluster_name
  }
}
