resource "null_resource" "aws_node_config" {
  depends_on = [
    module.eks
  ]
  provisioner "local-exec" {
    command = <<-EOT
      kubectl -n kube-system set env daemonset aws-node \
        MINIMUM_IP_TARGET=7 \
        WARM_IP_TARGET=3
    EOT
  }
}
