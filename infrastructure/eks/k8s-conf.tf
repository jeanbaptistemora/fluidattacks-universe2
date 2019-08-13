locals {
  kubeconfig = <<KUBECONFIG


apiVersion: v1
clusters:
- cluster:
    server: ${aws_eks_cluster.k8s_cluster.endpoint}
    certificate-authority-data: ${aws_eks_cluster.k8s_cluster.certificate_authority.0.data}
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: aws
  name: aws
current-context: aws
kind: Config
preferences: {}
users:
- name: aws
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      command: heptio-authenticator-aws
      args:
        - "token"
        - "-i"
        - "${var.clusterName}"
KUBECONFIG
}

resource "null_resource" "k8s_config" {
  provisioner "local-exec" {
    command = "echo \"${local.kubeconfig}\" > \"$HOME/.kube/config\""
  }

  depends_on = ["aws_eks_cluster.k8s_cluster"]
}

data "external" "aws_auth" {
  program = ["bash", "${path.module}/aws-auth.sh"]

  query = {
    cluster_name = var.clusterName
  }
}

provider "kubernetes" {
  host                   = aws_eks_cluster.k8s_cluster.endpoint
  cluster_ca_certificate = base64decode(aws_eks_cluster.k8s_cluster.certificate_authority.0.data)
  token                  = data.external.aws_auth.result.token
  load_config_file       = false
}

resource "kubernetes_config_map" "aws_auth" {
  metadata {
    name      = "aws-auth"
    namespace = "kube-system"
  }

  data = {
    mapRoles = <<YAML
- rolearn: ${aws_iam_role.k8s_nodes_role.arn}
  username: system:node:{{EC2PrivateDNSName}}
  groups:
    - system:bootstrappers
    - system:nodes
YAML
  }

  provisioner "local-exec" {
    command = "sleep 60"
  }

  depends_on = ["null_resource.k8s_config",
    "aws_autoscaling_group.k8s_nodes_autoscaling"
  ]
}

resource "kubernetes_service_account" "helm" {
  metadata {
    name      = "tiller"
    namespace = "kube-system"
  }

  provisioner "local-exec" {
    command = "kubectl create clusterrolebinding tiller-rule --clusterrole=cluster-admin --serviceaccount=${kubernetes_service_account.helm.metadata.0.namespace}:${kubernetes_service_account.helm.metadata.0.name}"
  }

  provisioner "local-exec" {
    command = "${path.module}/secure-tiller.sh ${kubernetes_service_account.helm.metadata.0.name}"
  }

  depends_on = ["kubernetes_config_map.aws_auth"]
}
