variable "clusterName" {}
variable "rtbId" {}
variable "vpcCidr" {}
variable "vpcSecondaryCidr" {}
variable "vpcId" {}
variable "eksSnetReg" {
  type = list(string)
}

resource "aws_subnet" "k8s_subnets" {
  count             = 2
  availability_zone = var.eksSnetReg[count.index]
  cidr_block        = cidrsubnet(var.vpcCidr, 2, count.index + 2)
  vpc_id            = var.vpcId

  tags = "${
    map(
     "Name", "Fluid-EKS",
     "kubernetes.io/cluster/${var.clusterName}", "shared",
    )
  }"
}

resource "aws_subnet" "k8s_subnets_secondary" {
  count             = 5
  availability_zone = var.eksSnetReg[count.index]
  cidr_block        = cidrsubnet(var.vpcSecondaryCidr, 3, count.index)
  vpc_id            = var.vpcId

  tags = "${
    map(
     "Name", "Fluid-EKS",
     "kubernetes.io/cluster/${var.clusterName}", "shared",
    )
  }"
}

resource "aws_route_table_association" "k8s_routetb_association" {
  count          = 2
  subnet_id      = aws_subnet.k8s_subnets.*.id[count.index]
  route_table_id = var.rtbId
}

resource "aws_route_table_association" "k8s_routetb_association_secondary" {
  count          = 5
  subnet_id      = aws_subnet.k8s_subnets_secondary.*.id[count.index]
  route_table_id = var.rtbId
}

output "k8sSubnet" {
  value = aws_subnet.k8s_subnets.*.id
}

output "k8sSubnetSeconday" {
  value = aws_subnet.k8s_subnets_secondary.*.id
}
