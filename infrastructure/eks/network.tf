resource "aws_vpc" "k8s_vpc" {
  cidr_block = "${var.vpc_cidr}"

  tags = "${
    map(
      "Name", "Fluid-EKS",
      "kubernetes.io/cluster/${var.cluster_name}", "shared",
    )
  }"
}

resource "aws_subnet" "k8s_subnets" {
  count = 2
  availability_zone = "${var.snet_regions[count.index]}"
  cidr_block        = "${cidrsubnet(aws_vpc.k8s_vpc.cidr_block, 2, count.index + 1)}"
  vpc_id            = "${aws_vpc.k8s_vpc.id}"

  tags = "${
    map(
     "Name", "Fluid-EKS",
     "kubernetes.io/cluster/${var.cluster_name}", "shared",
    )
  }"
}

resource "aws_internet_gateway" "k8s_gateway" {
  vpc_id = "${aws_vpc.k8s_vpc.id}"
}

resource "aws_route_table" "k8s_routetb" {
  vpc_id = "${aws_vpc.k8s_vpc.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.k8s_gateway.id}"
  }
}

resource "aws_route_table_association" "k8s_routetb_association" {
  count = 2
  subnet_id      = "${aws_subnet.k8s_subnets.*.id[count.index]}"
  route_table_id = "${aws_route_table.k8s_routetb.id}"
}
