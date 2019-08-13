# Master Security Group
resource "aws_security_group" "k8s_master_sec_group" {
  name        = "EKSMasterSecurityGroup"
  description = "Cluster communication with worker nodes"
  vpc_id      = var.vpcId

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Worker Nodes Security Group
resource "aws_security_group" "k8s_nodes_sec_group" {
  name        = "EKSWorkerNodesSecurityGroup"
  description = "Security group for all nodes in the cluster"
  vpc_id      = var.vpcId

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = "${
    map(
     "Name", "Fluid-EKS",
     "kubernetes.io/cluster/${var.clusterName}", "owned",
    )
  }"
}

resource "aws_security_group_rule" "k8s_nodes_nodes_rule" {
  description              = "Allow nodes to communicate with each other"
  from_port                = 0
  protocol                 = "-1"
  security_group_id        = aws_security_group.k8s_nodes_sec_group.id
  source_security_group_id = aws_security_group.k8s_nodes_sec_group.id
  to_port                  = 65535
  type                     = "ingress"
}

resource "aws_security_group_rule" "k8s_master_nodes_rule" {
  description              = "Allow worker Kubelets and pods to receive communication from the cluster control plane"
  from_port                = 1025
  protocol                 = "tcp"
  security_group_id        = aws_security_group.k8s_nodes_sec_group.id
  source_security_group_id = aws_security_group.k8s_master_sec_group.id
  to_port                  = 65535
  type                     = "ingress"
}

resource "aws_security_group_rule" "k8s_nodes_master_rule" {
  description              = "Allow pods to communicate with the cluster API Server"
  from_port                = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.k8s_master_sec_group.id
  source_security_group_id = aws_security_group.k8s_nodes_sec_group.id
  to_port                  = 443
  type                     = "ingress"
}
