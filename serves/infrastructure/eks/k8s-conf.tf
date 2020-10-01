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
