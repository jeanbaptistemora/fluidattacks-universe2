module "alb_ingress_controller" {
  source  = "iplabs/alb-ingress-controller/kubernetes"
  version = "~> 3.4.0"

  k8s_cluster_type = "eks"
  k8s_namespace    = "kube-system"

  aws_region_name  = var.region
  k8s_cluster_name = var.cluster_name

  aws_alb_ingress_controller_version = "1.1.7"
  aws_resource_name_prefix = ""
}
