variable "clusterInstanceType" {}
variable "eksAmiId" {}
variable "newEksAmiId" {}
variable "region" {}

resource "aws_eks_cluster" "k8s_cluster" {
  name            = "${var.clusterName}"
  role_arn        = "${aws_iam_role.k8s_master_role.arn}"

  vpc_config {
    security_group_ids = ["${aws_security_group.k8s_master_sec_group.id}"]
    subnet_ids         = ["${aws_subnet.k8s_subnets.*.id}"]
  }

  depends_on = [
    "aws_iam_role_policy_attachment.k8s_master_policy_1",
    "aws_iam_role_policy_attachment.k8s_master_policy_2",
  ]
}

locals {
  k8s_nodes_userdata = <<USERDATA
#!/bin/bash -xe

CA_CERTIFICATE_DIRECTORY=/etc/kubernetes/pki
CA_CERTIFICATE_FILE_PATH=$CA_CERTIFICATE_DIRECTORY/ca.crt
mkdir -p $CA_CERTIFICATE_DIRECTORY
echo "${aws_eks_cluster.k8s_cluster.certificate_authority.0.data}" | base64 -d >  $CA_CERTIFICATE_FILE_PATH
INTERNAL_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
sed -i s,MASTER_ENDPOINT,${aws_eks_cluster.k8s_cluster.endpoint},g /var/lib/kubelet/kubeconfig
sed -i s,CLUSTER_NAME,${var.clusterName},g /var/lib/kubelet/kubeconfig
sed -i s,REGION,${var.region},g /etc/systemd/system/kubelet.service
sed -i s,MAX_PODS,17,g /etc/systemd/system/kubelet.service
sed -i s,MASTER_ENDPOINT,${aws_eks_cluster.k8s_cluster.endpoint},g /etc/systemd/system/kubelet.service
sed -i s,INTERNAL_IP,$INTERNAL_IP,g /etc/systemd/system/kubelet.service
DNS_CLUSTER_IP=10.100.0.10
if [[ $INTERNAL_IP == 10.* ]] ; then DNS_CLUSTER_IP=172.20.0.10; fi
sed -i s,DNS_CLUSTER_IP,$DNS_CLUSTER_IP,g /etc/systemd/system/kubelet.service
sed -i s,CERTIFICATE_AUTHORITY_FILE,$CA_CERTIFICATE_FILE_PATH,g /var/lib/kubelet/kubeconfig
sed -i s,CLIENT_CA_FILE,$CA_CERTIFICATE_FILE_PATH,g  /etc/systemd/system/kubelet.service
systemctl daemon-reload
systemctl restart kubelet
USERDATA
  k8s_nodes_userdata_apps = <<USERDATA
#!/bin/bash
set -o xtrace
/etc/eks/bootstrap.sh ${var.clusterName} \
  --use-max-pods true \
  --b64-cluster-ca ${aws_eks_cluster.k8s_cluster.certificate_authority.0.data} \
  --apiserver-endpoint ${aws_eks_cluster.k8s_cluster.endpoint} \
  --kubelet-extra-args --node-labels=role=apps
USERDATA
}

resource "aws_launch_configuration" "k8s_nodes_launch_config" {
  associate_public_ip_address = true
  iam_instance_profile        = "${aws_iam_instance_profile.k8s_nodes_profile.name}"
  image_id                    = "${var.eksAmiId}"
  instance_type               = "${var.clusterInstanceType}"
  name_prefix                 = "EKSWorkerNodes"
  security_groups             = ["${aws_security_group.k8s_nodes_sec_group.id}"]
  user_data_base64            = "${base64encode(local.k8s_nodes_userdata)}"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "k8s_nodes_autoscaling" {
  desired_capacity     = 3
  launch_configuration = "${aws_launch_configuration.k8s_nodes_launch_config.id}"
  max_size             = 5
  min_size             = 3
  name                 = "EKSWorkerNodes"
  vpc_zone_identifier  = ["${aws_subnet.k8s_subnets.*.id}"]

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

resource "aws_launch_configuration" "k8s_app_nodes_launch_config" {
  associate_public_ip_address = true
  iam_instance_profile        = "${aws_iam_instance_profile.k8s_nodes_profile.name}"
  image_id                    = "${var.newEksAmiId}"
  instance_type               = "${var.clusterInstanceType}"
  name_prefix                 = "EKSWorkerNodes"
  security_groups             = ["${aws_security_group.k8s_nodes_sec_group.id}"]
  user_data_base64            = "${base64encode(local.k8s_nodes_userdata_apps)}"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "k8s_app_nodes_autoscaling" {
  desired_capacity     = 2
  launch_configuration = "${aws_launch_configuration.k8s_app_nodes_launch_config.id}"
  max_size             = 4
  min_size             = 2
  name                 = "EKSWorkerNodes"
  vpc_zone_identifier  = ["${aws_subnet.k8s_subnets.*.id}"]

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
