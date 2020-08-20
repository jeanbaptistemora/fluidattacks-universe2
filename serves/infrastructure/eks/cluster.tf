variable "clusterInstanceType" {}
variable "eksAmiId" {}
variable "nodeStorageSize" {}
variable "region" {}

resource "aws_eks_cluster" "k8s_cluster" {
  name            = var.clusterName
  role_arn        = aws_iam_role.k8s_master_role.arn

  vpc_config {
    security_group_ids = [aws_security_group.k8s_master_sec_group.id]
    subnet_ids         = aws_subnet.k8s_subnets.*.id
  }

  depends_on = [
    aws_iam_role_policy_attachment.k8s_master_policy_1,
    aws_iam_role_policy_attachment.k8s_master_policy_2,
  ]
}

locals {
  k8s_nodes_userdata = <<USERDATA
#!/bin/bash
set -o xtrace
/etc/eks/bootstrap.sh ${var.clusterName} \
  --use-max-pods true \
  --b64-cluster-ca ${aws_eks_cluster.k8s_cluster.certificate_authority.0.data} \
  --apiserver-endpoint ${aws_eks_cluster.k8s_cluster.endpoint}
USERDATA
}

resource "aws_ami_copy" "eks_ami_encrypted" {
  name  = "Fluid-EKS-Encrypted"
  source_ami_id     = var.eksAmiId
  source_ami_region = var.region
  description = "EKS Kubernetes Worker AMI with AmazonLinux2 image"
  encrypted   = true
}

resource "aws_launch_configuration" "k8s_nodes_launch_config" {
  associate_public_ip_address = true
  ebs_optimized               = true
  iam_instance_profile        = aws_iam_instance_profile.k8s_nodes_profile.name
  image_id                    = aws_ami_copy.eks_ami_encrypted.id
  instance_type               = var.clusterInstanceType
  name_prefix                 = "EKSWorkerNodes"
  security_groups             = [aws_security_group.k8s_nodes_sec_group.id]
  user_data_base64            = base64encode(local.k8s_nodes_userdata)

  root_block_device {
    volume_type = "gp2"
    volume_size = var.nodeStorageSize
    delete_on_termination = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "k8s_nodes_autoscaling" {
  desired_capacity     = 5
  launch_configuration = aws_launch_configuration.k8s_nodes_launch_config.id
  max_size             = 6
  min_size             = 5
  name                 = "EKSWorkerNodes"
  vpc_zone_identifier  = aws_subnet.k8s_subnets_secondary.*.id

  tag {
    key                 = "Name"
    value               = "Fluid-EKS"
    propagate_at_launch = true
  }

  tag {
    key                 = "kubernetes.io/cluster/${var.clusterName}"
    value               = "owned"
    propagate_at_launch = true
  }
}
